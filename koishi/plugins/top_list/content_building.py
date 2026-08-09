__all__ = ()

from ...bot_utils.constants import EMOJI__HEART_CURRENCY

from .constants import (
    PAGE_SIZE, STYLE_VALUE, STYLE_NAME, STYLE_NUMBER, TOP_LIST_TYPE_BALANCE, TOP_LIST_TYPE_CREDIBILITY
)


def produce_top_list_description(page_index, processed_entries, guild_id):
    """
    Produces top list description.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    page_index : `int`
        Page index.
    
    processed_entries : ``list<(ClientUserBase, int)>``
        Professed entries.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Yields
    -------
    part : `str`
    """
    yield '```ansi\n'
    
    offset = PAGE_SIZE * page_index
    offset_adjust = len(str(len(processed_entries) + offset))
    value_adjust = len(str(max((entry[1] for entry in processed_entries), default = 0)))
    
    for user, value in processed_entries:
        yield STYLE_NUMBER
        offset += 1
        offset_string = str(offset)
        adjust = offset_adjust - len(offset_string)
        if adjust:
            yield ' ' * adjust
        yield offset_string
        yield '.: '
        yield STYLE_VALUE
        value_string = str(value)
        adjust = value_adjust - len(value_string)
        if adjust:
            yield ' ' * adjust
        yield value_string
        yield ' '
        yield STYLE_NAME
        yield user.name_at(guild_id)
        yield '\n'
    
    yield '```'


def produce_top_list_header(top_list_type, page_index):
    """
    Produces top list header.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    top_list_type : `int`
        Top list's type.
    
    page_index : `int`
        Page index.
    
    Yields
    ------
    part : `str`
    """
    yield '# '
    
    if top_list_type == TOP_LIST_TYPE_BALANCE:
        prefix = EMOJI__HEART_CURRENCY.as_emoji
    elif top_list_type ==  TOP_LIST_TYPE_CREDIBILITY:
        prefix = 'Credibility'
    else:
        prefix = 'Pudding'
    yield prefix
    
    yield ' top-list\n\nPage: '
    yield str(page_index + 1)
