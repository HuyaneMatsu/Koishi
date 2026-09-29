__all__ = ()

from dateutil.relativedelta import relativedelta as RelativeDelta
from hata import (
    DATETIME_FORMAT_CODE, TIMESTAMP_STYLES, elapsed_time, format_datetime, format_unix_time, unix_time_to_datetime
)

from ...bot_utils.time import unix_time_seconds_get

from ..adventure_core import (
    ACTIONS, ACTION_TYPE_ARRIVAL, ACTION_TYPE_BUTCHERING, ACTION_TYPE_CANCELLATION, ACTION_TYPE_ENCOUNTER,
    ACTION_TYPE_FATALITY, ACTION_TYPE_FISHING, ACTION_TYPE_FORAGING, ACTION_TYPE_GARDENING, ACTION_TYPE_HUNT,
    ACTION_TYPE_NONE, ACTION_TYPE_TRAP, ACTION_TYPE_UNKNOWN, ADVENTURE_STATE_ACTIONING,
    ADVENTURE_STATE_ACTIONING_CANCEL_AFTER, ADVENTURE_STATE_CANCELLED, ADVENTURE_STATE_DEPARTING,
    ADVENTURE_STATE_FINALISED, ADVENTURE_STATE_RETURNING, AUTO_CANCELLATIONS, LOCATIONS,
    LOOT_STATE_LOST_DUE_FULL_INVENTORY, LOOT_STATE_LOST_DUE_LOW_ENERGY, LOOT_STATE_SUCCESS, RETURNS, TARGETS,
    produce_auto_cancellation_conditions, produce_auto_cancellation_conditions_listing, produce_goal,
    recovery_duration_seconds_get
)
from ..item_core import get_item
from ..unit_core import produce_duration_sophisticated, produce_kilogram, produce_kilogram_ratio

from .constants import (
    ADVENTURE_CANCELLATION_MODE_AFTER, ADVENTURE_CANCELLATION_MODE_NOW, ADVENTURE_LOOT_LISTING_MODE_DEFAULT,
    ADVENTURE_LOOT_LISTING_MODE_THIS_STEP, ADVENTURE_LOOT_LISTING_MODE_TOTAL
)


ACTION_TYPE_NAME_DEFAULT = 'Unknown'

ACTION_TYPE_TO_NAME = {
    ACTION_TYPE_NONE : 'Nothing',
    ACTION_TYPE_CANCELLATION : 'Cancellation',
    ACTION_TYPE_ARRIVAL : 'Arrival',
    ACTION_TYPE_FATALITY : 'Fatality',
    ACTION_TYPE_UNKNOWN : ACTION_TYPE_NAME_DEFAULT,
    
    ACTION_TYPE_GARDENING : 'Gardening',
    ACTION_TYPE_FORAGING : 'Foraging',
    ACTION_TYPE_BUTCHERING : 'Butchering',
    
    ACTION_TYPE_FISHING : 'Fishing',
    ACTION_TYPE_ENCOUNTER : 'Encounter',
    ACTION_TYPE_HUNT : 'Hunt',
    
    ACTION_TYPE_TRAP : 'Trapped',
}


def produce_adventure_initial_representation(location, target, duration, return_, auto_cancellation, goal):
    """
    Produces an adventure's initial representation.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    location : ``Location``
        Target duration.
    
    target : ``Target``
        Target action set.
    
    duration : `int`
        Duration.
    
    return_ : ``Return``
        Return logic identifier.
    
    auto_cancellation : ``AutoCancellation``
        Auto cancellation.
    
    goal : ``None | Goal``
        The goal of the adventure.
    
    Yields
    ------
    part : `str`
    """
    yield 'Location: '
    yield location.name
    
    yield '\nTarget: '
    yield target.name
    
    yield '\nDuration: '
    yield from produce_duration_sophisticated(duration)
    
    yield '\nReturn: '
    yield return_.name
    
    yield '\nAuto-cancellation: '
    yield auto_cancellation.name
    yield ' ('
    yield from produce_auto_cancellation_conditions(auto_cancellation)
    yield ')'
    
    if (goal is not None):
        yield '\nGoal: '
        yield from produce_goal(goal)


