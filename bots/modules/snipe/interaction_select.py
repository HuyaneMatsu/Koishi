__all__ = ()

from hata import Client

from .constants import CUSTOM_ID_SNIPE_SELECT_EMOJI, CUSTOM_ID_SNIPE_SELECT_REACTION, CUSTOM_ID_SNIPE_SELECT_STICKER
from .response_builder_select import (
    select_response_response_builder_emoji, select_response_response_builder_reaction, select_response_response_builder_sticker
)


SLASH_CLIENT: Client


@SLASH_CLIENT.interactions(custom_id = CUSTOM_ID_SNIPE_SELECT_EMOJI)
async def snipe_interaction_select_emoji(client, event):
    """
    Switches the response to the selected emoji.
    
    This function is a coroutine,
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    response : `None`, ``InteractionResponse``
    """
    return await select_response_response_builder_emoji(client, event)


@SLASH_CLIENT.interactions(custom_id = CUSTOM_ID_SNIPE_SELECT_REACTION)
async def snipe_interaction_select_reaction(client, event):
    """
    Switches the response to the selected reaction.
    
    This function is a coroutine,
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    response : `None`, ``InteractionResponse``
    """
    return await select_response_response_builder_reaction(client, event)


@SLASH_CLIENT.interactions(custom_id = CUSTOM_ID_SNIPE_SELECT_STICKER)
async def snipe_interaction_select_stickers(client, event):
    """
    Switches the response to the selected sticker.
    
    This function is a coroutine,
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    response : `None`, ``InteractionResponse``
    """
    return await select_response_response_builder_sticker(client, event)
