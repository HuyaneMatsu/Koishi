__all__ = ()

from base64 import b64decode as base_64_decode
from datetime import datetime as DateTime, timedelta as TimeDelta, timezone as TimeZone
from math import inf, isnan as is_nan

from hata import Client, InteractionType

from ...bots import FEATURE_CLIENTS

from ..adventure_core import (
    ACTION_TYPE_BUTCHERING, ADVENTURE_STATE_FINALISED, AUTO_CANCELLATIONS, AUTO_CANCELLATIONS_ALLOWED,
    AUTO_CANCELLATION_ID_DEFAULT, Adventure, DURATION_MAX, DURATION_MIN, DURATION_SUGGESTION_SETS, GOAL_TYPE_ITEM_EXACT,
    LOCATIONS, RETURNS, RETURNS_ALLOWED, RETURN_ID_AFTER, TARGETS, adventure_cancel_after, adventure_cancel_now,
    adventure_create, adventure_get, adventure_get_active, adventure_listing_get_page, adventure_save,
    can_cancel_adventure_after, can_cancel_adventure_any, can_cancel_adventure_now, get_action_type_multiplier,
    goal_create_item_exact, goal_deserialise, recovery_duration_seconds_get_of_energy_cost, scheduled_adventure_arrival
)
from ..inventory_core import create_item_suggestions, get_inventory, save_inventory, select_item
from ..item_core import (
    ITEM_FLAG_BUTCHERABLE, butcher_calculate_done, butcher_calculate_step, butcher_done_append, get_item,
    get_item_nullable
)
from ..quest_core import get_user_adventurer_rank_info
from ..seeding import create_seed
from ..unit_core import AMOUNT_TYPE_COUNT, AMOUNT_TYPE_VALUE, AMOUNT_TYPE_WEIGHT, parse_duration, produce_duration
from ..user_stats_core import (
    user_stats_calculate, user_stats_get, user_stats_save, user_stats_set_recovering_until,
    user_stats_set_recovering_until_notification_at
)

from .component_building import (
    build_adventure_action_listing_view_components, build_adventure_action_view_components,
    build_adventure_cancellation_components, build_adventure_cancellation_confirmation_form,
    build_adventure_create_confirm_components, build_adventure_create_confirmation_form,
    build_adventure_listing_view_components, build_adventure_view_components, build_butcher_components
)
from .constants import (
    ADVENTURE_CANCELLATION_MODE_AFTER, ADVENTURE_CANCELLATION_MODE_NONE, ADVENTURE_CANCELLATION_MODE_NOW,
    ADVENTURE_LISTING_PAGE_SIZE, ADVENTURE_VIEW_MODE_DEFAULT, ERROR_MESSAGE_ADVENTURE_DEPART_ALREADY_ON_ADVENTURE,
    ERROR_MESSAGE_ADVENTURE_DEPART_INVENTORY_OVERLOADED, ERROR_MESSAGE_ADVENTURE_NOT_ON_ADVENTURE,
    ERROR_MESSAGE_ADVENTURE_RECONSTRUCT_FAILURE, ERROR_MESSAGE_ADVENTURE_UNKNOWN_ADVENTURE, FLOAT_STRUCT
)
from .content_building import (
    produce_error_message_adventure_cannot_cancel, produce_error_message_adventure_depart_on_recovery,
    produce_error_message_adventure_duration_out_of_threshold
)
from .custom_ids import (
    CUSTOM_ID_ADVENTURE_ACTION_BATTLE_LOGS_PATTERN, CUSTOM_ID_ADVENTURE_ACTION_LISTING_VIEW_PATTERN,
    CUSTOM_ID_ADVENTURE_ACTION_VIEW_DEPART, CUSTOM_ID_ADVENTURE_ACTION_VIEW_PATTERN,
    CUSTOM_ID_ADVENTURE_ACTION_VIEW_RETURN, CUSTOM_ID_ADVENTURE_BUTCHER_CONTINUOUS_PATTERN,
    CUSTOM_ID_ADVENTURE_BUTCHER_DISABLED_PATTERN, CUSTOM_ID_ADVENTURE_BUTCHER_INITIAL_PATTERN,
    CUSTOM_ID_ADVENTURE_CANCELLATION_MODE, CUSTOM_ID_ADVENTURE_CANCEL_PATTERN,
    CUSTOM_ID_ADVENTURE_CREATE_CONFIRM_PATTERN, CUSTOM_ID_ADVENTURE_LISTING_VIEW_PATTERN,
    CUSTOM_ID_ADVENTURE_VIEW_PATTERN
)
from .duration_suggesting import get_duration_suggestions
from .goal_item_suggesting import get_best_matching_goal_item, get_goal_item_suggestions
from .location_suggesting import get_best_matching_location, get_location_suggestions
from .target_suggesting import get_best_matching_target, get_target_suggestions

from config import MARISA_MODE


try:
    from ..adventure_recovery_over_reminder_hook import set_closest_adventure_recovery_over_reminder
except ImportError:
    if not MARISA_MODE:
        raise
    
    async def set_closest_adventure_recovery_over_reminder(user_id, date_time):
        return


ADVENTURE_COMMANDS = FEATURE_CLIENTS.interactions(
    None,
    integration_types = ['guild_install', 'user_install'],
    is_global = True,
    name = 'adventure',
)


