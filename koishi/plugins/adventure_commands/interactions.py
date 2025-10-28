__all__ = ()

from datetime import datetime as DateTime, timezone as TimeZone

from hata import InteractionType, Client

from ...bots import FEATURE_CLIENTS

from ..adventure_core import (
    ADVENTURE_STATE_FINALIZED, AUTO_CANCELLATION_ID_DEFAULT, AUTO_CANCELLATIONS, AUTO_CANCELLATIONS_ALLOWED, Adventure,
    DURATION_MAX, DURATION_MIN, DURATION_SUGGESTION_SETS, LOCATIONS, RETURN_ID_AFTER, RETURNS, RETURNS_ALLOWED, TARGETS,
    adventure_cancel, build_duration_suggestion, can_cancel_adventure, get_active_adventure, get_adventure,
    get_adventure_action_listing, get_adventure_listing_page, parse_duration_hexadecimal, parse_duration_suggestion,
    scheduled_adventure_arrival, store_adventure
)
from ..inventory_core import get_inventory
from ..user_stats_core import get_user_stats

from .component_builders import (
    ADVENTURE_LISTING_PAGE_SIZE, build_adventure_action_listing_view_components, build_adventure_action_view_components,
    build_adventure_cancellation_components, build_adventure_cancellation_confirmation_form,
    build_adventure_create_confirm_components, build_adventure_create_confirmation_form,
    build_adventure_listing_view_components, build_adventure_view_active_components,
    build_adventure_view_finalized_components, produce_adventure_depart_failure_recovery_description
)
from .custom_ids import (
    ADVENTURE_ACTION_BATTLE_LOGS_RP, ADVENTURE_ACTION_VIEW_DEPART, ADVENTURE_ACTION_VIEW_RETURN,
    ADVENTURE_ACTION_LISTING_VIEW_RP, ADVENTURE_ACTION_VIEW_RP, ADVENTURE_CANCEL_RP, ADVENTURE_CREATE_CONFIRM_RP,
    ADVENTURE_LISTING_VIEW_RP, ADVENTURE_VIEW_RP
)
from .duration_suggesting import get_duration_suggestions
from .location_suggesting import get_best_matching_location, get_location_suggestions
from .target_suggesting import get_best_matching_target, get_target_suggestions


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
        'return_',
    ) = None,
    auto_cancellation_id_hexadecimal : (
        [(auto_cancellation.name, format(auto_cancellation.id, 'x')) for auto_cancellation in AUTO_CANCELLATIONS_ALLOWED],
        'Do you want to arrive back if full or low on energy / health?',
        'auto-cancellation',
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
    
    return_id_hexadecimal : `str`
        The return_ logic's identifier in hexadecimal.
    
    auto_cancellation_id_hexadecimal : `None | str`
        The auto-cancellation logic's identifier in hexadecimal.
    """
    while True:
        adventure = await get_active_adventure(interaction_event.user_id)
        if (adventure is not None):
            error_message = 'You are already on an adventure.'
            break
        
        user_stats = await get_user_stats(interaction_event.user_id)
        recovering_until = user_stats.recovering_until
        now = DateTime.now(tz = TimeZone.utc)
        if (recovering_until is not None) and (recovering_until > now):
            error_message = ''.join([*produce_adventure_depart_failure_recovery_description(recovering_until, now)])
            break
        
        # Check whether the inventory weight is greater than the available.
        inventory = await get_inventory(interaction_event.user_id)
        if inventory.weight > user_stats.stats_calculated.extra_inventory:
            error_message = f'Your inventory is overloaded, cannot go on an adventure like this.'
            break
        
        location = get_best_matching_location(location_name)
        if location is None:
            error_message = f'Unknown location: {location_name}.'
            break    
        
        target = get_best_matching_target(location.target_ids, target_name)
        if target is None:
            error_message = f'Unknown target: {target_name}.'
            break
        
        duration = parse_duration_hexadecimal(duration_string)
        if not duration:
            duration = parse_duration_suggestion(duration_string)
            if not duration:
                error_message = f'Could not recognize duration: {duration_string}.'
                break
        
        if duration < DURATION_MIN:
            error_message = (
                f'Duration under lower threshold: '
                f'{build_duration_suggestion(duration)} < {build_duration_suggestion(DURATION_MIN)}.'
            )
            break
        
        if duration > DURATION_MAX:
            error_message = (
                f'Duration over upper threshold: '
                f'{build_duration_suggestion(duration)} > {build_duration_suggestion(DURATION_MAX)}.'
            )
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
        
        await client.interaction_form_send(
            interaction_event,
            build_adventure_create_confirmation_form(
                interaction_event.user_id, location, target, duration, return_, auto_cancellation, True
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
async def autocomplete_depart_location(location_name):
    """
    Auto completes depart location.
    
    This function is a coroutine.
    
    Parameters
    ----------
    location_name : `None | str`
        The value to autocomplete.
    
    Returns
    -------
    suggestions : `list<(str, str)>`
    """
    return get_location_suggestions(location_name)


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
    
    location = get_best_matching_location(location_name)
    if location is None:
        return
    
    return get_target_suggestions(location.target_ids, target_name)


@depart.autocomplete('duration')
async def autocomplete_depart_duration(interaction_event, duration_string):
    """
    Auto completes depart target.
    
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
        duration = parse_duration_hexadecimal(duration_string)
        if duration:
            return [
                (build_duration_suggestion(duration), format(duration, 'x')),
            ]
    
    location_name = interaction_event.get_value_of('depart', 'location')
    if location_name is None:
        return
    
    location = get_best_matching_location(location_name)
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


@FEATURE_CLIENTS.interactions(custom_id = ADVENTURE_CREATE_CONFIRM_RP, target = 'form')
async def handle_adventure_create_confirm(
    client,
    interaction_event,
    user_id,
    location_id,
    target_id,
    duration,
    return_id,
    auto_cancellation_id,
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
            error_message = 'Could not restore the adventure data. Please depart to a new one.'
            break
        
        adventure = await get_active_adventure(user_id)
        if (adventure is not None):
            error_message = 'You are already on an adventure.'
            break
        
        user_stats = await get_user_stats(user_id)
        recovering_until = user_stats.recovering_until
        if (recovering_until is not None) and (recovering_until > DateTime.now(tz = TimeZone.utc)):
            error_message = 'You are currently recovering, cannot go on an adventure.'
            break
        
        stats_calculated = user_stats.stats_calculated
        
        # Check whether the inventory weight is greater than the available.
        inventory = await get_inventory(interaction_event.user_id)
        if inventory.weight > stats_calculated.extra_inventory:
            error_message = f'Your inventory is overloaded, cannot go on an adventure like this.'
            break
        
        adventure = Adventure(
            user_id,
            
            location_id,
            target_id,
            return_id,
            auto_cancellation_id,
            
            duration,
            stats_calculated.extra_health,
            stats_calculated.extra_energy,
        )
        await store_adventure(adventure)
        await scheduled_adventure_arrival(adventure)
        
        # Respond
        await client.interaction_response_message_edit(interaction_event, '-# _ _ ')
        await client.interaction_response_message_delete(interaction_event)
        
        await client.interaction_followup_message_create(
            interaction_event,
            components = build_adventure_create_confirm_components(
                interaction_event.user_id, adventure.entry_id, location, target, duration, return_, auto_cancellation,
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
        adventure = await get_active_adventure(interaction_event.user_id)
        if (adventure is None):
            error_message = 'You are not on an adventure.'
            break
        
        if not can_cancel_adventure(adventure):
            error_message = 'You are heading back home already.'
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


@ADVENTURE_COMMANDS.interactions
async def view(
    client,
    interaction_event,
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
    """
    await client.interaction_application_command_acknowledge(
        interaction_event,
        False,
        show_for_invoking_user_only = True
    )
    
    while True:
        adventure = await get_active_adventure(interaction_event.user_id)
        if (adventure is None):
            error_message = 'You are not on an adventure.'
            break
        
        adventure_action_listing = await get_adventure_action_listing(adventure.entry_id)
        user_stats = await get_user_stats(interaction_event.user_id)
        inventory = await get_inventory(adventure.user_id)
        
        await client.interaction_response_message_edit(interaction_event, '-# _ _ ')
        await client.interaction_response_message_delete(interaction_event)
        
        await client.interaction_followup_message_create(
            interaction_event,
            components = build_adventure_view_active_components(
                adventure,
                adventure_action_listing,
                False,
                0,
                DateTime.now(tz = TimeZone.utc),
                user_stats.stats_calculated.extra_inventory,
                inventory.weight,
            ),
        )
        return
    
    await client.interaction_response_message_edit(
        interaction_event,
        content = error_message,
        allowed_mentions = None,
    )


@FEATURE_CLIENTS.interactions(custom_id = ADVENTURE_CANCEL_RP)
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
        adventure = await get_adventure(adventure_entry_id)
        if (adventure is None):
            error_message = 'Could not resolve adventure.'
            break
        
        if not can_cancel_adventure(adventure):
            error_message = 'You are heading back home already or the adventure already finished.'
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


@FEATURE_CLIENTS.interactions(custom_id = ADVENTURE_CANCEL_RP, target = 'form')
async def handle_active_adventure_cancellation_confirmation(
    client,
    interaction_event,
    user_id,
    adventure_entry_id,
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
    """
    user_id = int(user_id, 16)
    adventure_entry_id = int(adventure_entry_id, 16)
    
    if interaction_event.type is InteractionType.application_command:
        function = Client.interaction_application_command_acknowledge
    else:
        function = Client.interaction_component_acknowledge
    await function(client, interaction_event, False)
    
    if interaction_event.user_id != user_id:
        return
    
    while True:
        adventure = await get_adventure(adventure_entry_id)
        if (adventure is None):
            error_message = 'Could not resolve adventure.'
            break
        
        if not can_cancel_adventure(adventure):
            error_message = 'You are heading back home already or the adventure already finished.'
            break
        
        await adventure_cancel(adventure)
        
        if interaction_event.type is InteractionType.application_command:
            await client.interaction_response_message_edit(interaction_event, '-# _ _')
            await client.interaction_response_message_delete(interaction_event)
        
        await client.interaction_followup_message_create(
            interaction_event,
            components = build_adventure_cancellation_components(),
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


@FEATURE_CLIENTS.interactions(custom_id = ADVENTURE_VIEW_RP)
async def handle_adventure_view(
    client,
    interaction_event,
    user_id,
    adventure_entry_id,
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
    
    allow_switching_to_adventure_listing_view : `str`
        Whether switching to adventure listing is allowed from adventure view as hexadecimal.
        Later converted back to integer.
    
    adventure_listing_page_index : `str`
        Adventure listing page index to direct to from adventure view as hexadecimal.
        Later converted to integer.
    """
    user_id = int(user_id, 16)
    adventure_entry_id = int(adventure_entry_id, 16)
    allow_switching_to_adventure_listing_view = True if int(allow_switching_to_adventure_listing_view, 16) else False
    adventure_listing_page_index = int(adventure_listing_page_index, 16)
    
    await client.interaction_component_acknowledge(
        interaction_event,
        False,
    )
    
    if interaction_event.user_id != user_id:
        return
    
    while True:
        adventure = await get_adventure(adventure_entry_id)
        if (adventure is None):
            error_message = 'Could not resolve adventure.'
            break
        
        adventure_action_listing = await get_adventure_action_listing(adventure_entry_id)
        
        if adventure.state == ADVENTURE_STATE_FINALIZED:
            components = build_adventure_view_finalized_components(
                adventure,
                adventure_action_listing,
                allow_switching_to_adventure_listing_view,
                adventure_listing_page_index,
            )
        
        else:
            user_stats = await get_user_stats(interaction_event.user_id)
            inventory = await get_inventory(adventure.user_id)
            
            components = build_adventure_view_active_components(
                adventure,
                adventure_action_listing,
                allow_switching_to_adventure_listing_view,
                adventure_listing_page_index,
                DateTime.now(tz = TimeZone.utc),
                user_stats.stats_calculated.extra_inventory,
                inventory.weight,
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


@FEATURE_CLIENTS.interactions(custom_id = [ADVENTURE_ACTION_VIEW_DEPART, ADVENTURE_ACTION_VIEW_RETURN])
async def handle_adventure_action_disabled():
    """
    Dummy handler for disabled adventure action views.
    
    This function is a coroutine.
    """


@FEATURE_CLIENTS.interactions(custom_id = ADVENTURE_ACTION_VIEW_RP)
async def handle_adventure_action_view(
    client,
    interaction_event,
    user_id,
    adventure_entry_id,
    adventure_action_entry_id,
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
    
    adventure_action_entry_id : `str`
        The adventure's action's entry's identifier as hexadecimal. Later converted back to integer.
    
    allow_switching_to_adventure_listing_view : `str`
        Whether switching to adventure listing is allowed from adventure view as hexadecimal.
        Later converted back to integer.
    
    adventure_listing_page_index : `str`
        Adventure listing page index to direct to from adventure view as hexadecimal.
        Later converted to integer.
    
    allow_switching_to_adventure_action_listing_view : `str`
        Whether switching to action listing view is allowed from a action view as hexadecimal.
        Later converted back to boolean.
    
    adventure_action_listing_page_index : `str`
        adventure action listing age index to direct to from action view as hexadecimal.
        Later converted back to integer.
    """
    user_id = int(user_id, 16)
    adventure_entry_id = int(adventure_entry_id, 16)
    adventure_action_entry_id = int(adventure_action_entry_id, 16)
    allow_switching_to_adventure_listing_view = True if int(allow_switching_to_adventure_listing_view, 16) else False
    adventure_listing_page_index = int(adventure_listing_page_index, 16)
    allow_switching_to_adventure_action_listing_view = True if int(allow_switching_to_adventure_action_listing_view, 16) else False
    adventure_action_listing_page_index = int(adventure_action_listing_page_index, 16)
    
    await client.interaction_component_acknowledge(
        interaction_event,
        False,
    )
    
    if interaction_event.user_id != user_id:
        return
    
    while True:
        adventure_action_listing = await get_adventure_action_listing(adventure_entry_id)
        for adventure_action in adventure_action_listing:
            if adventure_action.entry_id == adventure_action_entry_id:
                break
        else:
            error_message = 'Could not resolve adventure action.'
            break
        
        
        await client.interaction_response_message_edit(
            interaction_event,
            components = build_adventure_action_view_components(
                user_id,
                adventure_action,
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


@FEATURE_CLIENTS.interactions(custom_id = ADVENTURE_ACTION_BATTLE_LOGS_RP)
async def handle_adventure_action_battle_logs_view(
    client,
    interaction_event,
    user_id,
    adventure_entry_id,
    adventure_action_entry_id,
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
    
    adventure_action_entry_id : `str`
        The adventure's action's entry's identifier as hexadecimal. Later converted back to integer.
    """
    user_id = int(user_id, 16)
    adventure_entry_id = int(adventure_entry_id, 16)
    adventure_action_entry_id = int(adventure_action_entry_id, 16)
    
    await client.interaction_component_acknowledge(
        interaction_event,
        False,
    )
    
    # Battles are not implemented yet.


@FEATURE_CLIENTS.interactions(custom_id = ADVENTURE_ACTION_LISTING_VIEW_RP)
async def handle_adventure_action_listing_view(
    client,
    interaction_event,
    user_id,
    adventure_entry_id,
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
        
    allow_switching_to_adventure_listing_view : `str`
        Whether switching to adventure listing is allowed from adventure view as hexadecimal.
        Later converted back to integer.
    
    adventure_listing_page_index : `str`
        Adventure listing page index to direct to from adventure view as hexadecimal.
        Later converted to integer.
    
    adventure_entry_id : `str`
        The adventure's entry's identifier as hexadecimal. Later converted back to integer.
    
    adventure_action_listing_page_index : `str`
        Page index to show in hexadecimal. Later converted back to integer.
    """
    user_id = int(user_id, 16)
    adventure_entry_id = int(adventure_entry_id, 16)
    allow_switching_to_adventure_listing_view = True if int(allow_switching_to_adventure_listing_view, 16) else False
    adventure_listing_page_index = int(adventure_listing_page_index, 16)
    adventure_action_listing_page_index = int(adventure_action_listing_page_index, 16)
    
    await client.interaction_component_acknowledge(
        interaction_event,
        False,
    )
    
    if interaction_event.user_id != user_id:
        return
    
    while True:
        adventure = await get_adventure(adventure_entry_id)
        if (adventure is None):
            error_message = 'Could not resolve adventure.'
            break
        
        adventure_action_listing = await get_adventure_action_listing(adventure_entry_id)
        
        await client.interaction_response_message_edit(
            interaction_event,
            components = build_adventure_action_listing_view_components(
                adventure,
                adventure_action_listing,
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
    
    page_count, adventure_listing = await get_adventure_listing_page(
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


@FEATURE_CLIENTS.interactions(custom_id = ADVENTURE_LISTING_VIEW_RP)
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
    
    page_count, adventure_listing = await get_adventure_listing_page(
        interaction_event.user_id, page_index, ADVENTURE_LISTING_PAGE_SIZE
    )
    
    await client.interaction_response_message_edit(
        interaction_event,
        components = build_adventure_listing_view_components(
            interaction_event.user_id, adventure_listing, page_index, page_count
        ),
    )
