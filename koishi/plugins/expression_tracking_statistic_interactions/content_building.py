__all__ = ()

from math import floor, log

from hata import EMOJIS, STICKERS

from ..expression_tracking import (
    ACTION_TYPE_EMOJI_CONTENT, ACTION_TYPE_EMOJI_REACTION, ACTION_TYPE_STICKER, ENTITY_FILTER_RULE_EMOJI_ANIMATED,
    ENTITY_FILTER_RULE_EMOJI_STATIC
)

from .constants import MODE_GUILD_IN, MODE_GUILD_OF
from .helpers import unpack_action_types


def produce_header(
    guild,
    mode,
    action_types_packed,
    entity_filter_rule,
    months,
    page_index,
    page_size,
    order_decreasing,
):
    """
    Produces header.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    guild : ``None | Guild``
        The guild in context.
    
    mode : `int`
        The usage mode to respond with.
    
    action_types_packed : `int`
        The action types packed.
    
    entity_filter_rule : `int`
        Entity filter rule for detailed filtering.
    
    months : `int`
        The amount of months to look back.
    
    page_index : `int`
        The page's index to display.
    
    page_size : `int`
        The page's size to display.
    
    order_decreasing : `bool`
        Whether to order in a decreasing order.
    
    Yields
    ------
    part : `str`
    """
    # title
    yield '# '
    
    if mode == MODE_GUILD_OF:
        yield 'Of '
        yield guild.name
    
    elif mode == MODE_GUILD_IN:
        yield 'In '
        yield guild.name
    
    else:
        yield 'Unknown'
    
    yield '\'s '
    
    action_types = unpack_action_types(action_types_packed)
    if (ACTION_TYPE_EMOJI_CONTENT in action_types) or (ACTION_TYPE_EMOJI_REACTION in action_types):
        entity_type_name_plural = 'emojis'
        
        if (ACTION_TYPE_EMOJI_CONTENT not in action_types):
            location_name = 'reactions'
        elif (ACTION_TYPE_EMOJI_REACTION not in action_types):
            location_name = 'content'
        else:
            location_name = None
        
        if entity_filter_rule == ENTITY_FILTER_RULE_EMOJI_ANIMATED:
            filter_rule_name = 'animated'
        elif entity_filter_rule == ENTITY_FILTER_RULE_EMOJI_STATIC:
            filter_rule_name = 'static'
        else:
            filter_rule_name = None
        
    
    elif (ACTION_TYPE_STICKER in action_types):
        entity_type_name_plural = 'stickers'
        location_name = None
        filter_rule_name = None
    
    else:
        entity_type_name_plural = 'shrimp fries'
        location_name = None
        filter_rule_name = None
    
    if (filter_rule_name is not None):
        yield filter_rule_name
        yield ' '
    yield entity_type_name_plural
    if (location_name is not None):
        yield ' in '
        yield location_name
    
    
    # Other information
    yield '\nPage: '
    yield str(page_index + 1)
    yield '; page size: '
    yield str(page_size)
    yield '; months: '
    yield str(months)
    yield '; order: '
    yield ('decreasing' if order_decreasing else 'increasing')


def _get_entity_emoji(entity_id):
    """
    Gets the entity for an emoji identifier.
    
    Parameters
    ----------
    entity_id : `int`
        Entity identifier.
    
    Returns
    -------
    entity : ``None | Emoji``
    """
    return EMOJIS.get(entity_id, None)


def _get_entity_sticker(entity_id):
    """
    Gets the entity for an sticker identifier.
    
    Parameters
    ----------
    entity_id : `int`
        Entity identifier.
    
    Returns
    -------
    entity : ``None | Sticker``
    """
    return STICKERS.get(entity_id, None)


def _get_representation_emoji(client, entity):
    """
    Gets the representation of an emoji.
    
    Parameters
    ----------
    client : ``ClientUserBase``
        The client rendering this message.
    
    entity : ``Emoji``
        The entity to get representation of.
    
    Returns
    -------
    can_grave_and_representation : `(bool, str)`
    """
    if client.can_use_emoji(entity):
        can_grave = False
        representation = entity.as_emoji
    else:
        can_grave = True
        representation = entity.name
        if entity.require_colons:
            representation = f':{representation}:'

    return can_grave, representation


def _get_representation_sticker(client, entity):
    """
    Gets the representation of a sticker.
    
    Parameters
    ----------
    client : ``ClientUserBase``
        The client rendering this message.
    
    entity : ``Sticker``
        The entity to get representation of.
    
    Returns
    -------
    can_grave_and_representation : `(bool, str)`
    """
    return True, entity.name