@ADVENTURE_COMMANDS.interactions
async def depart(
    client,
    interaction_event,
    location_name : (str, 'Where are you going to depart?', 'location'),
    target_name : (str, 'What to do at the location.', 'target'),
    duration_string : (str, 'How long you want to go out for?', 'duration'),
    return_id_hexadecimal : (
        [(return_.name, format(return_.id, 'x')) for return_ in RETURNS_ALLOWED],
        'How do you want to arrive back?',
        'return',
    ) = None,
    auto_cancellation_id_hexadecimal : (
        [(auto_cancellation.name, format(auto_cancellation.id, 'x')) for auto_cancellation in AUTO_CANCELLATIONS_ALLOWED],
        'Do you want to arrive back if full or low on energy / health?',
        'auto-cancellation',
    ) = None,
    goal_type_hexadecimal : (
        [
            ('Item (exact)', format(GOAL_TYPE_ITEM_EXACT, 'x')),
        ],
        'The adventure\'s goal\'s type.',
        'goal-type',
    ) = None,
    goal_item_name : (
        str,
        'Target item of the goal.',
        'goal-item',
    ) = None,
    goal_amount_type_hexadecimal : (
        [
            ('count', format(AMOUNT_TYPE_COUNT, 'x')),
            ('weight (kg)', format(AMOUNT_TYPE_WEIGHT, 'x')),
            ('value', format(AMOUNT_TYPE_VALUE, 'x')),
        ],
        'The unit of the goal.',
        'goal-unit',
    ) = None,
    goal_amount_required : (
        'expression',
        'The required amount of the goal.',
        'goal-amount-required',
    ) = None,
):
    """
    Depart to an adventure!
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    location_name : `str`
        Depart location's name.
    
    target_name : `str`
        Targeted action's name set at the location.
    
    duration_string : `str`
        The duration  to depart to in string.
    
    return_id_hexadecimal : `str` = `None`, Optional
        The return_ logic's identifier in hexadecimal.
    
    auto_cancellation_id_hexadecimal : `None | str` = `None`, Optional
        The auto-cancellation logic's identifier in hexadecimal.
    
    goal_type_hexadecimal : `None | str` = `None`, Optional
        The adventure's goal's type's identifier as hexadecimal.
    
    goal_item_name : `None | str` = `None`, Optional
        The goal's item's name.
    
    goal_amount_type_hexadecimal : `None | str` = `None`, Optional
        The goal's amount type's identifier as hexadecimal.
    
    goal_amount_required : `None | str` = `None`, Optional
        The goal's required amount.
    """
    while True:
        adventure = await adventure_get_active(interaction_event.user_id)
        if (adventure is not None):
            error_message = ERROR_MESSAGE_ADVENTURE_DEPART_ALREADY_ON_ADVENTURE
            break
        
        user_stats = await user_stats_get(interaction_event.user_id)
        recovering_until = user_stats.recovering_until
        now = DateTime.now(TimeZone.utc)
        if (recovering_until is not None) and (recovering_until > now):
            error_message = ''.join([*produce_error_message_adventure_depart_on_recovery(recovering_until, now)])
            break
        
        # Check whether the inventory weight is greater than the available.
        inventory = await get_inventory(interaction_event.user_id)
        if inventory.weight > user_stats_calculate(user_stats).extra_inventory:
            error_message = ERROR_MESSAGE_ADVENTURE_DEPART_INVENTORY_OVERLOADED
            break
        
         
        location = get_best_matching_location(
            location_name,
            get_user_adventurer_rank_info(user_stats.credibility).level,
        )
        if location is None:
            error_message = f'Unknown location: {location_name}.'
            break    
        
        target = get_best_matching_target(location.target_ids, target_name)
        if target is None:
            error_message = f'Unknown target: {target_name}.'
            break
        
        duration = parse_duration(duration_string)
        if not duration:
            error_message = f'No or unrecognized duration: {duration_string}.'
            break
        
        if duration < DURATION_MIN:
            error_message = ''.join([*produce_error_message_adventure_duration_out_of_threshold(
                True, duration, DURATION_MIN
            )])
            break
        
        if duration > DURATION_MAX:
            error_message = ''.join([*produce_error_message_adventure_duration_out_of_threshold(
                False, duration, DURATION_MAX
            )])
            break
        
        # Use goto
        while True:
            if return_id_hexadecimal is None:
                return_id = RETURN_ID_AFTER
            else:
                try:
                    return_id = int(return_id_hexadecimal, base = 16)
                except ValueError:
                    return_ = None
                    break
            
            return_ = RETURNS.get(return_id, None)
            break
        
        if return_ is None:
            error_message = f'Unknown return: {return_id_hexadecimal}.'
            break
        
        # Use goto
        while True:
            if auto_cancellation_id_hexadecimal is None:
                auto_cancellation_id = AUTO_CANCELLATION_ID_DEFAULT
            else:
                try:
                    auto_cancellation_id = int(auto_cancellation_id_hexadecimal, base = 16)
                except ValueError:
                    auto_cancellation = None
                    break
            
            auto_cancellation = AUTO_CANCELLATIONS.get(auto_cancellation_id, None)
            break
        
        if auto_cancellation is None:
            error_message = f'Unknown auto-cancellation: {auto_cancellation_id_hexadecimal}.'
            break
        
        # Validate goal
        if (goal_type_hexadecimal is None):
            goal = None
        
        else:
            try:
                goal_type = int(goal_type_hexadecimal, 16)
            except ValueError:
                error_message = f'Not recognised goal type: {goal_type_hexadecimal!r}'
                break
            
            if goal_type == GOAL_TYPE_ITEM_EXACT:
                if (goal_item_name is None) or (goal_amount_type_hexadecimal is None) or (goal_amount_required is None):
                    error_message = (
                        'If `goal-type` is `Item (exact)`, then `goal-item`, `goal-unit` and `oal-amount-required` '
                        'are also all required.'
                    )
                    break
                
                goal_item = get_best_matching_goal_item(target.action_ids, goal_item_name)
                if (goal_item is None):
                    error_message = f'Not recognised goal item: {goal_item_name!r}' 
                    break
                
                try:
                    goal_amount_type = int(goal_amount_type_hexadecimal, 16)
                except KeyError:
                    error_message = f'Not recognised goal unit type: {goal_amount_type_hexadecimal!r}'
                    break
                
                if(
                    (goal_amount_type != AMOUNT_TYPE_COUNT) and
                    (goal_amount_type != AMOUNT_TYPE_WEIGHT) and
                    (goal_amount_type != AMOUNT_TYPE_VALUE)
                ):
                    error_message = f'Not recognised goal unit type: {goal_amount_type_hexadecimal!r}'
                    break
                
                if isinstance(goal_amount_required, float):
                    if is_nan(goal_amount_required):
                        error_message = f'`goal-amount-required` must be a number; got {goal_amount_required!r}'
                        break
                    
                    if (goal_amount_required == - inf) or (goal_amount_required == inf):
                        error_message = f'`goal-amount-required` Cannot be infinity, got {goal_amount_required!r}'
                        break
                    
                    if (goal_amount_type == AMOUNT_TYPE_WEIGHT):
                        goal_amount_required *= 1000.0
                    
                    goal_amount_required = int(goal_amount_required)
                
                else:
                    if (goal_amount_type == AMOUNT_TYPE_WEIGHT):
                        goal_amount_required *= 1000
                
                if goal_amount_required <= 0:
                    error_message = f'`goal-amount-required` cannot be non-positive, got {goal_amount_required!r}'
                    break
                
                goal = goal_create_item_exact(goal_item.id, goal_amount_type, goal_amount_required)
            
            else:
                # No other goal types are available currently.
                error_message = f'Not recognised goal type: {goal_type!r}'
                break
        
        await client.interaction_form_send(
            interaction_event,
            build_adventure_create_confirmation_form(
                interaction_event.user_id, location, target, duration, return_, auto_cancellation, goal
            ),
        )
        return
    
    await client.interaction_response_message_create(
        interaction_event,
        allowed_mentions = None,
        content = error_message,
        show_for_invoking_user_only = True
    )


