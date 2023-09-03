__all__ = ()

from re import compile as re_compile, escape as re_escape

from ...bots import SLASH_CLIENT

from .builders import build_top_list_response
from .constants import (
    CUSTOM_ID_CLOSE, CUSTOM_ID_PAGE_BASE, CUSTOM_ID_PAGE_NEXT_DISABLED, CUSTOM_ID_PAGE_PREVIOUS_DISABLED
)
from .queries import get_top_list_entries


@SLASH_CLIENT.interactions(is_global = True)
async def top_list(
    page : ('number', 'page?') = 1,
):
    """
    A list of my best simps.
    
    This function is a coroutine generator.
    
    Parameters
    ----------
    page : `int` = `1`, Optional
        Page number (1 based).
    
    Yields
    ------
    acknowledge / response : `None` / ``InteractionResponse``
    """
    if page <= 1:
        page_index = 0
    else:
        page_index = page - 1
    
    yield
    entries = await get_top_list_entries(page_index)
    yield build_top_list_response(page_index, entries)


@SLASH_CLIENT.interactions(custom_id = re_compile(f'{re_escape(CUSTOM_ID_PAGE_BASE)}(\d+)'))
async def top_list_page(page_index):
    """
    Gets the top list for the given page.
    
    This function is a coroutine generator.
    
    Parameters
    ----------
    page_index : `str`
        The page's index to make the response for. Later converted to `int`.
    
    Yields
    ------
    acknowledge / response : `None` / ``InteractionResponse``
    """
    page_index = int(page_index)
    
    yield
    entries = await get_top_list_entries(page_index)
    yield build_top_list_response(page_index, entries)



@SLASH_CLIENT.interactions(custom_id = [CUSTOM_ID_PAGE_PREVIOUS_DISABLED, CUSTOM_ID_PAGE_NEXT_DISABLED])
async def disabled_page_move():
    """
    Called when a disabled page-move is clicked. Does nothing.
    
    This function is a coroutine.
    """
    pass


@SLASH_CLIENT.interactions(custom_id = CUSTOM_ID_CLOSE)
async def top_list_close(client, event):
    """
    Deletes the top-list if applicable.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    """
    await client.interaction_component_acknowledge(event)
    
    if event.user_permissions.can_manage_messages or event.message.interaction.user is event.user:
        await client.interaction_response_message_delete(event)
    
    else:
        await client.interaction_followup_message_create(
            event,
            'You must be the invoker of the interaction, or have manage messages permission to do this.',
            show_for_invoking_user_only = True,
        )