def _produce_adventure_location_for_headers(adventure):
    """
    Helper function to produce adventure location for headers.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    adventure : ``Adventure``
        Adventure to produce for.
    
    Yields
    ------
    part : `str`
    """
    try:
        location = LOCATIONS[adventure.location_id]
    except KeyError:
        location_name = 'unknown'
    else:
        location_name = location.name
    
    try:
        target = TARGETS[adventure.target_id]
    except KeyError:
        target_name = 'unknown'
    else:
        target_name = target.name
    
    yield location_name
    yield ' for '
    yield target_name


def produce_adventure_cancellation_confirmation_description(adventure):
    """
    Produces an adventure cancellation confirmation description.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    adventure : ``Adventure``
        Adventure to produce description for.
    
    Yields
    ------
    part : `str`
    """
    yield 'Are you sure to cancel your adventure towards '
    yield from _produce_adventure_location_for_headers(adventure)
    yield '?'


def produce_butcher_header(item):
    """
    Produces butcher header.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    item : ``Item``
        Item to produce header for.
    
    Yields
    ------
    part : `str`    
    """
    yield '# Butchering '
    emoji = item.emoji
    if (emoji is not None):
        yield emoji.as_emoji
        yield ' '
    
    yield item.name


def produce_adventure_view_header(adventure):
    """
    Produces an adventure view header.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    adventure : ``Adventure``
        Adventure to produce header for.
    
    Yields
    ------
    part : `str`
    """
    yield '### Adventure to '
    yield from _produce_adventure_location_for_headers(adventure)


def produce_adventure_return_notification_header(adventure):
    """
    Produces an adventure return notification header.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    adventure : ``Adventure``
        Adventure to produce header for.
    
    Yields
    ------
    part : `str`
    """
    yield '### You have returned from adventure at '
    yield from _produce_adventure_location_for_headers(adventure)


def produce_adventure_return_notification_description(adventure):
    """
    Produces an adventure return notification description.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    adventure : ``Adventure``
        Adventure to produce description for.
    
    Yields
    ------
    part : `str`
    """
    duration_seconds = recovery_duration_seconds_get(adventure)
    until_seconds = adventure.updated_at + duration_seconds
    
    yield 'You are recovering for '
    yield elapsed_time(RelativeDelta(seconds = duration_seconds))
    yield ', until '
    yield format_unix_time(until_seconds, TIMESTAMP_STYLES.long_time)
    yield '.'


def produce_adventure_action_notification_header(adventure, adventure_action):
    """
    Produces adventure action notification header.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    adventure : ``Adventure``
        The adventure the user is on.
    
    adventure_action : ``AdventureAction``
        The adventure action to display.
    
    Yields
    ------
    part : `str`
    """
    yield '### '
    yield from _produce_adventure_action_type_for_headers(adventure_action)
    yield ' at '
    yield from _produce_adventure_location_for_headers(adventure)


def produce_adventure_action_listing_view_header(adventure, page_index):
    """
    Produces an adventure action listing view header.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    adventure : ``Adventure``
        Adventure to produce header for.
    
    page_index : `int`
        The shown page's index.
    
    Yields
    ------
    part : `str`
    """
    yield '### Actions of '
    yield from _produce_adventure_location_for_headers(adventure)
    yield ' (page '
    yield str(page_index + 1)
    yield ')'


def produce_adventure_listing_view_header(page_index):
    """
    Produces adventure listing view header.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    page_index : `int`
        The shown page's index.
    
    Yields
    ------
    part : `str`
    """
    yield '### Adventures (page '
    yield str(page_index + 1)
    yield ')'