@depart.autocomplete('location')
async def autocomplete_depart_location(interaction_event, location_name):
    """
    Auto completes depart location.
    
    This function is a coroutine.
    
    Parameters
    ----------
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    location_name : `None | str`
        The value to autocomplete.
    
    Returns
    -------
    suggestions : `list<(str, str)>`
    """
    user_stats = await user_stats_get(interaction_event.user_id)
    return get_location_suggestions(
        location_name,
        get_user_adventurer_rank_info(user_stats.credibility).level,
    )


@depart.autocomplete('target')
async def autocomplete_depart_target(interaction_event, target_name):
    """
    Auto completes depart target.
    
    This function is a coroutine.
    
    Parameters
    ----------
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    target_name : `None | str`
        The target name to autocomplete.
    
    Returns
    -------
    suggestions : `None | list<(str, str)>`
    """
    location_name = interaction_event.get_value_of('depart', 'location')
    if location_name is None:
        return
    
    user_stats = await user_stats_get(interaction_event.user_id)
    location = get_best_matching_location(
        location_name,
        get_user_adventurer_rank_info(user_stats.credibility).level,
    )
    if location is None:
        return
    
    return get_target_suggestions(location.target_ids, target_name)


@depart.autocomplete('duration')
async def autocomplete_depart_duration(interaction_event, duration_string):
    """
    Auto completes depart duration.
    
    This function is a coroutine.
    
    Parameters
    ----------
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    duration_string : `None | str`
        Duration string to auto complete.
    
    Returns
    -------
    suggestions : `None | list<(str, str)>`
    """
    if (duration_string is not None):
        duration = parse_duration(duration_string)
        if duration:
            duration_string = ''.join([*produce_duration(duration)])
            return [
                (duration_string, duration_string),
            ]
    
    location_name = interaction_event.get_value_of('depart', 'location')
    if location_name is None:
        return
    
    user_stats = await user_stats_get(interaction_event.user_id)
    location = get_best_matching_location(
        location_name,
        get_user_adventurer_rank_info(user_stats.credibility).level,
    )
    if location is None:
        return
    
    target_name = interaction_event.get_value_of('depart', 'target')
    target = get_best_matching_target(location.target_ids, target_name)
    if target is None:
        return
    
    duration_suggestion_set = DURATION_SUGGESTION_SETS.get(target.duration_suggestion_set_id, None)
    if duration_suggestion_set is None:
        return
    
    return get_duration_suggestions(duration_suggestion_set.durations, duration_string)


@depart.autocomplete('goal-item')
async def autocomplete_depart_goal_item(interaction_event, goal_item_string):
    """
    Auto completes depart goal item.
    
    This function is a coroutine.
    
    Parameters
    ----------
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    goal_item_string : `None | str`
        Goal item string to auto complete.
    
    Returns
    -------
    suggestions : `None | list<(str, str)>`
    """
    location_name = interaction_event.get_value_of('depart', 'location')
    if location_name is None:
        return
    
    user_stats = await user_stats_get(interaction_event.user_id)
    location = get_best_matching_location(
        location_name,
        get_user_adventurer_rank_info(user_stats.credibility).level,
    )
    if location is None:
        return
    
    target_name = interaction_event.get_value_of('depart', 'target')
    target = get_best_matching_target(location.target_ids, target_name)
    if target is None:
        return
    
    return get_goal_item_suggestions(target.action_ids, goal_item_string)


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_ADVENTURE_CREATE_CONFIRM_PATTERN, target = 'form')
async def handle_adventure_create_confirm(
    client,
    interaction_event,
    user_id,
    location_id,
    target_id,
    duration,
    return_id,
    auto_cancellation_id,
    goal_data_base_64,
):
    """
    Handles an adventure create confirm interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received this interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction.
    
    user_id : `str`
        The invoking user's identifier in hexadecimal. Later converted to int.
    
    location_id : `str`
        The selected location's identifier in hexadecimal. Later converted to int.
    
    target_id : `str`
        The selected target's identifier in hexadecimal. Later converted to int.
    
    duration : `str`
        The duration in hexadecimal. Later converted to int.
    
    return_id : `str`
        The selected return_'s identifier in hexadecimal. Later converted to int.
    
    auto_cancellation_id : `str`
        The selected auto-cancellation's identifier in hexadecimal. Later converted to int.
    
    goal_data_base_64 : `None | str`
        Serialised goal encoded as 64.
    """
    user_id = int(user_id, 16)
    location_id = int(location_id, 16)
    target_id = int(target_id, 16)
    duration = int(duration, 16)
    return_id = int(return_id, 16)
    auto_cancellation_id = int(auto_cancellation_id, 16)
    
    
    await client.interaction_application_command_acknowledge(
        interaction_event,
        False,
        show_for_invoking_user_only = True,
    )
    
    # Leave if the invoking user is different.
    if user_id != interaction_event.user_id:
        return
    
    while True:
        try:
            location = LOCATIONS[location_id]
            target = TARGETS[target_id]
            return_ = RETURNS[return_id]
            auto_cancellation = AUTO_CANCELLATIONS[auto_cancellation_id]
        except KeyError:
            error_message = ERROR_MESSAGE_ADVENTURE_RECONSTRUCT_FAILURE
            break
        
        if goal_data_base_64 is None:
            goal = None
        else:
            try:
                goal_data = base_64_decode(goal_data_base_64)
            except ValueError:
                error_message = ERROR_MESSAGE_ADVENTURE_RECONSTRUCT_FAILURE
                break
                
            goal = goal_deserialise(goal_data)
            if goal is None:
                error_message = ERROR_MESSAGE_ADVENTURE_RECONSTRUCT_FAILURE
                break
        
        user_stats = await user_stats_get(user_id)
        recovering_until = user_stats.recovering_until
        if (recovering_until is not None):
            if (recovering_until > DateTime.now(TimeZone.utc)):
                error_message = 'You are currently recovering, cannot go on an adventure.'
                break
            
            # If we are not recovering currently, set recovery until to `None`,
            # so when notifying, we know that we know that we should not be do it anymore.
            user_stats_set_recovering_until_notification_at(user_stats, None)
            await user_stats_save(user_stats)
        
        user_stats_calculated = user_stats_calculate(user_stats)
        
        # Check whether the inventory weight is greater than the available.
        inventory = await get_inventory(interaction_event.user_id)
        if inventory.weight > user_stats_calculated.extra_inventory:
            error_message = ERROR_MESSAGE_ADVENTURE_DEPART_INVENTORY_OVERLOADED
            break
        
        adventure = await adventure_get_active(user_id)
        if (adventure is not None):
            error_message = ERROR_MESSAGE_ADVENTURE_DEPART_ALREADY_ON_ADVENTURE
            break
        
        adventure = adventure_create(
            user_id,
            
            location_id,
            target_id,
            return_id,
            auto_cancellation_id,
            (None if goal is None else [goal]),
            
            duration,
            user_stats_calculated.extra_health,
            user_stats_calculated.extra_energy,
        )
        await adventure_save(adventure)
        await scheduled_adventure_arrival(adventure)
        
        # Respond
        await client.interaction_response_message_edit(interaction_event, '-# _ _ ')
        await client.interaction_response_message_delete(interaction_event)
        
        await client.interaction_followup_message_create(
            interaction_event,
            components = build_adventure_create_confirm_components(
                interaction_event.user_id,
                adventure.entry_id,
                location,
                target,
                duration,
                return_,
                auto_cancellation,
                goal
            ),
        )
        return
    
    await client.interaction_response_message_edit(
        interaction_event,
        content = error_message,
        allowed_mentions = None,
    )


