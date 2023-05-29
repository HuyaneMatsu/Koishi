__all__ = ()

import re

from hata import Emoji, UNICODE_TO_EMOJI, parse_emoji
from hata.ext.slash import InteractionResponse

from .cache_sticker import get_sticker
from .choice import Choice
from .choice_type import ChoiceTypeEmoji, ChoiceTypeReaction, ChoiceTypeSticker
from .embed_parsers import parse_source_message_url
from .helpers import are_actions_allowed_for_entity, is_event_user_same, translate_components

CHOICE_RP = re.compile('(e|s|r)\\:(\\d+)\\:([^\\:]*)\\:(|0|1)')


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
    choice : `None`, ``ChoiceBase``
    """
    selected_values = event.values
    if (selected_values is None):
        return None
    
    match = CHOICE_RP.fullmatch(selected_values[0])
    if match is None:
        return None
    
    entity_kind, entity_id, entity_name, animated = match.groups()
    
    entity_id = int(entity_id)
    
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
    
    else:
        entity = await get_sticker(client, entity_id)
        if entity is None:
            return None
        
        choice_type = ChoiceTypeSticker
    
    return Choice(entity, choice_type)


async def select_option_parser_emoji(client, event):
    """
    Parses the emoji out from the given event's select option.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``Event``
        The received event.
    
    Returns
    -------
    emoji : `None`, ``Emoji``
    """
    selected_emojis = event.values
    if (selected_emojis is None):
        return None
    
    selected_emoji = selected_emojis[0]
    return parse_emoji(selected_emoji)


async def select_option_parser_sticker(client, event):
    """
    Parses the sticker out from the given event's select option.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``Event``
        The received event.
    
    Returns
    -------
    sticker : `None`, ``Sticker``
    """
    selected_stickers = event.values
    if (selected_stickers is None):
        return None
    
    selected_sticker = selected_stickers[0]
    try:
        selected_sticker_id = int(selected_sticker)
    except ValueError:
        return None
    
    return await get_sticker(client, selected_sticker_id)


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
    
    embed = await choice.build_embed(client, event, parse_source_message_url(message), detailed)
    
    guild_id = event.guild_id
    if (guild_id == 0) or (not are_actions_allowed_for_entity(choice.entity)):
        translate_table = choice.select_table_disabled
    elif (guild_id == choice.entity.guild_id):
        translate_table = choice.select_table_inside
    else:
        translate_table = choice.select_table_outside
    
    return InteractionResponse(
        embed = embed,
        components = translate_components(message.iter_components(), translate_table),
    )
    
    return select_response_response_builder_generic
