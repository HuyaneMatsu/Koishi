__all__ = ()

from ...bots import FEATURE_CLIENTS

from .component_building import build_top_list_components
from .constants import TOP_LIST_TYPE_BALANCE, TOP_LIST_TYPE_CREDIBILITY
from .custom_ids import (
    CUSTOM_ID_TOP_LIST_CLOSE_PATTERN, CUSTOM_ID_TOP_LIST_PAGE_INDEX_DECREMENT_DISABLED,
    CUSTOM_ID_TOP_LIST_PAGE_INDEX_INCREMENT_DISABLED, CUSTOM_ID_TOP_LIST_PAGE_INDEX_PATTERN
)
from .queries import get_top_list_entries


TOP_LIST_COMMAND = FEATURE_CLIENTS.interactions(
    None,
    name = 'top-list',
    is_global = True,
    description = 'A list of my best simps',
)


async def handle_top_list_command_common(
    client,
    interaction_event,
    top_list_type,
):
    """
    Common top list command handlers.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        Client receiving this interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    top_list_type : `int`
        Top list's type.
    """
    await client.interaction_application_command_acknowledge(
        interaction_event,
        False,
    )
    
    processed_entries_and_has_more = await get_top_list_entries(top_list_type, 0)
    
    await client.interaction_response_message_edit(
        interaction_event,
        components = build_top_list_components(
            interaction_event.user_id, top_list_type, 0, *processed_entries_and_has_more, interaction_event.guild_id
        ),
    )


@TOP_LIST_COMMAND.interactions(name = 'heart')
async def top_list_balance(
    client,
    interaction_event,
):
    """
    Heart top list.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        Client receiving this interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    """
    await handle_top_list_command_common(client, interaction_event, TOP_LIST_TYPE_BALANCE)


@TOP_LIST_COMMAND.interactions(name = 'credibility')
async def top_list_credibility(
    client,
    interaction_event,
):
    """
    Credibility top list.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        Client receiving this interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    """
    await handle_top_list_command_common(client, interaction_event, TOP_LIST_TYPE_CREDIBILITY)


@FEATURE_CLIENTS.interactions(custom_id = [
    CUSTOM_ID_TOP_LIST_PAGE_INDEX_INCREMENT_DISABLED,
    CUSTOM_ID_TOP_LIST_PAGE_INDEX_DECREMENT_DISABLED,
])
async def handle_top_list_dummy():
    """
    Handles a dummy top list interaction.
    
    This function is a coroutine.
    """


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_TOP_LIST_PAGE_INDEX_PATTERN)
async def handle_top_list_page(client, interaction_event, user_id, top_list_type, page_index):
    """
    Handles a top list page component interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        Client receiving this interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        The original invoking user's identifier encoded as a string representing a hexadecimal integer.
    
    top_list_type : `str`
        The list's type encoded as a string representing a hexadecimal integer.
    
    page_index : `int`
        The page's index to show encoded as a string representing a hexadecimal integer.
    """
    try:
        user_id = int(user_id, 16)
        top_list_type = int(top_list_type, 16)
        page_index = int(page_index, 16)
    except ValueError:
        return
    
    if interaction_event.user_id != user_id:
        return
    
    await client.interaction_component_acknowledge(
        interaction_event,
        False,
    )
    
    processed_entries_and_has_more = await get_top_list_entries(top_list_type, page_index)
    
    await client.interaction_response_message_edit(
        interaction_event,
        components = build_top_list_components(
            user_id, top_list_type, page_index, *processed_entries_and_has_more, interaction_event.guild_id
        ),
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_TOP_LIST_CLOSE_PATTERN)
async def top_list_close(client, interaction_event, user_id):
    """
    Handles a top list close component interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        Client receiving this interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        The original invoking user's identifier encoded as a string representing a hexadecimal integer.
    """
    
    try:
        user_id = int(user_id, 16)
    except ValueError:
        return
    
    if interaction_event.user_id != user_id:
        return
    
    await client.interaction_component_acknowledge(interaction_event)
    await client.interaction_response_message_delete(interaction_event)