@ADVENTURE_COMMANDS.interactions
async def cancel(
    client,
    interaction_event,
):
    """
    Cancels the active adventure.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    """
    while True:
        adventure = await adventure_get_active(interaction_event.user_id)
        if (adventure is None):
            error_message = ERROR_MESSAGE_ADVENTURE_NOT_ON_ADVENTURE
            break
        
        if not can_cancel_adventure_any(adventure):
            error_message = ''.join([*produce_error_message_adventure_cannot_cancel(
                adventure.state, ADVENTURE_CANCELLATION_MODE_NONE
            )])
            break
        
        await client.interaction_form_send(
            interaction_event,
            build_adventure_cancellation_confirmation_form(adventure),
        )
        return
    
    await client.interaction_response_message_create(
        interaction_event,
        content = error_message,
        allowed_mentions = None,
    )


async def _build_adventure_components_common(
    adventure, adventure_view_mode, allow_switching_to_adventure_listing_view, adventure_listing_page_index
):
    """
    Generic function to build adventure components.
    
    This function is a coroutine.
    
    Parameters
    ----------
    adventure : ``Adventure``
        Adventure to build components for.
    
    adventure_view_mode : `int`
        How to render the adventure.
    
    allow_switching_to_adventure_listing_view : `bool`
        Whether switching to adventure listing is allowed from adventure view.
    
    adventure_listing_page_index : `int`
        Adventure listing page index to direct to from adventure view.
    
    Returns
    -------
    components : ``list<Component>``
    """
    if adventure.state == ADVENTURE_STATE_FINALISED:
        inventory_total = 0
        inventory_exhausted = 0
    else:
        user_stats = await user_stats_get(adventure.user_id)
        inventory = await get_inventory(adventure.user_id)
        
        inventory_total = user_stats_calculate(user_stats).extra_inventory
        inventory_exhausted = inventory.weight
    
    return build_adventure_view_components(
        adventure,
        adventure_view_mode,
        allow_switching_to_adventure_listing_view,
        adventure_listing_page_index,
        inventory_total,
        inventory_exhausted,
    )
    
    return components


ADVENTURE_VIEW_OPTION_CURRENT = 1 << 0
ADVENTURE_VIEW_OPTION_PREVIOUS = 1 << 1
ADVENTURE_VIEW_OPTION_CURRENT_OR_PREVIOUS = ADVENTURE_VIEW_OPTION_CURRENT | ADVENTURE_VIEW_OPTION_PREVIOUS


