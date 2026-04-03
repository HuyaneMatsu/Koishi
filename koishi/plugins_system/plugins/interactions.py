__all__ = ()

from hata import CLIENTS
from hata.ext.slash import InteractionResponse

from ...bots import MAIN_CLIENT

from .helpers import (
    CUSTOM_ID_PAGE_CLOSE, CUSTOM_ID_PAGE_N_RP, CUSTOM_ID_SWITCH_CLIENT_RP, check_permission,
    create_plugins_page_components, get_plugins_sequence, render_plugins_page
)


@MAIN_CLIENT.interactions(custom_id = CUSTOM_ID_PAGE_N_RP)
async def list_plugins_for_page(event, client_id, page):
    """
    Lists the available plugins for the given page.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received event.
    
    client_id : `str`
        Client identifier. Converted to `int`.
    
    page : `str`
        Page number. Converted to `int`.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    check_permission(event)
    page = int(page, base = 16)
    client_id = int(client_id, base = 16)
    selected_client = CLIENTS.get(client_id, None)
    
    plugins_sequence = get_plugins_sequence(selected_client)
    return InteractionResponse(
        content = render_plugins_page(selected_client, plugins_sequence, page),
        components = create_plugins_page_components(selected_client, plugins_sequence, page),
    )


@MAIN_CLIENT.interactions(custom_id = CUSTOM_ID_SWITCH_CLIENT_RP)
async def list_plugins_for_client(event, page):
    """
    Lists the available plugins for the selected client.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received event.
    
    page : `str`
        Page number. Converted to `int`.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    check_permission(event)
    
    page = int(page, base = 16)
    
    client_id = event.value
    if client_id is None:
        selected_client = None
    else:
        client_id = int(client_id, base = 16)
        selected_client = CLIENTS.get(client_id, None)
    
    plugins_sequence = get_plugins_sequence(selected_client)
    return InteractionResponse(
        content = render_plugins_page(selected_client, plugins_sequence, page),
        components = create_plugins_page_components(selected_client, plugins_sequence, page),
    )


@MAIN_CLIENT.interactions(custom_id = CUSTOM_ID_PAGE_CLOSE)
async def close_plugins_page(client, event):
    """
    Closes the plugins page.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    event : ``InteractionEvent``
        The received event.
    """
    check_permission(event)
    
    await client.interaction_component_acknowledge(event)
    await client.interaction_response_message_delete(event)