def produce_adventure_short_representation(adventure):
    """
    Produces short representation of an adventure for adventure listing view.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    adventure : ``Adventure``
        Adventure to produce representation for.
    
    Yields
    ------
    part : `str`
    """
    yield format(unix_time_to_datetime(adventure.created_at), DATETIME_FORMAT_CODE)
    yield ' UTC '
    yield from _produce_adventure_location_for_headers(adventure)


def _produce_adventure_in_progress_state_description(adventure_state):
    """
    Produces adventure in-progress state description.
    
    Parameters
    ----------
    adventure_state : `int`
        The adventure's state.
    
    Yields
    ------
    part : `str`
    """
    if adventure_state == ADVENTURE_STATE_DEPARTING:
        next_step_description = 'departing to the location'
    
    elif adventure_state == ADVENTURE_STATE_ACTIONING:
        next_step_description = 'working on your target task'
    
    elif adventure_state == ADVENTURE_STATE_ACTIONING_CANCEL_AFTER:
        next_step_description = 'working on your target task, then will return after'
    
    elif adventure_state == ADVENTURE_STATE_CANCELLED or adventure_state == ADVENTURE_STATE_RETURNING:
        next_step_description = 'returning home'
    
    else:
        next_step_description = None
    
    if (next_step_description is not None):
        yield '\nYou are currently '
        yield next_step_description
        yield '.'


def produce_adventure_view_description(adventure, inventory_total, inventory_exhausted):
    """
    Produces adventure description.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    adventure : ``Adventure``
        Adventure to produce description for.
    
    inventory_total : `int`
        The user's total inventory.
    
    inventory_exhausted : `int`
        The user's used inventory.
    
    Yields
    ------
    part : `str`
    """
    yield 'Departed at: '
    yield format(unix_time_to_datetime(adventure.created_at), DATETIME_FORMAT_CODE)
    yield ' UTC\nUsed health: '
    yield str(adventure.health_exhausted)
    yield ' / '
    yield str(adventure.health_initial)
    yield '\nUsed energy: '
    yield str(adventure.energy_exhausted)
    yield ' / '
    yield str(adventure.energy_initial)
    
    if adventure.state == ADVENTURE_STATE_FINALISED:
        yield '\nTotal duration: '
        yield elapsed_time(RelativeDelta(
            unix_time_to_datetime(adventure.updated_at),
            unix_time_to_datetime(adventure.created_at),
        ))
        yield '\nRecovery time: '
        yield elapsed_time(RelativeDelta(seconds = recovery_duration_seconds_get(adventure)))
    
    else:
        yield '\nUsed inventory: '
        yield from produce_kilogram_ratio(inventory_exhausted, inventory_total)
        yield '\nElapsed time: '
        yield elapsed_time(RelativeDelta(
            unix_time_to_datetime(unix_time_seconds_get()),
            unix_time_to_datetime(adventure.created_at),
        ))
        
        yield from _produce_adventure_in_progress_state_description(adventure.state)


