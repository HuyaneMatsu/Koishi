__all__ = ('adventure_cancel', 'scheduled_adventure_arrival', 'set_adventure_return_notifier')

from datetime import datetime as DateTime, timedelta as TimeDelta, timezone as TimeZone

from scarletio import Task, get_event_loop

from ...inventory_core import get_inventory, save_inventory
from ...user_stats_core import get_user_stats

from ..action import ACTION_ID_SYSTEM_ARRIVAL, ACTION_ID_SYSTEM_CANCELLATION, ACTION_ID_SYSTEM_UNKNOWN
from ..adventure import (
    ADVENTURE_STATE_ACTIONING, ADVENTURE_STATE_CANCELLED, ADVENTURE_STATE_DEPARTING, ADVENTURE_STATE_FINALIZED,
    ADVENTURE_STATE_RETURNING, AdventureAction, build_loot_data
)
from ..constants import ADVENTURES_ACTIVE
from ..queries import store_adventure_action, update_adventure

from .helpers import (
    accumulate_looted_items, get_action, get_action_type_multiplier, get_duration_till_action_occurrence,
    get_duration_till_recovery_end, get_location_distance_travel_duration, get_should_cancel_adventure
)
from .loot_accumulation_logic import accumulate_action_loot
from .seed_stepping import step_seed, step_seed_initial


LOOP = get_event_loop()


def _adventure_return_notifier_slot():
    notifier = None
    
    def set_adventure_return_notifier(input_notifier):
        """
        Sets a notification deliverer for adventure return.
        
        Parameters
        ----------
        input_notifier : ``None | async (adventure : Adventure) -> None``
            Notification deliverer to set.
        """
        nonlocal notifier
        notifier = input_notifier
        
    def get_adventure_return_notifier():
        """
        Returns the notification deliverer for adventure return.
        
        Returns
        -------
        notifier : ``None | async (adventure : Adventure) -> None``
        """
        nonlocal notifier
        return notifier
    
    return set_adventure_return_notifier, get_adventure_return_notifier


set_adventure_return_notifier, get_adventure_return_notifier = _adventure_return_notifier_slot()
del _adventure_return_notifier_slot


async def scheduled_adventure_arrival(adventure):
    """
    Begins the adventure by scheduling a handle for arrival.
    
    This function is a coroutine.
    
    Parameters
    ----------
    adventure : ``Adventure``
        The adventure to depart.
    """
    user_stats = await get_user_stats(adventure.user_id)
    
    travel_duration = get_location_distance_travel_duration(adventure, user_stats)
    
    adventure.handle = LOOP.call_after(
        (adventure.updated_at + TimeDelta(seconds = travel_duration) - DateTime.now(tz = TimeZone.utc)).total_seconds(),
        invoke_adventure_arrival,
        adventure,
    )


def invoke_adventure_arrival(adventure):
    """
    Ensures that the adventurer arrives at the destination location.
    
    Parameters
    ----------
    adventure : ``Adventure``
        The adventure to update.
    """
    Task(LOOP, adventure_arrival(adventure))


async def adventure_arrival(adventure):
    """
    Ensures that the adventurer arrives at the destination location.
    
    This function is a coroutine.
    
    Parameters
    ----------
    adventure : ``Adventure``
        The adventure to update.
    """
    initial_seed = step_seed_initial(adventure.seed, adventure.action_count)
    action = get_action(adventure, initial_seed)
    if action is None:
        await adventure_unknown(adventure)
        return
    
    user_stats = await get_user_stats(adventure.user_id)
    multiplier = get_action_type_multiplier(action.type, user_stats)
    travel_duration = get_location_distance_travel_duration(adventure, user_stats)
    loot_accumulations, seed = accumulate_action_loot(action, initial_seed)
    duration = get_duration_till_action_occurrence(action.duration, initial_seed, loot_accumulations, multiplier)
    
    arrival_date = adventure.updated_at + TimeDelta(seconds = travel_duration)
    
    # Update the adventure.
    adventure.state = ADVENTURE_STATE_ACTIONING
    adventure.updated_at = arrival_date
    adventure.action_count += 1
    # Save
    await update_adventure(adventure)
    
    adventure_action = AdventureAction(
        adventure.entry_id,
        ACTION_ID_SYSTEM_ARRIVAL,
        arrival_date,
        None,
        None,
        0,
        0,
    )
    # Save
    await store_adventure_action(adventure_action)
    
    # Schedule new handle.
    adventure.handle = LOOP.call_after(
        (arrival_date + TimeDelta(seconds = duration) - DateTime.now(tz = TimeZone.utc)).total_seconds(),
        invoke_adventure_action_step,
        adventure,
    )