def produce_guild_of_description(client, action_types_packed, entries):
    """
    Produces guild-of description.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    client : ``ClientUserBase``
        The client rendering this message.
    
    action_types_packed : `int`
        The action types packed.
    
    entries : `list<(int, int, int)>`
        Entries to render.
    
    Yields
    ------
    part : `str`
    """
    action_types = unpack_action_types(action_types_packed)
    if (ACTION_TYPE_EMOJI_CONTENT in action_types) or (ACTION_TYPE_EMOJI_REACTION in action_types):
        entity_name = 'Emojis'
        get_entity = _get_entity_emoji
        get_representation = _get_representation_emoji
    else:
        entity_name = 'Stickers'
        get_entity = _get_entity_sticker
        get_representation = _get_representation_sticker
    
    total_highest = max(entry[1] for entry in entries)
    if total_highest == 0:
        highest_number_representation_length = 1
    else:
        highest_number_representation_length = 1 + floor(log(total_highest, 10))
        
    column_width_total = max(len('Total'), highest_number_representation_length)
    column_width_internal = max(len('Internal'), highest_number_representation_length)
    column_width_external = max(len('External'), highest_number_representation_length)
    
    yield '`'
    
    space_length = column_width_total - len('Total')
    if space_length:
        yield ' ' * space_length
    yield 'Total'
    
    yield ' | '
    
    space_length = column_width_internal - len('Internal')
    if space_length:
        yield ' ' * space_length
    yield 'Internal'
    
    yield ' | '
    
    space_length = column_width_external - len('External')
    if space_length:
        yield ' ' * space_length
    yield 'External'
    
    yield ' | '
    
    yield entity_name
    yield '`'
    
    for entity_id, total, internal in entries:
        yield '\n`'
        
        # Produce total
        total_string = str(total)
        space_length = column_width_total - len(total_string)
        if space_length:
            yield ' ' * space_length
        yield total_string
        
        yield ' | '
        
        # Produce internal
        internal_string = str(internal)
        space_length = column_width_internal - len(internal_string)
        if space_length:
            yield ' ' * space_length
        yield internal_string
        
        yield ' | '
        
        # Produce external
        external_string = str(total - internal)
        space_length = column_width_external - len(external_string)
        if space_length:
            yield ' ' * space_length
        yield external_string
        
        yield ' | '
        
        # Produce representation
        entity = get_entity(entity_id)
        if entity is None:
            can_grave = True
            representation = str(entity_id)
        else:
            can_grave, representation = get_representation(client, entity)
        
        if can_grave:
            yield representation
            yield '`'
        else:
            yield '` '
            yield representation


def produce_guild_in_description(client, guild_id, action_types_packed, entries):
    """
    Produces guild-in description.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    client : ``ClientUserBase``
        The client rendering this message.
    
    guild_id : `int`
        The local guild's identifier.
    
    action_types_packed : `int`
        The action types packed.
    
    entries : `list<(int, int)>`
        Entries to render.
    
    Yields
    ------
    part : `str`
    """
    action_types = unpack_action_types(action_types_packed)
    if (ACTION_TYPE_EMOJI_CONTENT in action_types) or (ACTION_TYPE_EMOJI_REACTION in action_types):
        entity_name = 'Emojis'
        get_entity = _get_entity_emoji
        get_representation = _get_representation_emoji
    else:
        entity_name = 'Stickers'
        get_entity = _get_entity_sticker
        get_representation = _get_representation_sticker
    
    total_highest = max(entry[1] for entry in entries)
    if total_highest == 0:
        highest_number_representation_length = 1
    else:
        highest_number_representation_length = 1 + floor(log(total_highest, 10))
        
    column_width_total = max(len('Total'), highest_number_representation_length)
    column_width_source = max(len('internal'), len('external'))
    
    yield '`'
    space_length = column_width_total - len('Total')
    if space_length:
        yield ' ' * space_length
    yield 'Total'
    
    yield ' | '
    
    space_length = column_width_source - len('Source')
    if space_length:
        yield ' ' * space_length
    yield 'Source'
    
    yield ' | '
    
    yield entity_name
    yield '`'
    
    for entity_id, total in entries:
        yield '\n`'
        
        # Produce total
        total_string = str(total)
        space_length = column_width_total - len(total_string)
        if space_length:
            yield ' ' * space_length
        yield total_string
        yield ' | '
        
        # Produce source
        entity = get_entity(entity_id)
        if entity is None:
            source = 'external'
        else:
            source = 'internal' if entity.guild_id == guild_id else 'external'
        
        space_length = column_width_source - len(source)
        if space_length:
            yield ' ' * space_length
        yield source
        
        yield ' | '
        
        # produce representation
        if entity is None:
            can_grave = True
            representation = str(entity_id)
        else:
            can_grave, representation = get_representation(client, entity)
        
        if can_grave:
            yield representation
            yield '`'
        else:
            yield '` '
            yield representation
