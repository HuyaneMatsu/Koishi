__all__ = ()

from hata import Client, DiscordException, ERROR_CODES

from ...bots import SLASH_CLIENT

from .component_translate_tables import DM_DISABLE
from .constants import CUSTOM_ID_SNIPE_DM
from .helpers import get_message_attachment, translate_components


@SLASH_CLIENT.interactions(custom_id = CUSTOM_ID_SNIPE_DM)
async def snipe_interaction_dm(client, event):
    """
    Dm-s the message to the user.
    
    This function is a coroutine.
    
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
    file = await get_message_attachment(client, message)
    channel = await client.channel_private_create(event.user)
    try:
        await client.message_create(
            channel,
            embed = embed,
            components = translate_components(message.iter_components(), DM_DISABLE),
            file = file
        )
    except DiscordException as err:
        if err.code == ERROR_CODES.cannot_message_user: # user has dm-s disabled:
            await client.interaction_followup_message_create(
                event,
                'Could not deliver direct message.',
                show_for_invoking_user_only = True
            )
        
        else:
            raise
