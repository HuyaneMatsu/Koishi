__all__ = (
    'adventure_cancel_after', 'adventure_cancel_now', 'scheduled_adventure_arrival', 'set_adventure_action_notifier',
    'set_adventure_return_notifier'
)

from random import Random
from math import ceil

from hata import unix_time_to_datetime
from scarletio import Task, get_event_loop

from config import MARISA_MODE

from ....bot_utils.getter_setter_pair import getter_setter_pair_create
from ....bot_utils.time import unix_time_seconds_get

from ...inventory_core import get_inventory, save_inventory
from ...user_stats_core import user_stats_get, user_stats_save, user_stats_set_recovering_until
from ...seeding import step_seed, step_seed_initial

from ..action import (
    ACTION_ID_SYSTEM_ARRIVAL, ACTION_ID_SYSTEM_CANCELLATION_NOW, ACTION_ID_SYSTEM_CANCELLATION_AFTER,
    ACTION_ID_SYSTEM_UNKNOWN
)
from ..adventure import (
    ADVENTURE_STATE_ACTIONING, ADVENTURE_STATE_ACTIONING_CANCEL_AFTER, ADVENTURE_STATE_CANCELLED,
    ADVENTURE_STATE_DEPARTING, ADVENTURE_STATE_FINALISED, ADVENTURE_STATE_RETURNING, adventure_action_create,
    loot_data_build, adventure_set_state, adventure_set_updated_at, adventure_add_action,
    adventure_count_actions_for_seeding, adventure_increase_energy_exhausted, adventure_increase_health_exhausted
)
from ..constants import ADVENTURES_ACTIVE
from ..queries import adventure_save

from .helpers import (
    accumulate_looted_items, action_get, get_action_type_multiplier, action_duration_seconds_get,
    recovery_duration_seconds_get, travel_duration_seconds_get, should_cancel_adventure
)
from .loot_accumulation_logic import accumulate_action_loot


try:
    from ...adventure_recovery_over_reminder_hook import set_closest_adventure_recovery_over_reminder
except ImportError:
    if not MARISA_MODE:
        raise
    
    async def set_closest_adventure_recovery_over_reminder(user_id, date_time):
        return


LOOP = get_event_loop()

get_adventure_action_notifier, set_adventure_action_notifier = getter_setter_pair_create()
get_adventure_return_notifier, set_adventure_return_notifier = getter_setter_pair_create()


