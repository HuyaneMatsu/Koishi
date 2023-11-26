__all__ = ()

from hata import Client

from ...bots import FEATURE_CLIENTS

from .component_translate_tables import REVEAL_DISABLE
from .constants import CUSTOM_ID_SNIPE_REVEAL
from .helpers import get_message_attachment, translate_components


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_SNIPE_REVEAL)
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
    
    embeds = message.embeds
    if embeds is None:
        return
    
    await client.interaction_component_acknowledge(event, wait = False)
    file = await get_message_attachment(client, message)
    await client.interaction_followup_message_create(
        event,
        embed = embeds,
        components = translate_components(event.message.iter_components(), REVEAL_DISABLE),
        file = file,
    )
    await client.interaction_response_message_delete(event)
