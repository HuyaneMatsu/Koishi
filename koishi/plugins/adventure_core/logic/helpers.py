__all__ = ('can_cancel_adventure', 'get_duration_till_recovery_end', 'get_location_distance_travel_duration',)


from datetime import datetime as DateTime
from math import floor, log
from sys import modules

from scarletio import copy_docs

from config import MARISA_MODE

from ...item_core import get_item

from ..action import (
    ACTION_TYPE_BUTCHERING, ACTION_TYPE_ENCOUNTER, ACTION_TYPE_FISHING, ACTION_TYPE_FORAGING, ACTION_TYPE_GARDENING,
    ACTION_TYPE_HUNT, ACTION_TYPE_TRAP
)
from ..adventure import (
    ADVENTURE_STATE_ACTIONING, ADVENTURE_STATE_DEPARTING, LOOT_STATE_LOST_DUE_FULL_INVENTORY,
    LOOT_STATE_LOST_DUE_LOW_ENERGY, LOOT_STATE_SUCCESS
)
from ..auto_cancellation import check_auto_cancellation_conditions
from ..constants import (
    ACTIONS, AUTO_CANCELLATIONS, DISTANCE_DEFAULT, LOCATIONS, RECOVERY_DURATION_BY_LOST_ENERGY,
    RECOVERY_DURATION_BY_LOST_HEALTH, RECOVERY_DURATION_MULTIPLIER_FATALITY, TARGETS, TEST_MODE_DURATION_DIVIDER
)
from ..return_ import RETURN_ID_BEFORE


def get_location_distance_travel_duration(adventure, user_stats):
    """
    Gets how long traveling to the target location takes.
    
    Parameters
    ----------
    adventure : ``Adventure``
        The adventure to update.
    
    user_stats : ``UserStats``
        The user's stats.
    
    Returns
    -------
    duration : `int`
    """
    try:
        location = LOCATIONS[adventure.location_id]
    except KeyError:
        distance = DISTANCE_DEFAULT
    else:
        distance = location.distance
    
    return distance * 1000 // user_stats.stats_calculated.extra_movement


def get_duration_till_action_occurrence(base_duration, random, loot_accumulations, multiplier):
    """
    Gets duration till action occurrence.
    
    Parameters
    ----------
    base_duration : `int`
        The action's base duration.
    
    random : `random.Random`
        Random number generator to use.
    
    loot_accumulations : ``dict<int, LootAccumulation>``
        Accumulated loot from the action.
    
    multiplier : `float`
        Multiplier of the user for this given action.
    
    Returns
    -------
    duration : `int`
    """
    # Set the required duration between 0.5 - 1.5 times of the action's duration.
    duration = (base_duration >> 1) + (random.random() * (base_duration + 1))
    duration = floor(duration / multiplier)
    
    duration = sum((loot_accumulation.duration_cost for loot_accumulation in loot_accumulations.values()), duration)
    return duration


def get_action_type_multiplier(action_type, user_stats):
    """
    Gets multiplier for the given action type.
    
    Parameters
    ----------
    action_type : `int`
        The action's type.
    
    user_stats : ``UserStats``
        The user's stats.
    
    Returns
    -------
    multiplier : `float`
    """
    user_stats_calculated = user_stats.stats_calculated
    if action_type == ACTION_TYPE_GARDENING:
        stat = user_stats_calculated.extra_gardening
    
    elif action_type == ACTION_TYPE_FORAGING:
        stat = user_stats_calculated.extra_foraging
    
    elif action_type == ACTION_TYPE_BUTCHERING:
        stat = user_stats_calculated.extra_butchering
    
    elif action_type == ACTION_TYPE_FISHING:
        stat = user_stats_calculated.extra_fishing
    
    elif action_type == ACTION_TYPE_ENCOUNTER:
        # This one gets no special treatment.
        stat = 10
    
    elif action_type == ACTION_TYPE_HUNT:
        stat = user_stats_calculated.extra_hunting
    
    elif action_type == ACTION_TYPE_TRAP:
        stat = user_stats_calculated.extra_movement // 80
    
    else:
        stat = 10
    
    return log(stat) / 2.302585092994046


def get_action(adventure, random):
    """
    Gets action for adventure stepping.
    
    Parameters
    ----------
    adventure : ``Adventure``
        The adventure to update.
    
    random : `random.Random`
        Random number generator to use.
    
    Returns
    -------
    action : ``None | Action``
    """
    try:
        target = TARGETS[adventure.target_id]
    except KeyError:
        return
    
    action_ids = target.action_ids
    action_count = len(action_ids)
    if not action_count:
        return
    
    if action_count == 1:
        action_id = action_ids[0]
        try:
            action = ACTIONS[action_id]
        except KeyError:
            return
    
    else:
        actions = []
        for action_id in action_ids:
            try:
                action = ACTIONS[action_id]
            except KeyError:
                return
            
            actions.append(action)
        
        action_location = floor(random.random() % sum(action.weight for action in actions))
        for action in actions:
            action_location -= action.weight
            if action_location < 0:
                break
    
    return action