@ADVENTURE_COMMANDS.interactions
async def view(
    client,
    interaction_event,
    option : (
        [
            ('current', format(ADVENTURE_VIEW_OPTION_CURRENT, 'x')),
            ('previous', format(ADVENTURE_VIEW_OPTION_PREVIOUS, 'x')),
            ('current or previous', format(ADVENTURE_VIEW_OPTION_CURRENT_OR_PREVIOUS, 'x')),
        ],
        'Current or previous?',
    ) = None,
):
    """
    View your current adventure and its progress.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    option : `None | str` = `None`, Optional
        Which quest to show as a string representing a hexadecimal integer.
    """
    if option is None:
        option = ADVENTURE_VIEW_OPTION_CURRENT_OR_PREVIOUS
    else:
        try:
            option = int(option, 16)
        except ValueError:
            option = ADVENTURE_VIEW_OPTION_CURRENT_OR_PREVIOUS
    
    await client.interaction_application_command_acknowledge(
        interaction_event,
        False,
        show_for_invoking_user_only = True
    )
    
    while True:
        error_message = None
        
        while True:
            if (option & ADVENTURE_VIEW_OPTION_CURRENT):
                adventure = await adventure_get_active(interaction_event.user_id)
                if (adventure is not None):
                    break
                
                if (option == ADVENTURE_VIEW_OPTION_CURRENT):
                    error_message = ERROR_MESSAGE_ADVENTURE_NOT_ON_ADVENTURE
                    break
            
            if (option & ADVENTURE_VIEW_OPTION_PREVIOUS):
                active_adventure = await adventure_get_active(interaction_event.user_id)
                page_size = 1 + (active_adventure is not None)
                page_count, adventure_listing = await adventure_listing_get_page(
                    interaction_event.user_id, -1, page_size
                )
                if (adventure_listing is not None) and (len(adventure_listing) == page_size):
                    adventure = adventure_listing[0]
                    break
                
                if (option == ADVENTURE_VIEW_OPTION_PREVIOUS):
                    error_message = 'You were not on an adventure.'
                    break
            
            error_message = 'You are not on adventure and never were.'
            break
        
        if (error_message is not None):
            break
        
        components = await _build_adventure_components_common(adventure, ADVENTURE_VIEW_MODE_DEFAULT, False, 0)
        
        await client.interaction_response_message_edit(interaction_event, '-# _ _ ')
        await client.interaction_response_message_delete(interaction_event)
        
        await client.interaction_followup_message_create(
            interaction_event,
            components = components,
        )
        return
    
    await client.interaction_response_message_edit(
        interaction_event,
        content = error_message,
        allowed_mentions = None,
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_ADVENTURE_CANCEL_PATTERN)
async def handle_active_adventure_cancellation_invoke(
    client,
    interaction_event,
    user_id,
    adventure_entry_id,
):
    """
    Handles an active adventure cancellation.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        The owner user's identifier as hexadecimal. Later converted back to integer.
    
    adventure_entry_id : `str`
        The adventure's entry's identifier as hexadecimal. Later converted back to integer.
    """
    user_id = int(user_id, 16)
    adventure_entry_id = int(adventure_entry_id, 16)
    
    
    if interaction_event.user_id != user_id:
        return
    
    while True:
        adventure = await adventure_get(adventure_entry_id)
        if (adventure is None):
            error_message = ERROR_MESSAGE_ADVENTURE_UNKNOWN_ADVENTURE
            break
        
        if not can_cancel_adventure_any(adventure):
            error_message = ''.join([*produce_error_message_adventure_cannot_cancel(
                adventure.state, ADVENTURE_CANCELLATION_MODE_NONE
            )])
            break
        
        await client.interaction_form_send(
            interaction_event,
            build_adventure_cancellation_confirmation_form(adventure),
        )
        return
    
    await client.interaction_component_acknowledge(
        interaction_event,
    )
    await client.interaction_followup_message_create(
        interaction_event,
        content = error_message,
        allowed_mentions = None,
        show_for_invoking_user_only = True,
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_ADVENTURE_CANCEL_PATTERN, target = 'form')
async def handle_active_adventure_cancellation_confirmation(
    client,
    interaction_event,
    user_id,
    adventure_entry_id,
    *,
    cancellation_mode : CUSTOM_ID_ADVENTURE_CANCELLATION_MODE = None,
):
    """
    Handles an active adventure cancellation confirmation.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        The owner user's identifier as hexadecimal. Later converted back to integer.
    
    adventure_entry_id : `str`
        The adventure's entry's identifier as hexadecimal. Later converted back to integer.
    
    cancellation_mode : `None | str`
        Adventure cancellation mode as hexadecimal. Later converted back to integer.
    """
    try:
        user_id = int(user_id, 16)
        adventure_entry_id = int(adventure_entry_id, 16)
    except ValueError:
        return
    
    # If `cancellation_mode` is `None`, means we select the first available cancellation method,
    # else we use the selected one.
    if cancellation_mode is None:
        cancellation_mode = ADVENTURE_CANCELLATION_MODE_NONE
    else:
        try:
            cancellation_mode = int(cancellation_mode[0], 16)
        except ValueError:
            return
        
        if (
            (cancellation_mode != ADVENTURE_CANCELLATION_MODE_NOW) and
            (cancellation_mode != ADVENTURE_CANCELLATION_MODE_AFTER)
        ):
            return
    
    
    if interaction_event.type is InteractionType.application_command:
        function = Client.interaction_application_command_acknowledge
    else:
        function = Client.interaction_component_acknowledge
    await function(client, interaction_event, False)
    
    if interaction_event.user_id != user_id:
        return
    
    while True:
        adventure = await adventure_get(adventure_entry_id)
        if (adventure is None):
            error_message = ERROR_MESSAGE_ADVENTURE_UNKNOWN_ADVENTURE
            break
        
        while True:
            if cancellation_mode == ADVENTURE_CANCELLATION_MODE_NOW:
                can_cancel = can_cancel_adventure_now(adventure)
                break
            
            if cancellation_mode == ADVENTURE_CANCELLATION_MODE_AFTER:
                can_cancel = can_cancel_adventure_after(adventure)
                break
            
            # No cancellation mode specified, prefer the one with stricter condition.
            if can_cancel_adventure_after(adventure):
                cancellation_mode = ADVENTURE_CANCELLATION_MODE_AFTER
                can_cancel = True
                break
            
            if can_cancel_adventure_now(adventure):
                cancellation_mode = ADVENTURE_CANCELLATION_MODE_NOW
                can_cancel = True
                break
            
            can_cancel = False
            break
        
        if not can_cancel:
            error_message = ''.join([*produce_error_message_adventure_cannot_cancel(
                adventure.state, cancellation_mode
            )])
            break
        
        if cancellation_mode == ADVENTURE_CANCELLATION_MODE_NOW:
            await adventure_cancel_now(adventure)
        else:
            await adventure_cancel_after(adventure)
        
        if interaction_event.type is InteractionType.application_command:
            await client.interaction_response_message_edit(interaction_event, '-# _ _')
            await client.interaction_response_message_delete(interaction_event)
        
        await client.interaction_followup_message_create(
            interaction_event,
            components = build_adventure_cancellation_components(cancellation_mode),
        )
        return
    
    if interaction_event.type is InteractionType.application_command:
        function = Client.interaction_response_message_edit
    else:
        function = Client.interaction_followup_message_create
    await function(
        client,
        interaction_event,
        content = error_message,
        allowed_mentions = None,
        show_for_invoking_user_only = True,
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_ADVENTURE_VIEW_PATTERN)
async def handle_adventure_view(
    client,
    interaction_event,
    user_id,
    adventure_entry_id,
    adventure_view_mode,
    allow_switching_to_adventure_listing_view,
    adventure_listing_page_index,
):
    """
    Handles an adventure view. This is also used for refreshing.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        The owner user's identifier as hexadecimal. Later converted back to integer.
    
    adventure_entry_id : `str`
        The adventure's entry's identifier as hexadecimal. Later converted back to integer.
    
    adventure_view_mode : `str`
        How to render the adventure as hexadecimal.
    
    allow_switching_to_adventure_listing_view : `str`
        Whether switching to adventure listing is allowed from adventure view as hexadecimal.
    
    adventure_listing_page_index : `str`
        Adventure listing page index to direct to from adventure view as hexadecimal.
        Later converted to integer.
    """
    try:
        user_id = int(user_id, 16)
        adventure_entry_id = int(adventure_entry_id, 16)
        adventure_view_mode = int(adventure_view_mode, 16)
        allow_switching_to_adventure_listing_view = True if int(allow_switching_to_adventure_listing_view, 16) else False
        adventure_listing_page_index = int(adventure_listing_page_index, 16)
    except ValueError:
        return
    
    await client.interaction_component_acknowledge(
        interaction_event,
        False,
    )
    
    if interaction_event.user_id != user_id:
        return
    
    while True:
        adventure = await adventure_get(adventure_entry_id)
        if (adventure is None):
            error_message = ERROR_MESSAGE_ADVENTURE_UNKNOWN_ADVENTURE
            break
        
        components = await _build_adventure_components_common(
            adventure, adventure_view_mode, allow_switching_to_adventure_listing_view, adventure_listing_page_index
        )
        
        await client.interaction_response_message_edit(
            interaction_event,
            components = components,
        )
        return
    
    await client.interaction_followup_message_create(
        interaction_event,
        content = error_message,
        allowed_mentions = None,
        show_for_invoking_user_only = True,
    )


