__all__ = ()

from hata import Client, DiscordException, ERROR_CODES

from .constants import (
    BUTTON_SNIPE_ACTIONS_DISABLED, BUTTON_SNIPE_ADD_DISABLED, BUTTON_SNIPE_DM_DISABLED, BUTTON_SNIPE_EDIT_DISABLED,
    BUTTON_SNIPE_REMOVE_DISABLED, BUTTON_SNIPE_REVEAL_DISABLED, CUSTOM_ID_SNIPE_ACTIONS_EMOJI,
    CUSTOM_ID_SNIPE_ACTIONS_STICKER, CUSTOM_ID_SNIPE_ADD_EMOJI, CUSTOM_ID_SNIPE_ADD_STICKER, CUSTOM_ID_SNIPE_DM,
    CUSTOM_ID_SNIPE_EDIT_EMOJI, CUSTOM_ID_SNIPE_EDIT_STICKER, CUSTOM_ID_SNIPE_REMOVE_EMOJI,
    CUSTOM_ID_SNIPE_REMOVE_STICKER, CUSTOM_ID_SNIPE_REVEAL
)
from .helpers import translate_components


SLASH_CLIENT: Client

DISABLED_TABLE_DM = {
    CUSTOM_ID_SNIPE_REVEAL: BUTTON_SNIPE_REVEAL_DISABLED,
    CUSTOM_ID_SNIPE_DM: BUTTON_SNIPE_DM_DISABLED,
    CUSTOM_ID_SNIPE_ACTIONS_EMOJI: BUTTON_SNIPE_ACTIONS_DISABLED,
    CUSTOM_ID_SNIPE_ACTIONS_STICKER: BUTTON_SNIPE_ACTIONS_DISABLED,
    CUSTOM_ID_SNIPE_ADD_EMOJI: BUTTON_SNIPE_ADD_DISABLED,
    CUSTOM_ID_SNIPE_ADD_STICKER: BUTTON_SNIPE_ADD_DISABLED,
    CUSTOM_ID_SNIPE_REMOVE_EMOJI: BUTTON_SNIPE_REMOVE_DISABLED,
    CUSTOM_ID_SNIPE_REMOVE_STICKER: BUTTON_SNIPE_REMOVE_DISABLED,
    CUSTOM_ID_SNIPE_EDIT_EMOJI: BUTTON_SNIPE_EDIT_DISABLED,
    CUSTOM_ID_SNIPE_EDIT_STICKER: BUTTON_SNIPE_EDIT_DISABLED,
}


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
    channel = await client.channel_private_create(event.user)
    try:
        await client.message_create(
            channel,
            embed = embed,
            components = translate_components(message.iter_components(), DISABLED_TABLE_DM),
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