async def schedule_adventure_action(adventure):
    """
    Schedules a new action of the action.
    
    This function is a coroutine.
    
    Parameters
    ----------
    adventure : ``Adventure``
        The adventure to update.
    """
    initial_seed = step_seed_initial(adventure.seed, adventure.action_count)
    action = get_action(adventure, initial_seed)
    if action is None:
        await adventure_unknown(adventure)
        return
    
    user_stats = await get_user_stats(adventure.user_id)
    multiplier = get_action_type_multiplier(action.type, user_stats)
    loot_accumulations, seed = accumulate_action_loot(action, initial_seed)
    duration = get_duration_till_action_occurrence(action.duration, initial_seed, loot_accumulations, multiplier)
    
    # Schedule new handle.
    adventure.handle = LOOP.call_after(
        (adventure.updated_at + TimeDelta(seconds = duration) - DateTime.now(tz = TimeZone.utc)).total_seconds(),
        invoke_adventure_action_step,
        adventure,
    )


def invoke_adventure_action_step(adventure):
    """
    Ensures that the adventure's next action occurs.
    
    Parameters
    ----------
    adventure : ``Adventure``
        The adventure to update.
    """
    Task(LOOP, adventure_action_step(adventure))


async def adventure_action_step(adventure):
    """
    Called when an adventure's next action occurs.
    
    This function is a coroutine.
    
    Parameters
    ----------
    adventure : ``Adventure``
        The adventure to update.
    """
    initial_seed = step_seed_initial(adventure.seed, adventure.action_count)
    action = get_action(adventure, initial_seed)
    if action is None:
        await adventure_unknown(adventure)
        return
    
    user_stats = await get_user_stats(adventure.user_id)
    inventory = await get_inventory(adventure.user_id)
    
    # We do not have battle system set up yet, so we ignore that step.
    health_exhausted = 0
    
    # Accumulate loot.
    loot_accumulations, seed = accumulate_action_loot(action, initial_seed)
    multiplier = get_action_type_multiplier(action.type, user_stats)
    duration = get_duration_till_action_occurrence(action.duration, initial_seed, loot_accumulations, multiplier)
    
    looted_items, energy_exhausted = accumulate_looted_items(
        adventure, user_stats, inventory, loot_accumulations, multiplier
    )
    
    # Save inventory.
    await save_inventory(inventory)
    
    action_date = adventure.updated_at + TimeDelta(seconds = duration)
    
    # Update adventure.
    adventure.updated_at = action_date
    adventure.action_count += 1
    adventure.energy_exhausted += energy_exhausted
    adventure.health_exhausted += health_exhausted
    
    # Calculate what we need for the next step.
    travel_duration = get_location_distance_travel_duration(adventure, user_stats)
    
    next_initial_seed = step_seed(initial_seed)
    next_action = get_action(adventure, next_initial_seed)
    
    if next_action is None:
        should_return = True
        duration = travel_duration
        callback = invoke_adventure_return
    
    else:
        next_loot_accumulations, next_seed = accumulate_action_loot(next_action, next_initial_seed)
        next_multiplier = get_action_type_multiplier(next_action.type, user_stats)
        next_duration = get_duration_till_action_occurrence(
            next_action.duration, next_initial_seed, next_loot_accumulations, next_multiplier
        )
        
        should_return = get_should_cancel_adventure(
            adventure, user_stats, inventory, action_date, next_duration, travel_duration
        )
        if should_return:
            duration = travel_duration
            callback = invoke_adventure_return
        else:
            duration = next_duration
            callback = invoke_adventure_action_step
    
    # Finish modifying the adventure.
    
    # If next step is unknown we will insert +1 action
    if next_action is None:
        adventure.action_count += 1
    
    if should_return:
        adventure.state = ADVENTURE_STATE_RETURNING
    
    # Save
    await update_adventure(adventure)
    
    # Create and insert the current action.
    adventure_action = AdventureAction(
        adventure.entry_id,
        action.id,
        action_date,
        None,
        build_loot_data(looted_items),
        health_exhausted,
        energy_exhausted,
    )
    # Save
    await store_adventure_action(adventure_action)
    
    # Insert a lost entry if we are lost.
    if next_action is None:
        adventure_action = AdventureAction(
            adventure.entry_id,
            ACTION_ID_SYSTEM_UNKNOWN,
            action_date,
            None,
            None,
            0,
            0,
        )
        # Save
        await store_adventure_action(adventure_action)
    
    # Schedule new handle
    adventure.handle = LOOP.call_after(
        (action_date + TimeDelta(seconds = duration) - DateTime.now(tz = TimeZone.utc)).total_seconds(),
        callback,
        adventure,
    )