@FEATURE_CLIENTS.interactions(
    custom_id = [
        CUSTOM_ID_ADVENTURE_ACTION_VIEW_DEPART,
        CUSTOM_ID_ADVENTURE_ACTION_VIEW_RETURN,
        CUSTOM_ID_ADVENTURE_BUTCHER_DISABLED_PATTERN,
    ],
)
async def handle_adventure_action_disabled():
    """
    Dummy handler for disabled adventure action views.
    
    This function is a coroutine.
    """


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_ADVENTURE_ACTION_VIEW_PATTERN)
async def handle_adventure_action_view(
    client,
    interaction_event,
    user_id,
    adventure_entry_id,
    adventure_action_index,
    adventure_view_mode,
    allow_switching_to_adventure_listing_view,
    adventure_listing_page_index,
    allow_switching_to_adventure_action_listing_view,
    adventure_action_listing_page_index,
):
    """
    Shows the selected adventure action.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        The owner user's identifier as hexadecimal. Later converted back to integer.
    
    adventure_entry_id : `str`
        The adventure's entry's identifier as hexadecimal. Later converted back to integer.
    
    adventure_action_index : `str`
        The adventure's action's index as hexadecimal. Later converted back to integer.
    
    adventure_view_mode : `str`
        How to render the adventure as hexadecimal.
    
    allow_switching_to_adventure_listing_view : `str`
        Whether switching to adventure listing is allowed from adventure view as hexadecimal.
    
    adventure_listing_page_index : `str`
        Adventure listing page index to direct to from adventure view as hexadecimal.
        Later converted to integer.
    
    allow_switching_to_adventure_action_listing_view : `str`
        Whether switching to action listing view is allowed from a action view as hexadecimal.
        Later converted back to boolean.
    
    adventure_action_listing_page_index : `str`
        adventure action listing age index to direct to from action view as hexadecimal.
    """
    try:
        user_id = int(user_id, 16)
        adventure_entry_id = int(adventure_entry_id, 16)
        adventure_action_index = int(adventure_action_index, 16)
        adventure_view_mode = int(adventure_view_mode, 16)
        allow_switching_to_adventure_listing_view = True if int(allow_switching_to_adventure_listing_view, 16) else False
        adventure_listing_page_index = int(adventure_listing_page_index, 16)
        allow_switching_to_adventure_action_listing_view = True if int(allow_switching_to_adventure_action_listing_view, 16) else False
        adventure_action_listing_page_index = int(adventure_action_listing_page_index, 16)
    except ValueError:
        return
    
    await client.interaction_component_acknowledge(
        interaction_event,
        False,
    )
    
    if interaction_event.user_id != user_id:
        return
    
    while True:
        adventure = await adventure_get(adventure_entry_id)
        while True:
            if adventure is None:
                adventure_action = None
                break
            
            adventure_action_listing = adventure.action_listing
            if adventure_action_listing is None:
                adventure_action = None
                break
            
            if adventure_action_index >= len(adventure_action_listing):
                adventure_action = None
                break
            
            
            adventure_action = adventure_action_listing[adventure_action_index]
            break
        
        if (adventure_action is None):
            error_message = 'Could not resolve adventure action.'
            break
        
        
        await client.interaction_response_message_edit(
            interaction_event,
            components = build_adventure_action_view_components(
                user_id,
                adventure_entry_id,
                adventure_action,
                adventure_action_index,
                adventure_view_mode,
                allow_switching_to_adventure_listing_view,
                adventure_listing_page_index,
                allow_switching_to_adventure_action_listing_view,
                adventure_action_listing_page_index,
            ),
        )
        return
    
    await client.interaction_followup_message_create(
        interaction_event,
        content = error_message,
        allowed_mentions = None,
        show_for_invoking_user_only = True,
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_ADVENTURE_ACTION_BATTLE_LOGS_PATTERN)
async def handle_adventure_action_battle_logs_view(
    client,
    interaction_event,
    user_id,
    adventure_entry_id,
    adventure_action_index,
):
    """
    Shows the selected adventure action's battle logs.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        The owner user's identifier as hexadecimal. Later converted back to integer.
    
    adventure_entry_id : `str`
        The adventure's entry's identifier as hexadecimal. Later converted back to integer.
    
    adventure_action_index : `str`
        The adventure's action's index as hexadecimal. Later converted back to integer.
    """
    user_id = int(user_id, 16)
    adventure_entry_id = int(adventure_entry_id, 16)
    adventure_action_index = int(adventure_action_index, 16)
    
    await client.interaction_component_acknowledge(
        interaction_event,
        False,
    )
    
    # Battles are not implemented yet.


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_ADVENTURE_ACTION_LISTING_VIEW_PATTERN)
async def handle_adventure_action_listing_view(
    client,
    interaction_event,
    user_id,
    adventure_entry_id,
    adventure_view_mode,
    allow_switching_to_adventure_listing_view,
    adventure_listing_page_index,
    adventure_action_listing_page_index,
):
    """
    Shows the selected adventure action listing page.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        The owner user's identifier as hexadecimal. Later converted back to integer.
    
    adventure_entry_id : `str`
        The adventure's entry's identifier as hexadecimal. Later converted back to integer.
    
    adventure_view_mode : `str`
        How to render the adventure as hexadecimal.
        
    allow_switching_to_adventure_listing_view : `str`
        Whether switching to adventure listing is allowed from adventure view as hexadecimal.
    
    adventure_listing_page_index : `str`
        Adventure listing page index to direct to from adventure view as hexadecimal.
        Later converted to integer.
    
    adventure_action_listing_page_index : `str`
        Page index to show in hexadecimal. Later converted back to integer.
    """
    try:
        user_id = int(user_id, 16)
        adventure_entry_id = int(adventure_entry_id, 16)
        adventure_view_mode = int(adventure_view_mode, 16)
        allow_switching_to_adventure_listing_view = True if int(allow_switching_to_adventure_listing_view, 16) else False
        adventure_listing_page_index = int(adventure_listing_page_index, 16)
        adventure_action_listing_page_index = int(adventure_action_listing_page_index, 16)
    except ValueError:
        return
    
    await client.interaction_component_acknowledge(
        interaction_event,
        False,
    )
    
    if interaction_event.user_id != user_id:
        return
    
    while True:
        adventure = await adventure_get(adventure_entry_id)
        if (adventure is None):
            error_message = ERROR_MESSAGE_ADVENTURE_UNKNOWN_ADVENTURE
            break
        
        await client.interaction_response_message_edit(
            interaction_event,
            components = build_adventure_action_listing_view_components(
                adventure,
                adventure_view_mode,
                allow_switching_to_adventure_listing_view,
                adventure_listing_page_index,
                adventure_action_listing_page_index,
            ),
        )
        return
    
    await client.interaction_followup_message_create(
        interaction_event,
        content = error_message,
        allowed_mentions = None,
        show_for_invoking_user_only = True,
    )


