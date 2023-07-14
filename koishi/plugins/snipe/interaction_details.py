__all__ = ()

from hata import Client

from ...bots import SLASH_CLIENT

from .choice_type import ChoiceTypeEmoji, ChoiceTypeReaction, ChoiceTypeSoundboardSound, ChoiceTypeSticker
from .component_translate_tables import DETAILS_DISABLE
from .constants import (
    CUSTOM_ID_SNIPE_DETAILS_EMOJI, CUSTOM_ID_SNIPE_DETAILS_REACTION, CUSTOM_ID_SNIPE_DETAILS_SOUNDBOARD_SOUND,
    CUSTOM_ID_SNIPE_DETAILS_STICKER
)
from .embed_parsers import parse_source_message_url
from .helpers import translate_components


async def snipe_interaction_respond_with_details(client, event, choice_type):
    """
    Shared function used by entity detail shower component commands.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    event : ``InteractionEvent``
        The received interaction event.
    
    choice_type : `type<ChoiceTypeBase>`
        Choice type.
    """
    await client.interaction_component_acknowledge(event, wait = False)
    
    entity_id, entity = await choice_type.parse_and_get_entity_id_and_entity(client, event)
    if (entity is None):
        return
    
    embed = await choice_type.build_embed(entity, client, event, parse_source_message_url(event.message), True)
     
    await client.interaction_response_message_edit(
        event,
        embed = embed,
        components = translate_components(event.message.iter_components(), DETAILS_DISABLE),
    )


@SLASH_CLIENT.interactions(custom_id = CUSTOM_ID_SNIPE_DETAILS_EMOJI)
async def snipe_interaction_emoji_details(client, event):
    """
    Changes the embed to show the emoji's details. Also disabled the `details` button.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    event : ``InteractionEvent``
        The received interaction event.
    """
    await snipe_interaction_respond_with_details(client, event, ChoiceTypeEmoji)


@SLASH_CLIENT.interactions(custom_id = CUSTOM_ID_SNIPE_DETAILS_REACTION)
async def snipe_interaction_reaction_details(client, event):
    """
    Changes the embed to show the reaction's details. Also disabled the `details` button.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    event : ``InteractionEvent``
        The received interaction event.
    """
    await snipe_interaction_respond_with_details(client, event, ChoiceTypeReaction)


@SLASH_CLIENT.interactions(custom_id = CUSTOM_ID_SNIPE_DETAILS_SOUNDBOARD_SOUND)
async def snipe_interaction_soundboard_sound_details(client, event):
    """
    Changes the embed to show the soundboard sound's details. Also disabled the `details` button.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    event : ``InteractionEvent``
        The received interaction event.
    """
    await snipe_interaction_respond_with_details(client, event, ChoiceTypeSoundboardSound)


@SLASH_CLIENT.interactions(custom_id = CUSTOM_ID_SNIPE_DETAILS_STICKER)
async def snipe_interaction_sticker_details(client, event):
    """
    Changes the embed to show the sticker's details. Also disabled the `details` button.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    event : ``InteractionEvent``
        The received interaction event.
    """
    await snipe_interaction_respond_with_details(client, event, ChoiceTypeSticker)
