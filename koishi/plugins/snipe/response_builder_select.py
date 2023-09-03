__all__ = ()

import re

from hata import Emoji, UNICODE_TO_EMOJI, parse_emoji
from hata.ext.slash import InteractionResponse

from .cache_soundboard_sound import get_soundboard_sound
from .cache_sticker import get_sticker
from .choice import Choice
from .choice_type import ChoiceTypeEmoji, ChoiceTypeReaction, ChoiceTypeSoundboardSound, ChoiceTypeSticker
from .embed_parsers import parse_source_message_url
from .helpers import are_actions_allowed_for_entity, is_event_user_same, translate_components


CHOICE_RP = re.compile('(e|s|r|o)\\:(?:(\\d+)\\:)?(\\d+)\\:([^\\:]*)\\:(|0|1)')


def is_message_detailed(message):
    """
    Returns whether the message is showing detailed entity information.
    
    Parameters
    ----------
    message : ``Message``
        The message to check.
    
    Returns
    -------
    is_message_detailed : `bool`
    """
    embed = message.embed
    if (embed is None):
        return False
    
    fields = embed.fields
    if (fields is None):
        return False
    
    return (len(fields) > 2)


ANIMATED_RESOLUTION = {
    '0': False, 
    '1': True,
}


async def choice_parser(client, event):
    """
    Parses the choice out from the given event's select option.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``Event``
        The received event.
    
    Returns
    -------
    choice : `None`, ``Choice``
    """
    selected_values = event.values
    if (selected_values is None):
        return None
    
    match = CHOICE_RP.fullmatch(selected_values[0])
    if match is None:
        return None
    
    entity_kind, guild_id, entity_id, entity_name, animated = match.groups()
    
    entity_id = int(entity_id)
    
    # At the case of old choices, `guild_id` can be matched as `None`.
    if guild_id is None:
        guild_id = 0
    else:
        guild_id = int(guild_id)
    
    if entity_kind in ('e', 'r'):
        if entity_id:
            entity = Emoji._create_partial(entity_id, entity_name, ANIMATED_RESOLUTION.get(animated, False))
        else:
            try:
                entity = UNICODE_TO_EMOJI.get(entity_name, None)
            except KeyError:
                return None
        
        if entity_kind == 'e':
            choice_type = ChoiceTypeEmoji
        else:
            choice_type = ChoiceTypeReaction
    
    elif entity_kind == 's':
        entity = await get_sticker(client, entity_id)
        if entity is None:
            return None
        
        choice_type = ChoiceTypeSticker
    
    elif entity_kind == 'o':
        entity = await get_soundboard_sound(client, guild_id, entity_id)
        if entity is None:
            return None
        
        choice_type = ChoiceTypeSoundboardSound
        
    else:
        return None
    
    return Choice(entity, choice_type)


async def select_response_builder(client, event):
    """
    Creates a select response.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received event.
    
    Returns
    -------
    response : `None`, ``InteractionResponse``
    """
    message = event.message
    if message is None:
        return
    
    if not is_event_user_same(event, message):
        return
    
    detailed = is_message_detailed(message)
    
    choice = await choice_parser(client, event)
    if choice is None:
        return
    
    entity, choice_type = choice
    embeds = await choice_type.build_embeds(entity, client, event, parse_source_message_url(message), detailed)
    
    file = await choice_type.get_file(entity, client)
    
    guild_id = event.guild_id
    if (guild_id == 0) or (not are_actions_allowed_for_entity(entity)):
        translate_table = choice_type.select_table_disabled
    elif (guild_id == entity.guild_id):
        translate_table = choice_type.select_table_inside
    else:
        translate_table = choice_type.select_table_outside
    
    return InteractionResponse(
        embed = embeds,
        components = translate_components(message.iter_components(), translate_table),
        file = file,
    )