def produce_adventure_view_description_detailed_listing(adventure, inventory_total, inventory_exhausted):
    """
    Produces adventure description detailed in a listing format.
    
    This function is an iterable generator.
    
    Parameters
    -----------
    adventure : ``Adventure``
        Adventure to produce description for.
    
    inventory_total : `int`
        The user's total inventory.
    
    inventory_exhausted : `int`
        The user's used inventory.
    
    Yields
    ------
    part : `str`
    """
    yield '- Departed at\n  - '
    yield format(unix_time_to_datetime(adventure.created_at), DATETIME_FORMAT_CODE)
    yield ' UTC\n- Used health\n  - '
    yield str(adventure.health_exhausted)
    yield ' / '
    yield str(adventure.health_initial)
    yield '\n- Used energy\n  - '
    yield str(adventure.energy_exhausted)
    yield ' / '
    yield str(adventure.energy_initial)
    
    if adventure.state == ADVENTURE_STATE_FINALISED:
        yield '\n- Total duration\n  - '
        yield elapsed_time(RelativeDelta(
            unix_time_to_datetime(adventure.updated_at),
            unix_time_to_datetime(adventure.created_at),
        ))
        yield '\n- Recovery time\n  - '
        yield elapsed_time(RelativeDelta(seconds = recovery_duration_seconds_get(adventure)))
    
    else:
        yield '\n- Used inventory\n  - '
        yield from produce_kilogram_ratio(inventory_exhausted, inventory_total)
        yield '\n- Elapsed time\n  - '
        yield elapsed_time(RelativeDelta(
            unix_time_to_datetime(unix_time_seconds_get()),
            unix_time_to_datetime(adventure.created_at),
        ))
    
    yield '\n- Adventure settings\n  - Duration\n    - '
    
    yield from produce_duration_sophisticated(adventure.initial_duration_seconds)
    yield ', return '
    try:
        return_ = RETURNS[adventure.return_id]
    except KeyError:
        return_name = 'unknown'
    else:
        return_name = return_.name.lower()
    yield return_name
    
    auto_cancellation_id = adventure.auto_cancellation_id
    
    try:
        auto_cancellation = AUTO_CANCELLATIONS[auto_cancellation_id]
    except KeyError:
        pass
    else:
        yield '\n  - Auto cancellation\n'
        yield from produce_auto_cancellation_conditions_listing(auto_cancellation, '    ')
    
    goal_listing = adventure.goal_listing
    if (goal_listing is not None):
        yield '\n  - Goal\n    - '
        yield from produce_goal(goal_listing[0])
    
    if adventure.state != ADVENTURE_STATE_FINALISED:
        yield from _produce_adventure_in_progress_state_description(adventure.state)


def _produce_adventure_action_type_for_headers(adventure_action):
    """
    Helper function to produce adventure action type for headers.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    adventure_action : ``AdventureAction``
        Adventure action to produce for.
    
    Yields
    ------
    part : `str`
    """
    try:
        action = ACTIONS[adventure_action.action_id]
    except KeyError:
        action_name = ACTION_TYPE_NAME_DEFAULT
    else:
        action_name = ACTION_TYPE_TO_NAME.get(action.type, ACTION_TYPE_NAME_DEFAULT)
    
    yield action_name


def produce_adventure_action_short_representation(adventure_action):
    """
    Produces an adventure action's header.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    adventure_action : ``AdventureAction``
        Adventure action to produce header for.
    
    Yields
    ------
    part : `str`
    """
    yield format_unix_time(adventure_action.created_at, TIMESTAMP_STYLES.long_time)
    yield ' '
    yield from _produce_adventure_action_type_for_headers(adventure_action)


def produce_adventure_action_view_header(adventure_action):
    """
    Produces an adventure action's header.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    adventure_action : ``AdventureAction``
        Adventure action to produce header for.
    
    Yields
    ------
    part : `str`
    """
    yield '### Action '
    yield from _produce_adventure_action_type_for_headers(adventure_action)


def produce_adventure_action_view_description(adventure_action):
    """
    Produces an adventure action's description.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    adventure_action : ``AdventureAction``
        Adventure action to produce description for.
    
    Yields
    ------
    part : `str`
    """
    yield 'Occurred at: '
    yield format_unix_time(adventure_action.created_at, TIMESTAMP_STYLES.long_time)
    yield '\nUsed health: '
    yield str(adventure_action.health_exhausted)
    yield '\nUsed energy: '
    yield str(adventure_action.energy_exhausted)


def _item_and_amount_pair_sort_key_getter(item):
    """
    Sort key getter for item and amount pair items.
    
    Parameters
    ----------
    item : ``(Item, int)``
        Item to get sort key for.
    
    Returns
    -------
    key : `str`
    """
    return item[0].name


