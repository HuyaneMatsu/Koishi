__all__ = ()

from hata.ext.slash import P

from ...bot_utils.constants import GUILD__SUPPORT
from ...bot_utils.user_getter import get_user
from ...bots import MAIN_CLIENT

from .component_building import (
    build_to_do_create_form, build_to_do_delete_form, build_to_do_edit_form, build_to_do_listing, build_to_do_view
)
from .helpers import check_for_required_role, get_to_do_suggestions, match_to_do, match_to_do_listing
from .queries import get_to_do_listing


TO_DO = MAIN_CLIENT.interactions(
    None,
    name = 'todo',
    description = 'To-Do list for koishi',
    guild = GUILD__SUPPORT,
)


@TO_DO.autocomplete('name')
async def autocomplete_to_do_name(client, interaction_event, value):
    """
    Autocompletes a to-do command's name.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client receiving this interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    value : `None | str`
        Value to match.
    """
    while True:
        error_message = check_for_required_role(interaction_event)
        if (error_message is not None):
            break
        
        to_do_listing = await get_to_do_listing()
        await client.interaction_application_command_autocomplete(
            interaction_event,
            get_to_do_suggestions(to_do_listing, value),
        )
        return
    
    await client.interaction_application_command_autocomplete(
        interaction_event,
        None,
    )
    await client.interaction_followup_message_create(
        interaction_event,
        allowed_mentions = None,
        content = error_message,
        show_for_invoking_user_only = False,
    )


@TO_DO.interactions
async def add(
    client,
    interaction_event,
):
    """
    Adds a new to-do!
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client receiving this interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    """
    while True:
        error_message = check_for_required_role(interaction_event)
        if (error_message is not None):
            break
        
        await client.interaction_form_send(
            interaction_event,
            build_to_do_create_form(),
        )
        return
    
    await client.interaction_response_message_create(
        interaction_event,
        allowed_mentions = None,
        content = error_message,
        show_for_invoking_user_only = False,
    )


@TO_DO.interactions
async def get(
    client,
    interaction_event,
    name: (str, 'The entry\'s name | Use # to search by id.'),
):
    """
    Shows the defined to-do.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client receiving this interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    name : `str`
        The to-do's name to get.
    """
    await client.interaction_application_command_acknowledge(
        interaction_event,
        show_for_invoking_user_only = True,
    )
    
    while True:
        error_message = check_for_required_role(interaction_event)
        if (error_message is not None):
            break
        
        to_do_listing = await get_to_do_listing()
        to_do = match_to_do(to_do_listing, name)
        if (to_do is None):
            error_message = 'Could not match any to-do.'
            break
        
        user = await get_user(to_do.creator_id)
        
        await client.interaction_response_message_edit(interaction_event, '-# _ _')
        await client.interaction_response_message_delete(interaction_event)
        await client.interaction_followup_message_create(
            interaction_event,
            allowed_mentions = None,
            components = build_to_do_view(to_do, user, interaction_event.guild_id),
        )
        return
    
    await client.interaction_response_message_edit(
        interaction_event,
        allowed_mentions = None,
        content = error_message,
    )


@TO_DO.interactions
async def list_(
    client,
    interaction_event,
    page: P(int, 'Select a page.', min_value = 1, max_value = 10000) = 1,
    query: P(str, 'The entry\'s name', min_length = 2, max_length = 30) = None,
):
    """
    Lists to-dos.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client receiving this interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    page : `int` = `1`, Optional
        The page to show.
    
    query : `None | str` = `None`, Optional
        The to-do's name to get.
    """
    await client.interaction_application_command_acknowledge(
        interaction_event,
        show_for_invoking_user_only = True,
    )
    
    page_index = max(0, page - 1)
    
    while True:
        error_message = check_for_required_role(interaction_event)
        if (error_message is not None):
            break
        
        to_do_listing = await get_to_do_listing()
        to_do_listing = match_to_do_listing(to_do_listing, query)
        
        await client.interaction_response_message_edit(interaction_event, '-# _ _')
        await client.interaction_response_message_delete(interaction_event)
        await client.interaction_followup_message_create(
            interaction_event,
            allowed_mentions = None,
            components = build_to_do_listing(to_do_listing, page_index, query),
        )
        return
    
    await client.interaction_response_message_edit(
        interaction_event,
        allowed_mentions = None,
        content = error_message,
    )


@TO_DO.interactions
async def edit(
    client,
    interaction_event,
    name: (str, 'The entry\'s name | Use # to search by id.'),
):
    """
    Edit the defined to-do!
    
    Parameters
    ----------
    client : ``Client``
        The client receiving this interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    name : `str`
        The to-do's name to get.
    """
    while True:
        error_message = check_for_required_role(interaction_event)
        if (error_message is not None):
            break
        
        to_do_listing = await get_to_do_listing()
        to_do = match_to_do(to_do_listing, name)
        if (to_do is None):
            error_message = 'Could not match any to-do.'
            break
        
        await client.interaction_form_send(
            interaction_event,
            build_to_do_edit_form(to_do),
        )
        return
    
    await client.interaction_response_message_create(
        interaction_event,
        allowed_mentions = None,
        content = error_message,
        show_for_invoking_user_only = False,
    )


@TO_DO.interactions
async def del_(
    client,
    interaction_event,
    name: (str, 'The entry\'s name | Use # to search by id.'),
):
    """
    Removes the defined to-do.
    
    Parameters
    ----------
    client : ``Client``
        The client receiving this interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    name : `str`
        The to-do's name to get.
    """
    while True:
        error_message = check_for_required_role(interaction_event)
        if (error_message is not None):
            break
        
        to_do_listing = await get_to_do_listing()
        to_do = match_to_do(to_do_listing, name)
        if (to_do is None):
            error_message = 'Could not match any to-do.'
            break
        
        await client.interaction_form_send(
            interaction_event,
            build_to_do_delete_form(to_do),
        )
        return
    
    await client.interaction_response_message_create(
        interaction_event,
        allowed_mentions = None,
        content = error_message,
        show_for_invoking_user_only = False,
    )
