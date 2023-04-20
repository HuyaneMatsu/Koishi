__all__ = ()

from hata import Client

from .component_translate_tables import REVEAL_DISABLE
from .constants import CUSTOM_ID_SNIPE_REVEAL
from .helpers import translate_components


SLASH_CLIENT: Client


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
        components = translate_components(event.message.iter_components(), REVEAL_DISABLE),
    )
    await client.interaction_response_message_delete(event)
