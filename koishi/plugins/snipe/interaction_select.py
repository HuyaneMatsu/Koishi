__all__ = ()

from hata import Client

from ...bots import FEATURE_CLIENTS

from .constants import CUSTOM_ID_SNIPE_SELECT
from .response_builder_select import select_response_builder


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_SNIPE_SELECT)
async def snipe_interaction_select_emoji(client, event):
    """
    Switches the response to the selected entity.
    
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
    return await select_response_builder(client, event)
