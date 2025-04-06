__all__ = ()

from math import floor, log10

from hata import Embed
from hata.ext.slash import Button, InteractionResponse, Row

from ...bot_utils.constants import EMOJI__HEART_CURRENCY

from .constants import (
    BUTTON_CLOSE, BUTTON_PAGE_NEXT_DISABLED, BUTTON_PAGE_PREVIOUS_DISABLED, CUSTOM_ID_PAGE_BASE, EMOJI_PAGE_NEXT,
    EMOJI_PAGE_PREVIOUS, PAGE_SIZE, STYLE_HEARTS, STYLE_NAME, STYLE_NUMBER
)


def build_content(page_index, processed_entries, guild_id):
    """
    Builds a page_number of entries.
    
    Parameters
    ----------
    page_index : `int`
        Page index (0 based).
    
    processed_entries : `list<(int, int, ClientUserBase)`
        Professed entries.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    content : `str`
    """
    content_parts = ['```']
    
    if processed_entries:
        content_parts.append('ansi\n')
        
        index_adjust = floor(log10(page_index * PAGE_SIZE + len(processed_entries))) + 1
        hearts_adjust = floor(log10(max(entry[1] for entry in processed_entries))) + 1
        
        for number, total_hearts, user in processed_entries:
            content_parts.append(STYLE_NUMBER)
            content_parts.append(str(number).rjust(index_adjust))
            content_parts.append('.: ')
            content_parts.append(STYLE_HEARTS)
            content_parts.append(str(total_hearts).rjust(hearts_adjust))
            content_parts.append(' ')
            content_parts.append(STYLE_NAME)
            content_parts.append(user.name_at(guild_id))
            content_parts.append('\n')
    else:
        content_parts.append('\nno result\n')
    
    content_parts.append('```')
    
    return ''.join(content_parts)


def build_components(page_index, entry_count):
    """
    Builds components for the current page.
    
    Parameters
    ----------
    page_index : `int`
        Page index (0 based).
    entry_count : `int`
        The entry count on this page.
    
    Returns
    -------
    components : ``Component``
    """
    if page_index <= 0:
        button_previous = BUTTON_PAGE_PREVIOUS_DISABLED
    else:
        button_previous = Button(
            f'Page {page_index}',
            EMOJI_PAGE_PREVIOUS,
            custom_id = f'{CUSTOM_ID_PAGE_BASE}{page_index - 1!s}',
        )
    
    if entry_count < PAGE_SIZE:
        button_next = BUTTON_PAGE_NEXT_DISABLED.copy_with(
            label = f'Page {page_index + 2}'
        )
    else:
        button_next = Button(
            f'Page {page_index + 2}',
            emoji = EMOJI_PAGE_NEXT,
            custom_id = f'{CUSTOM_ID_PAGE_BASE}{page_index + 1!s}',
        )
    
    return Row(button_previous, button_next, BUTTON_CLOSE)


def build_top_list_response(page_index, entries, guild_id):
    """
    Makes top list response.
    
    Parameters
    ----------
    page_index : `int`
        The page's index to make the response for.
    
    entries : `list<(int, int, ClientUserBase)`
        Processed entries.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    embed = Embed(
        f'{EMOJI__HEART_CURRENCY} Top-list {EMOJI__HEART_CURRENCY}',
        build_content(page_index, entries, guild_id),
    ).add_field(
        'Page',
        (
            f'```\n'
            f'{page_index + 1}\n'
            f'```'
        ),
        True,
    ).add_field(
        'Sort order',
        (
            f'```\n'
            f'decreasing\n'
            f'```'
        ),
        True,
    )
    
    components = build_components(page_index, len(entries))
    
    return InteractionResponse(
        embed = embed,
        components = components,
    )
