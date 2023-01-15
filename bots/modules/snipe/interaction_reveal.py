__all__ = ()

from hata import Client

from .constants import BUTTON_SNIPE_REVEAL_DISABLED, CUSTOM_ID_SNIPE_REVEAL
from .helpers import translate_components

SLASH_CLIENT: Client

DISABLED_TABLE_COVERT = {
    CUSTOM_ID_SNIPE_REVEAL: BUTTON_SNIPE_REVEAL_DISABLED,
}


@SLASH_CLIENT.interactions(custom_id = CUSTOM_ID_SNIPE_REVEAL)
async def snipe_message_reveal(client, event):
    """
    Flips the interaction's message.
    
    This function is a coroutine,
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    """
    message = event.message
    if message is None:
        return
    
    embed = message.embed
    if embed is None:
        return
    
    await client.interaction_component_acknowledge(event, wait = False)
    await client.interaction_followup_message_create(
        event,
        embed = embed,
        components = translate_components(event.message.iter_components(), DISABLED_TABLE_COVERT),
    )
    await client.interaction_response_message_delete(event)