async def adventure_cancel(adventure):
    """
    Cancels the adventure and schedules return.
    
    This function is a coroutine.
    
    Parameters
    ----------
    adventure : ``Adventure``
        The adventure to depart.
    """
    # Get user stats
    user_stats = await get_user_stats(adventure.user_id)
    
    # Skip if the adventure is in an invalid state.
    adventure_state = adventure.state
    if adventure_state not in (ADVENTURE_STATE_ACTIONING, ADVENTURE_STATE_DEPARTING):
        return
    
    # Cancel current handle.
    handle = adventure.handle
    if (handle is not None):
        handle.cancel()
    
    now = DateTime.now(tz = TimeZone.utc)
    
    # Update the adventure.
    adventure.state = ADVENTURE_STATE_CANCELLED
    adventure.updated_at = now
    adventure.action_count += 1
    await update_adventure(adventure)
    
    # Create action for the cancellation.
    adventure_action = AdventureAction(
        adventure.entry_id,
        ACTION_ID_SYSTEM_CANCELLATION,
        now,
        None,
        None,
        0,
        0,
    )
    await store_adventure_action(adventure_action)
    
    # Schedule new handle.
    duration = get_location_distance_travel_duration(adventure, user_stats)
    if adventure_state != ADVENTURE_STATE_ACTIONING:
        # Take the lowest in case we accumulated offset.
        duration = min(duration, (adventure.created_at - now).total_seconds())
    
    adventure.handle = LOOP.call_after(
        duration,
        invoke_adventure_return,
        adventure,
    )


def invoke_adventure_return(adventure):
    """
    Called when the adventurer return homes.
    
    Parameters
    ----------
    adventure : ``Adventure``
        The adventure to update.
    """
    Task(LOOP, adventure_return(adventure))


async def adventure_return(adventure):
    """
    Ensured when the adventurer return homes.
    
    This function is a coroutine.
    
    Parameters
    ----------
    adventure : ``Adventure``
        The adventure to update.
    """
    user_stats = await get_user_stats(adventure.user_id)
    duration = get_location_distance_travel_duration(adventure, user_stats)
    
    # If the adventure is cancelled, we may have returned earlier
    if (adventure.state == ADVENTURE_STATE_CANCELLED) and (adventure.action_count == 1):
        duration = min(duration, (adventure.updated_at - adventure.created_at).total_seconds())
    
    return_date = adventure.updated_at + TimeDelta(seconds = duration)
    
    # Update adventure.
    adventure.state = ADVENTURE_STATE_FINALIZED
    adventure.updated_at = return_date
    adventure.handle = None
    
    # Clear from cache.
    try:
        del ADVENTURES_ACTIVE[adventure.user_id]
    except KeyError:
        pass
    
    # Save adventure
    await update_adventure(adventure)
    
    # Calculate for how long the user is eeping after the adventure.
    duration_till_recovery_end = get_duration_till_recovery_end(adventure)
    if duration_till_recovery_end:
        user_stats.set('recovering_until', return_date + TimeDelta(seconds = duration_till_recovery_end))
        await user_stats.save()
    
    # Notify
    notifier = get_adventure_return_notifier()
    if (notifier is not None):
        await notifier(adventure)


async def schedule_adventure_return(adventure):
    """
    Schedules adventure return.
    
    This function is a coroutine.
    
    Parameters
    ----------
    adventure : ``Adventure``
        The adventure to update.
    """
    user_stats = await get_user_stats(adventure.user_id)
    duration = get_location_distance_travel_duration(adventure, user_stats)
    
    # If the adventure is cancelled, we may have returned earlier
    if (adventure.state == ADVENTURE_STATE_CANCELLED) and (adventure.action_count == 1):
        duration = min(duration, (adventure.updated_at - adventure.created_at).total_seconds())
    
    adventure.handle = LOOP.call_after(
        (adventure.updated_at + TimeDelta(seconds = duration) - DateTime.now(tz = TimeZone.utc)).total_seconds(),
        invoke_adventure_return,
        adventure,
    )


def invoke_adventure_unknown(adventure):
    """
    Called when an adventure visits a seemingly unknown location.
    We cannot handle it, because something references to an entity that is do not exist.
    
    Parameters
    ----------
    adventure : ``Adventure``
        The adventure to update.
    """
    Task(LOOP, adventure_unknown(adventure))


async def adventure_unknown(adventure):
    """
    Ensured when an adventure visits a seemingly unknown location.
    
    This function is a coroutine.
    
    Parameters
    ----------
    adventure : ``Adventure``
        The adventure to update.
    """
    user_stats = await get_user_stats(adventure.user_id)
    now = DateTime.now(tz = TimeZone.utc)
    
    # Update the adventure.
    adventure.state = ADVENTURE_STATE_RETURNING
    adventure.updated_at = now
    adventure.action_count += 1
    
    # Save
    await update_adventure(adventure)
    
    # Create action for being lost.
    adventure_action = AdventureAction(
        adventure.entry_id,
        ACTION_ID_SYSTEM_UNKNOWN,
        now,
        None,
        None,
        0,
        0,
    )
    # Save
    await store_adventure_action(adventure_action)
    
    # Schedule new handle.
    adventure.handle = LOOP.call_after(
        get_location_distance_travel_duration(adventure, user_stats),
        invoke_adventure_return,
        adventure,
    )