@ADVENTURE_COMMANDS.interactions
async def history(
    client,
    interaction_event,
):
    """
    Shows you your adventure history.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    """
    await client.interaction_application_command_acknowledge(
        interaction_event,
        False,
        show_for_invoking_user_only = True
    )
    
    page_count, adventure_listing = await adventure_listing_get_page(
        interaction_event.user_id, -1, ADVENTURE_LISTING_PAGE_SIZE
    )
    
    await client.interaction_response_message_edit(interaction_event, '-# _ _ ')
    await client.interaction_response_message_delete(interaction_event)
    
    await client.interaction_followup_message_create(
        interaction_event,
        components = build_adventure_listing_view_components(
            interaction_event.user_id, adventure_listing, page_count - 1, page_count
        ),
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_ADVENTURE_LISTING_VIEW_PATTERN)
async def handle_adventure_listing_view(
    client,
    interaction_event,
    user_id,
    page_index,
):
    """
    Shows the selected adventure listing page.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        The owner user's identifier as hexadecimal. Later converted back to integer.
    
    page_index : `str`
        Page index to show in hexadecimal. Later converted back to integer.
    """
    user_id = int(user_id, 16)
    page_index = int(page_index, 16)
    
    await client.interaction_component_acknowledge(
        interaction_event,
        False,
    )
    
    if interaction_event.user_id != user_id:
        return
    
    page_count, adventure_listing = await adventure_listing_get_page(
        interaction_event.user_id, page_index, ADVENTURE_LISTING_PAGE_SIZE
    )
    
    await client.interaction_response_message_edit(
        interaction_event,
        components = build_adventure_listing_view_components(
            interaction_event.user_id, adventure_listing, page_index, page_count
        ),
    )


@ADVENTURE_COMMANDS.interactions
async def butcher(
    client,
    interaction_event,
    item_name : (str, 'Body or body part', 'body'),
):
    """
    Butcher a body or body part you have already collected.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    item_name : `str`
        The item's name to butcher.
    """
    await client.interaction_application_command_acknowledge(
        interaction_event,
        False,
        show_for_invoking_user_only = True,
    )
    
    while True:
        adventure = await adventure_get_active(interaction_event.user_id)
        if (adventure is not None):
            error_message = 'You cannot butcher while on adventure.'
            break
        
        inventory = await get_inventory(interaction_event.user_id)
        item = select_item(inventory, ITEM_FLAG_BUTCHERABLE, item_name)
        if item is None:
            error_message = f'You cannot butcher {item_name!s}, you do not have such an item.'
            break
        
        user_stats = await user_stats_get(interaction_event.user_id)
        multiplier = get_action_type_multiplier(ACTION_TYPE_BUTCHERING, user_stats)
        
        now = DateTime.now(TimeZone.utc)
        recovering_until = user_stats.recovering_until
        if (recovering_until is None) or (recovering_until < now):
            recovering_until = None
        
        
        await client.interaction_response_message_edit(interaction_event, '-# _ _ ')
        await client.interaction_response_message_delete(interaction_event)
        
        await client.interaction_followup_message_create(
            interaction_event,
            components = build_butcher_components(
                interaction_event.user,
                interaction_event.guild_id,
                item,
                0,
                0,
                multiplier,
                None,
                0,
                None,
                None,
                None,
                0,
                now,
                recovering_until,
            ),
        )
        return
    
    await client.interaction_response_message_edit(
        interaction_event,
        content = error_message,
    )