async def scheduled_adventure_arrival(adventure):
    """
    Begins the adventure by scheduling a handle for arrival.
    
    This function is a coroutine.
    
    Parameters
    ----------
    adventure : ``Adventure``
        The adventure to depart.
    """
    user_stats = await user_stats_get(adventure.user_id)
    
    travel_duration_seconds = travel_duration_seconds_get(adventure, user_stats)
    
    adventure.handle = LOOP.call_after(
        (adventure.updated_at + travel_duration_seconds - unix_time_seconds_get()),
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
    initial_seed = step_seed_initial(adventure.seed, 0)
    random = Random(initial_seed)
    action = action_get(adventure, random)
    if action is None:
        await adventure_unknown(adventure)
        return
    
    user_stats = await user_stats_get(adventure.user_id)
    multiplier = get_action_type_multiplier(action.type, user_stats)
    travel_duration_seconds = travel_duration_seconds_get(adventure, user_stats)
    loot_accumulations = accumulate_action_loot(action, random, multiplier)
    action_duration_seconds = action_duration_seconds_get(
        action.duration, random, loot_accumulations, multiplier
    )
    
    arrival_at = adventure.updated_at + travel_duration_seconds
    
    # Update the adventure.
    adventure_set_state(adventure, ADVENTURE_STATE_ACTIONING)
    adventure_set_updated_at(adventure, arrival_at)
    adventure_add_action(
        adventure,
        adventure_action_create(
            ACTION_ID_SYSTEM_ARRIVAL,
            arrival_at,
            None,
            None,
            0,
            0,
        ),
    )
    # Save
    await adventure_save(adventure)
    
    # Schedule new handle.
    adventure.handle = LOOP.call_after(
        (arrival_at + action_duration_seconds - unix_time_seconds_get()),
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
    initial_seed = step_seed_initial(adventure.seed, adventure_count_actions_for_seeding(adventure))
    random = Random(initial_seed)
    action = action_get(adventure, random)
    if action is None:
        await adventure_unknown(adventure)
        return
    
    user_stats = await user_stats_get(adventure.user_id)
    multiplier = get_action_type_multiplier(action.type, user_stats)
    loot_accumulations = accumulate_action_loot(action, random, multiplier)
    duration_seconds = action_duration_seconds_get(action.duration, random, loot_accumulations, multiplier)
    
    # Schedule new handle.
    adventure.handle = LOOP.call_after(
        (adventure.updated_at + duration_seconds - unix_time_seconds_get()),
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
    initial_seed = step_seed_initial(adventure.seed, adventure_count_actions_for_seeding(adventure))
    random = Random(initial_seed)
    action = action_get(adventure, random)
    if action is None:
        await adventure_unknown(adventure)
        return
    
    user_stats = await user_stats_get(adventure.user_id)
    inventory = await get_inventory(adventure.user_id)
    
    # We do not have battle system set up yet, so we ignore that step.
    health_exhausted = 0
    
    # Accumulate loot.
    multiplier = get_action_type_multiplier(action.type, user_stats)
    loot_accumulations = accumulate_action_loot(action, random, multiplier)
    duration_seconds = action_duration_seconds_get(action.duration, random, loot_accumulations, multiplier)
    
    looted_items, energy_exhausted = accumulate_looted_items(adventure, user_stats, inventory, loot_accumulations)
    energy_exhausted = ceil(energy_exhausted / multiplier)
    
    # Save inventory.
    await save_inventory(inventory)
    
    action_at = adventure.updated_at + duration_seconds
    
    # Update adventure.
    adventure_set_updated_at(adventure, action_at)
    adventure_increase_energy_exhausted(adventure, energy_exhausted)
    adventure_increase_health_exhausted(adventure, health_exhausted)
    
    # Calculate what we need for the next step.
    travel_duration_seconds = travel_duration_seconds_get(adventure, user_stats)
    
    next_initial_seed = step_seed(initial_seed)
    
    cancelling_after = adventure.state == ADVENTURE_STATE_ACTIONING_CANCEL_AFTER
    if cancelling_after:
        next_action = None
    else:
        next_random = Random(next_initial_seed)
        next_action = action_get(adventure, next_random)
    
    if next_action is None:
        should_return = True
        duration_seconds = travel_duration_seconds
        callback = invoke_adventure_return
    
    else:
        next_multiplier = get_action_type_multiplier(next_action.type, user_stats)
        next_loot_accumulations = accumulate_action_loot(next_action, next_random, next_multiplier)
        next_duration_seconds = action_duration_seconds_get(
            next_action.duration, next_random, next_loot_accumulations, next_multiplier
        )
        
        should_return = should_cancel_adventure(
            adventure,
            user_stats,
            inventory,
            action_at,
            next_duration_seconds,
            travel_duration_seconds,
            looted_items,
        )
        if should_return:
            duration_seconds = travel_duration_seconds
            callback = invoke_adventure_return
        else:
            duration_seconds = next_duration_seconds
            callback = invoke_adventure_action_step
    
    # Finish modifying the adventure.
    if should_return:
        adventure_set_state(adventure, ADVENTURE_STATE_RETURNING)
    
    # Create and insert the current action.
    adventure_action = adventure_action_create(
        action.id,
        action_at,
        None,
        loot_data_build(looted_items),
        health_exhausted,
        energy_exhausted,
    )
    adventure_add_action(adventure, adventure_action)
    
    # Insert a lost entry if we are lost.
    if (not cancelling_after) and (next_action is None):
        adventure_add_action(
            adventure,
                adventure_action_create(
                ACTION_ID_SYSTEM_UNKNOWN,
                action_at,
                None,
                None,
                0,
                0,
            ),
        )
    
    # Save
    await adventure_save(adventure)
    
    # Schedule new handle
    adventure.handle = LOOP.call_after(
        (action_at + duration_seconds - unix_time_seconds_get()),
        callback,
        adventure,
    )
    
    notifier = get_adventure_action_notifier()
    if (notifier is not None):
        await notifier(adventure, adventure_action)


async def adventure_cancel_now(adventure):
    """
    Cancels the adventure and schedules return.
    
    This function is a coroutine.
    
    Parameters
    ----------
    adventure : ``Adventure``
        The adventure to depart.
    """
    # Get user stats
    user_stats = await user_stats_get(adventure.user_id)
    
    # Skip if the adventure is in an invalid state.
    adventure_state = adventure.state
    if adventure_state not in (
        ADVENTURE_STATE_ACTIONING,
        ADVENTURE_STATE_ACTIONING_CANCEL_AFTER,
        ADVENTURE_STATE_DEPARTING,
    ):
        return
    
    # Cancel current handle.
    handle = adventure.handle
    if (handle is not None):
        handle.cancel()
    
    now_seconds = unix_time_seconds_get()
    
    # Update the adventure.
    adventure_set_state(adventure, ADVENTURE_STATE_CANCELLED)
    adventure_set_updated_at(adventure, now_seconds)
    
    
    # Create action for the cancellation.
    adventure_add_action(
        adventure,
        adventure_action_create(
            ACTION_ID_SYSTEM_CANCELLATION_NOW,
            now_seconds,
            None,
            None,
            0,
            0,
        ),
    )
    
    # save
    await adventure_save(adventure)
    
    # Schedule new handle.
    duration_seconds = travel_duration_seconds_get(adventure, user_stats)
    if adventure_state == ADVENTURE_STATE_DEPARTING:
        # Take the lowest in case we accumulated offset.
        duration_seconds = min(duration_seconds, (now_seconds - adventure.created_at))
    
    adventure.handle = LOOP.call_after(
        duration_seconds,
        invoke_adventure_return,
        adventure,
    )


async def adventure_cancel_after(adventure):
    """
    Cancels the adventure after the next action is done.
    
    This function is a coroutine.
    
    Parameters
    ----------
    adventure : ``Adventure``
        The adventure to depart.
    """
    # Skip if the adventure is in an invalid state.
    adventure_state = adventure.state
    if adventure_state != ADVENTURE_STATE_ACTIONING:
        return
    
    # Update the adventure.
    adventure_set_state(adventure, ADVENTURE_STATE_ACTIONING_CANCEL_AFTER)
    adventure_add_action(
        adventure,
        adventure_action_create(
            ACTION_ID_SYSTEM_CANCELLATION_AFTER,
            unix_time_seconds_get(),
            None,
            None,
            0,
            0,
        ),
    )
    await adventure_save(adventure)


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
    user_stats = await user_stats_get(adventure.user_id)
    duration_seconds = travel_duration_seconds_get(adventure, user_stats)
    
    # If the adventure is cancelled, we may have returned earlier
    if (adventure.state == ADVENTURE_STATE_CANCELLED) and (not adventure_count_actions_for_seeding(adventure)):
        duration_seconds = min(duration_seconds, (adventure.updated_at - adventure.created_at))
    
    return_at = adventure.updated_at + duration_seconds
    
    # Update adventure.
    adventure_set_state(adventure, ADVENTURE_STATE_FINALISED)
    adventure_set_updated_at(adventure, return_at)
    adventure.handle = None
    
    # Clear from cache.
    try:
        del ADVENTURES_ACTIVE[adventure.user_id]
    except KeyError:
        pass
    
    # Save adventure
    await adventure_save(adventure)
    
    # Calculate for how long the user is eeping after the adventure.
    recovery_duration_seconds = recovery_duration_seconds_get(adventure)
    if recovery_duration_seconds:
        recovering_until_date_time = unix_time_to_datetime((return_at + recovery_duration_seconds))
        user_stats_set_recovering_until(user_stats, recovering_until_date_time)
        await set_closest_adventure_recovery_over_reminder(user_stats, recovering_until_date_time)
        await user_stats_save(user_stats)
    
    
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
    user_stats = await user_stats_get(adventure.user_id)
    duration_seconds = travel_duration_seconds_get(adventure, user_stats)
    
    # If the adventure is cancelled, we may have returned earlier
    if (adventure.state == ADVENTURE_STATE_CANCELLED) and (not adventure_count_actions_for_seeding(adventure)):
        duration_seconds = min(duration_seconds, (adventure.updated_at - adventure.created_at))
    
    adventure.handle = LOOP.call_after(
        (adventure.updated_at + duration_seconds - unix_time_seconds_get()),
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
    user_stats = await user_stats_get(adventure.user_id)
    now_seconds = unix_time_seconds_get()
    
    # Update the adventure.
    adventure_set_state(adventure, ADVENTURE_STATE_RETURNING)
    adventure_set_updated_at(adventure, now_seconds)
    adventure_add_action(
        adventure,
        adventure_action_create(
            ACTION_ID_SYSTEM_UNKNOWN,
            now_seconds,
            None,
            None,
            0,
            0,
        ),
    )
    
    # Save
    await adventure_save(adventure)
    
    # Schedule new handle.
    adventure.handle = LOOP.call_after(
        travel_duration_seconds_get(adventure, user_stats),
        invoke_adventure_return,
        adventure,
    )