def accumulate_looted_item_loss_due_to_low_energy(loot_accumulations, looted_items, available_energy):
    """
    Accumulates how much items we lost due to not having enough energy.
    
    Parameters
    ----------
    loot_accumulations : ``dict<int, LootAccumulation>``
        Accumulated loot from the action.
    
    looted_items : `list<(int, int, int)>`
        Already accumulated looted items. 
        A list of tuple of 3 elements: loot state, item id and given amount.
    
    available_energy : `int`
        The available energy of the user.
    
    Returns
    -------
    energy_exhausted : `int`
    """
    total_energy_required = sum(
        loot_accumulation.energy_cost for loot_accumulation in loot_accumulations.values()
    )
    if available_energy >= total_energy_required:
        energy_exhausted = total_energy_required
    
    elif available_energy <= 0:
        energy_exhausted = 0
        
        # if the energy is at 0 already, we remove all items
        for item_id, loot_accumulation in loot_accumulations.items():
            looted_items.append((LOOT_STATE_LOST_DUE_LOW_ENERGY, item_id, loot_accumulation.amount))
        
        loot_accumulations.clear()
    
    else:
        energy_exhausted = available_energy
        
        multiplier_lost_due_low_energy = available_energy / total_energy_required
        to_remove_item_ids = None
        
        for item_id, loot_accumulation in loot_accumulations.items():
            amount = loot_accumulation.amount
            left = floor(amount * multiplier_lost_due_low_energy)
            reduction = amount - left
            
            if left:
                loot_accumulation.amount = left
            
            else:
                if to_remove_item_ids is None:
                    to_remove_item_ids = []
                to_remove_item_ids.append(item_id)
            
            looted_items.append((LOOT_STATE_LOST_DUE_LOW_ENERGY, item_id, reduction))
        
        # Clear the ones that went down to 0
        if (to_remove_item_ids is not None):
            for item_id in to_remove_item_ids:
                try:
                    del loot_accumulations[item_id]
                except KeyError:
                    pass
    
    return energy_exhausted


def accumulate_looted_item_loss_due_to_low_inventory(loot_accumulations, looted_items, available_inventory):
    """
    Accumulates how much items we lost due to not having enough inventory.
    
    Parameters
    ----------
    loot_accumulations : ``dict<int, LootAccumulation>``
        Accumulated loot from the action.
    
    looted_items : `list<(int, int, int)>`
        Already accumulated looted items. 
        A list of tuple of 3 elements: loot state, item id and given amount.
    
    available_inventory : `int`
        The available inventory of the user.
    """
    total_inventory_required = sum(
        get_item(item_id).weight * loot_accumulation.amount
        for item_id, loot_accumulation in loot_accumulations.items()
    )
    
    if available_inventory > total_inventory_required:
        pass
    
    elif available_inventory <= 0:
        # Available inventory is already 0, we remove all items.
        for item_id, loot_accumulation in loot_accumulations.items():
            looted_items.append((LOOT_STATE_LOST_DUE_FULL_INVENTORY, item_id, loot_accumulation.amount))
        
        loot_accumulations.clear()
    
    else:
        multiplier_due_to_low_inventory = available_inventory / total_inventory_required
        to_remove_item_ids = None
        
        for item_id, loot_accumulation in loot_accumulations.items():
            amount = loot_accumulation.amount
            left = floor(amount * multiplier_due_to_low_inventory)
            reduction = amount - left
            
            if left:
                loot_accumulation.amount = left
            
            else:
                if (to_remove_item_ids is None):
                    to_remove_item_ids = []
                to_remove_item_ids.append(item_id)
            
            looted_items.append((LOOT_STATE_LOST_DUE_FULL_INVENTORY, item_id, reduction))
        
        # Clear the ones that went down to 0
        if (to_remove_item_ids is not None):
            for item_id in to_remove_item_ids:
                try:
                    del loot_accumulations[item_id]
                except KeyError:
                    pass