def produce_loot_listing(grouped_loot, loot_listing_mode):
    """
    Produces loot listing.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    grouped_loot : `dict<int, dict<int, int>>`
        Grouped loot by state.
    
    loot_listing_mode : `int`
        How to list the loot.
    
    Yields
    ------
    part : `str`
    """
    group_added = False
    
    while True:
        if loot_listing_mode != ADVENTURE_LOOT_LISTING_MODE_DEFAULT:
            if loot_listing_mode == ADVENTURE_LOOT_LISTING_MODE_TOTAL:
                titles = (
                    'Total loot',
                    'Total loot lost due to low energy',
                    'Total loot lost due to full inventory',
                )
                break
            
            if loot_listing_mode == ADVENTURE_LOOT_LISTING_MODE_THIS_STEP:
                titles = (
                    'Loot (this step)',
                    'Loot lost due to low energy (this step)',
                    'Loot lost due to full inventory (this step)',
                )
                break
            
            # No other cases:
            
        titles = (
            'Loot',
            'Loot lost due to low energy',
            'Loot lost due to full inventory',
        )
        break
    
    
    for loot_state, title in zip(
        (LOOT_STATE_SUCCESS, LOOT_STATE_LOST_DUE_LOW_ENERGY, LOOT_STATE_LOST_DUE_FULL_INVENTORY),
        titles,
    ):
        try:
            group = grouped_loot[loot_state]
        except KeyError:
            continue
        
        if group_added:
            yield '\n'
        else:
            group_added = True
        
        yield '### '
        yield title
        yield ':'
        
        for item, amount in sorted(
            ((get_item(item_id), amount) for (item_id, amount) in group.items()),
            key = _item_and_amount_pair_sort_key_getter,
        ):
            yield '\n- '
            
            emoji = item.emoji
            if (emoji is not None):
                yield emoji.as_emoji
                yield ' '
            
            yield item.name
            yield ' x'
            yield str(amount)
            yield ' ('
            yield from produce_kilogram(item.weight * amount)
            yield ')'


def produce_error_message_adventure_depart_on_recovery(recovering_until, now):
    """
    Produces adventure depart failure message for the case when the user is recovering.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    recovering_until : `DateTine`
        Until when the user is recovering.
    
    now : `DateTime`
        The current time.
    
    Yields
    ------
    part : `str`
    """
    yield 'You are currently recovering for '
    yield elapsed_time(RelativeDelta(recovering_until, now))
    yield ', until '
    yield format_datetime(recovering_until, TIMESTAMP_STYLES.long_time)
    yield '.\nYou cannot go on an adventure in the meantime.'


def produce_error_message_adventure_cannot_cancel(adventure_state, cancellation_mode):
    """
    Produces adventure cancellation error message, when the user cannot cancel it.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    adventure_state : `int`
        The adventure's state.
    
    cancellation_mode : `int`
        Cancellation mode.
    
    Yields
    ------
    part : `str`
    """
    yield 'You cannot cancel your adventure'
    
    if cancellation_mode == ADVENTURE_CANCELLATION_MODE_NOW:
        when_description = 'immediately'
    elif cancellation_mode == ADVENTURE_CANCELLATION_MODE_AFTER:
        when_description = 'after the next action'
    else:
        when_description = None
    
    if (when_description is not None):
        yield ' '
        yield when_description
    
    if adventure_state == ADVENTURE_STATE_DEPARTING:
        adventure_state_description = 'while you are departing'
    elif adventure_state == ADVENTURE_STATE_ACTIONING_CANCEL_AFTER:
        adventure_state_description = 'if it is already being cancelled after the next action'
    elif (adventure_state == ADVENTURE_STATE_CANCELLED) or (adventure_state == ADVENTURE_STATE_RETURNING):
        adventure_state_description = 'while you are returning home'
    else:
        adventure_state_description = None
    
    if (adventure_state_description is not None):
        yield ' '
        yield adventure_state_description
    
    yield '.'