@butcher.autocomplete('item_name')
async def command_butcher_autocomplete_item_name(interaction_event, value):
    """
    Gets item suggestions for the given value.
    
    This function is a coroutine.
    
    Parameters
    ----------
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    value : `None | str`
        Value to filter for.
    
    Returns
    -------
    suggestions : `None | list<(str, int)>`
    """
    inventory = await get_inventory(interaction_event.user_id)
    return create_item_suggestions(inventory, ITEM_FLAG_BUTCHERABLE, value)


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_ADVENTURE_BUTCHER_INITIAL_PATTERN)
async def handle_butcher_initial(
    client,
    interaction_event,
    user_id,
    item_id,
):
    """
    handles a butcher initial interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        The invoking user's identifier in hexadecimal. Later converted to int.
    
    item_id : `str`
        The butchered item's identifier in hexadecimal. Later converted to int.
    """
    try:
        user_id = int(user_id, 16)
        item_id = int(item_id, 16)
    except ValueError:
        return
    
    await client.interaction_component_acknowledge(
        interaction_event,
        False,
    )
    
    if interaction_event.user_id != user_id:
        return
    
    while True:
        adventure = await adventure_get_active(interaction_event.user_id)
        if (adventure is not None):
            error_message = 'You cannot butcher while on adventure.'
            break
        
        initial_item = get_item_nullable(item_id)
        if initial_item is None:
            error_message = 'Such item does not exist.'
            break
        
        inventory = await get_inventory(interaction_event.user_id)
        amount = inventory.get_item_amount(initial_item)
        if amount <= 0:
            error_message = f'You do not have any {initial_item.name}-s.'
            break
        
        user_stats = await user_stats_get(interaction_event.user_id)
        multiplier = get_action_type_multiplier(ACTION_TYPE_BUTCHERING, user_stats)
        
        seed = create_seed()
        butcher_amounts, energy_cost, butcherables = butcher_calculate_done(
            initial_item, seed, 0, multiplier
        )
        
        # Update inventory and stats.
        
        inventory.modify_item_amount(initial_item, -1)
        if (butcher_amounts is not None):
            for item_id, amount in butcher_amounts:
                inventory.modify_item_amount(get_item(item_id), amount)
        
        await save_inventory(inventory)
        
        now = DateTime.now(TimeZone.utc)
        recovering_until = user_stats.recovering_until
        if (recovering_until is None) or (recovering_until < now):
            recovering_until = None
        
        if energy_cost:
            recovering_until = (
                (now if recovering_until is None else recovering_until) +
                TimeDelta(seconds = recovery_duration_seconds_get_of_energy_cost(energy_cost))
            )
            user_stats_set_recovering_until(user_stats, recovering_until)
            await set_closest_adventure_recovery_over_reminder(user_stats, recovering_until)
            await user_stats_save(user_stats)
        
        # Respond.
        
        await client.interaction_response_message_edit(
            interaction_event,
            components = build_butcher_components(
                interaction_event.user,
                interaction_event.guild_id,
                initial_item,
                seed,
                0,
                multiplier,
                butcher_amounts,
                energy_cost,
                butcherables,
                initial_item,
                butcher_amounts,
                energy_cost,
                now,
                recovering_until,
            ),
        )
        return
    
    await client.interaction_followup_message_create(
        interaction_event,
        content = error_message,
        show_for_invoking_user_only = True,
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_ADVENTURE_BUTCHER_CONTINUOUS_PATTERN)
async def handle_butcher_continuous(
    client,
    interaction_event,
    user_id,
    item_id,
    seed,
    butcher_flags,
    butchered_index,
    multiplier,
):
    """
    handles a butcher continuous interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        The invoking user's identifier in hexadecimal. Later converted to int.
    
    item_id : `str`
        The butchered item's identifier in hexadecimal. Later converted to int.
    
    seed : `str`
        Seed to use for butchering in hexadecimal. Later converted to int.
    
    butcher_flags : `str`
        Flags described which body parts were already butchered in hexadecimal. Later converted to int.
    
    butchered_index : `str`
        The index of the item to butcher in hexadecimal. Later converted to int.
    
    multiplier : `str`
        The initial multiplier in hexadecimal. Later converted to float.
    """
    try:
        user_id = int(user_id, 16)
        item_id = int(item_id, 16)
        seed = int(seed, 16)
        butcher_flags = int(butcher_flags, 16)
        butchered_index = int(butchered_index, 16)
    except ValueError:
        return
    
    try:
        multiplier = base_64_decode(multiplier)
    except ValueError:
        return
    
    if len(multiplier) != 8:
        return
    
    multiplier = FLOAT_STRUCT.unpack(multiplier)[0]
    
    if is_nan(multiplier):
        multiplier = 1.0
    elif multiplier < 0.05:
        multiplier = 0.05
    elif multiplier > 1000.0:
        multiplier = 1000.0
    
    await client.interaction_component_acknowledge(
        interaction_event,
        False,
    )
    
    if interaction_event.user_id != user_id:
        return
    
    while True:
        adventure = await adventure_get_active(interaction_event.user_id)
        if (adventure is not None):
            error_message = 'You cannot butcher while on adventure.'
            break
        
        initial_item = get_item_nullable(item_id)
        if initial_item is None:
            error_message = 'Such item does not exist.'
            break
        
        butcher_amounts_accumulated, energy_cost_accumulated, butcherables = butcher_calculate_done(
            initial_item, seed, butcher_flags, multiplier
        )
        
        if butcherables is None:
            butchered_item = None
        else:
            for butchered_item, index in butcherables:
                if index == butchered_index:
                    break
            else:
                butchered_item = None
        
        if (butchered_item is None):
            error_message = 'Such body part does not exist.'
            break
        
        inventory = await get_inventory(interaction_event.user_id)
        amount = inventory.get_item_amount(butchered_item)
        if amount <= 0:
            error_message = f'You do not have any {butchered_item.name}-s.'
            break
        
        butcher_amounts, energy_cost = butcher_calculate_step(butchered_item, butchered_index, seed, multiplier)
        
        # Update inventory and stats.
        
        inventory.modify_item_amount(butchered_item, -1)
        if (butcher_amounts is not None):
            for item_id, amount in butcher_amounts:
                inventory.modify_item_amount(get_item(item_id), amount)
        
        await save_inventory(inventory)
        
        user_stats = await user_stats_get(interaction_event.user_id)
        
        now = DateTime.now(TimeZone.utc)
        recovering_until = user_stats.recovering_until
        if (recovering_until is None) or (recovering_until < now):
            recovering_until = None
        
        if energy_cost:
            recovering_until = (
                (now if recovering_until is None else recovering_until) +
                TimeDelta(seconds = recovery_duration_seconds_get_of_energy_cost(energy_cost))
            )
            user_stats_set_recovering_until(user_stats, recovering_until)
            await set_closest_adventure_recovery_over_reminder(user_stats, recovering_until)
            await user_stats_save(user_stats)
        
        # Respond.
        
        butcher_amounts_accumulated, energy_cost_accumulated, butcherables = butcher_done_append(
            butcher_amounts_accumulated,
            energy_cost_accumulated,
            butcherables,
            butchered_item,
            butchered_index,
            butcher_amounts,
            energy_cost,
        )
        
        await client.interaction_response_message_edit(
            interaction_event,
            components = build_butcher_components(
                interaction_event.user,
                interaction_event.guild_id,
                initial_item,
                seed,
                butcher_flags | (1 << butchered_index),
                multiplier,
                butcher_amounts_accumulated,
                energy_cost_accumulated,
                butcherables,
                butchered_item,
                butcher_amounts,
                energy_cost,
                now,
                recovering_until,
            ),
        )
        return
    
    await client.interaction_followup_message_create(
        interaction_event,
        content = error_message,
        show_for_invoking_user_only = True,
    )