def accumulate_looted_items(adventure, user_stats, inventory, loot_accumulations, multiplier):
    """
    Accumulates how much items the user looted.
    
    Parameters
    ----------
    adventure : ``Adventure``
        Adventure in context.
    
    user_stats : ``UserStats``
        The user's stats.
    
    inventory : ``Inventory``
        The user's inventory.
    
    loot_accumulations : ``dict<int, LootAccumulation>``
        Accumulated loot from the action.
    
    multiplier : `float`
        Multiplier of the user for this given action.
    
    Returns
    -------
    looted_items_and_energy_exhausted : `(list<(int, int, int)>, int)`
        The accumulated looted items and the used energy by it. 
    """
    looted_items = []
    
    while True:
        # Apply stat based multiplier.
        if not loot_accumulations:
            energy_exhausted = 0
            break
        
        for loot_accumulation in loot_accumulations.values():
            loot_accumulation.amount = floor(loot_accumulation.amount * multiplier)
        
        # Calculate how much energy we have available and reduce the loot amount as required.
        energy_exhausted = accumulate_looted_item_loss_due_to_low_energy(
            loot_accumulations, looted_items, adventure.energy_initial - adventure.energy_exhausted
        )
        if not loot_accumulations:
            break
        
        # Calculate how much inventory space we have available and reduce the loot amount as required.
        available_inventory = user_stats.stats_calculated.extra_inventory - inventory.weight
        accumulate_looted_item_loss_due_to_low_inventory(
            loot_accumulations, looted_items, available_inventory
        )
        if not loot_accumulations:
            break
        
        # At this point we should be able to give all items to the user.
        for item_id, loot_accumulation in loot_accumulations.items():
            looted_items.append((LOOT_STATE_SUCCESS, item_id, loot_accumulation.amount))
            inventory.modify_item_amount(get_item(item_id), loot_accumulation.amount)
        
        loot_accumulations.clear()
        break
    
    return looted_items, energy_exhausted


def get_should_cancel_adventure(adventure, user_stats, inventory, now, duration_till_next_occurrence, travel_duration):
    """
    Gets whether the adventure should be cancelled.
    
    Parameters
    ----------
    adventure : ``Adventure``
        Adventure in context.
    
    user_stats : ``UserStats``
        The user's stats.
    
    inventory : ``Inventory``
        The user's inventory.
    
    now : `DateTime`
        The current time.
    
    duration_till_next_occurrence : `int`
        How much is the duration till the next occurrence.
    
    travel_duration : `int`
        The duration to travel back.
    
    Returns
    -------
    should_cancel : `bool`
    """
    # If we are out of time, we always return.
    available_duration = adventure.initial_duration - floor((now - adventure.created_at).total_seconds())
    if available_duration <= 0:
        return True
    
    # If we want to return before timeout, then we also add the next occurrence time to it.
    if adventure.return_id == RETURN_ID_BEFORE:
        added_duration = duration_till_next_occurrence
    else:
        added_duration = 0
    
    if available_duration < (added_duration + travel_duration):
        return True
    
    # Check whether we should auto cancel the adventure.
    try:
        auto_cancellation = AUTO_CANCELLATIONS[adventure.auto_cancellation_id]
    except KeyError:
        pass
    else:
        cancelled = check_auto_cancellation_conditions(
            auto_cancellation,
            user_stats.stats_calculated.extra_inventory,
            inventory.weight,
            adventure.health_initial,
            adventure.health_exhausted,
            adventure.energy_initial,
            adventure.energy_exhausted,
        )
        if cancelled:
            return True
        
    # No more conditions
    return False


def get_duration_till_recovery_end(adventure):
    """
    Gets the duration till the user recovery from its adventure.
    
    Parameters
    ----------
    adventure : ``Adventure``
        The adventure the user finished.
    
    Returns
    -------
    duration : `int`
    """
    health_exhausted = adventure.health_exhausted
    energy_exhausted = adventure.energy_exhausted
    
    duration = health_exhausted * RECOVERY_DURATION_BY_LOST_HEALTH + energy_exhausted * RECOVERY_DURATION_BY_LOST_ENERGY
    if health_exhausted >= adventure.health_initial:
        duration *= RECOVERY_DURATION_MULTIPLIER_FATALITY
    
    return duration


def can_cancel_adventure(adventure):
    """
    Returns whether the adventure can be cancelled.
    
    Parameters
    ----------
    adventure : ``Adventure``
        The adventure to check.
    
    Returns
    -------
    can_cancel : `bool`
    """
    return adventure.state in (ADVENTURE_STATE_ACTIONING, ADVENTURE_STATE_DEPARTING)


# Reduce the durations if the plugin is ran in test mode.
if MARISA_MODE and ('vampytest' not in modules):
    _get_location_distance_travel_duration = get_location_distance_travel_duration
    
    @copy_docs(get_location_distance_travel_duration)
    def get_location_distance_travel_duration(adventure, user_stats):
        return _get_location_distance_travel_duration(adventure, user_stats) // TEST_MODE_DURATION_DIVIDER
    
    
    _get_duration_till_action_occurrence = get_duration_till_action_occurrence
    
    @copy_docs(get_duration_till_action_occurrence)
    def get_duration_till_action_occurrence(base_duration, random, loot_accumulations, multiplier):
        return _get_duration_till_action_occurrence(
            base_duration, random, loot_accumulations, multiplier
        ) // TEST_MODE_DURATION_DIVIDER
    
    
    _get_duration_till_recovery_end = get_duration_till_recovery_end
    
    @copy_docs(get_duration_till_recovery_end)
    def get_duration_till_recovery_end(adventure):
        return _get_duration_till_recovery_end(adventure) // TEST_MODE_DURATION_DIVIDER