def produce_error_message_adventure_duration_out_of_threshold(lower, duration, threshold):
    """
    Produces adventure depart error message, when the given duration is out of the expected range.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    lower : `bool`
        Whether it is the lower threshold the duration is out of.
    
    duration : `int`
        Give duration.
    
    threshold : `int`
        Threshold.
    
    Yields
    ------
    part : `str`
    """
    yield 'Duration '
    yield ('under lower' if lower else 'over upper')
    yield ' threshold: '
    yield from produce_duration_sophisticated(duration)
    yield ' '
    yield ('<' if lower else '>')
    yield ' '
    yield from produce_duration_sophisticated(threshold)
    yield '.'


def produce_butcher_item_description(item, loot_chance_and_amount, energy_cost):
    """
    Produces butcher item description.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    item : ``Item``
        Item to butcher.
    
    loot_chance_and_amount : `None | list<(int, float, int)>`
        Loot chances and amounts.
    
    energy_cost : `int`
        Upper energy cost.
    
    Yields
    ------
    part : `str`
    """
    yield '### Butcher '
    emoji = item.emoji
    if (emoji is not None):
        yield emoji.as_emoji
        yield ' '
    
    yield item.name
    
    yield ' costing up to '
    yield str(energy_cost)
    yield ' energy, for:'
    
    if (loot_chance_and_amount is None):
        yield ' *none*'
    else:
        for item_id, chance, amount in loot_chance_and_amount:
            item = get_item(item_id)
            yield '\n- '
            
            yield str(round(chance * 100.0))
            yield '% chance of '
            
            yield str(amount)
            yield ' '
            
            emoji = item.emoji
            if (emoji is not None):
                yield emoji.as_emoji
                yield ' '
            
            yield item.name


def _produce_butcher_amounts_and_cost(butcher_amounts, energy_cost):
    """
    Produces butcher description.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    butcher_amounts : `list(int, int)>`
        Butchered amounts.
    
    energy_cost : `int`
        The used energy.
    
    Yields
    ------
    part : `str`
    """
    yield 'Used energy: '
    yield str(energy_cost)
    yield '\nButchered:'
    
    if (butcher_amounts is None):
        yield ' *none*'
    else:
        for item_id, amount in butcher_amounts:
            item = get_item(item_id)
            yield '\n- '
            yield str(amount)
            yield ' '
            
            emoji = item.emoji
            if (emoji is not None):
                yield emoji.as_emoji
                yield ' '
            
            yield item.name
    

def produce_butcher_done_description(butcher_amounts, energy_cost):
    """
    Produces butcher done description.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    butcher_amounts : `list(int, int)>`
        Butchered amounts.
    
    energy_cost : `int`
        The used energy.
    
    Yields
    ------
    part : `str`
    """
    yield '### Total\n'
    yield from _produce_butcher_amounts_and_cost(butcher_amounts, energy_cost)


def produce_butcher_step_description(butchered_item, butcher_amounts, energy_cost):
    """
    Produces butcher done description.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    butchered_item : ``Item``
        The butchered item.
    
    butcher_amounts : `list(int, int)>`
        Butchered amounts.
    
    energy_cost : `int`
        The used energy.
    
    Yields
    ------
    part : `str`
    """
    yield '### Butchered '
    
    emoji = butchered_item.emoji
    if (emoji is not None):
        yield emoji.as_emoji
        yield ' '
    
    yield butchered_item.name
    yield '\n'
    
    yield from _produce_butcher_amounts_and_cost(butcher_amounts, energy_cost)


def produce_butcher_recovering_until_footer(now, recovering_until):
    """
    Produces butcher recovering until footer.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    now : `DateTime`
        The current date time.
    
    recovering_until : `DateTime`
        Until when the user is recovering for.
    
    Yields
    ------
    part : `str`
    """
    yield 'You are recovering for '
    yield elapsed_time(RelativeDelta(recovering_until, now))
    yield ', until '
    yield format_datetime(recovering_until, TIMESTAMP_STYLES.long_time)
    yield '.'
