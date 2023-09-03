__all__ = ()

from hata import Embed
from hata.ext.slash import Button, InteractionResponse, Row

from .constants import (
    BUTTON_CLOSE, BUTTON_PAGE_NEXT_DISABLED, BUTTON_PAGE_PREVIOUS_DISABLED, CUSTOM_ID_PAGE_BASE, EMOJI_PAGE_NEXT,
    EMOJI_PAGE_PREVIOUS, NAME_ALL, NAME_ALL_HEADER, NAME_BAN, NAME_BAN_HEADER, NAME_KICK, NAME_KICK_HEADER, NAME_MUTE,
    NAME_MUTE_HEADER, PAGE_MAX, PAGE_MIN, PAGE_SIZE, STYLE_ALL, STYLE_BAN, STYLE_FOCUS, STYLE_KICK, STYLE_MUTE,
    STYLE_NAME, STYLE_NUMBER, TYPE_BAN, TYPE_KICK, TYPE_MUTE, TYPE_TO_NAME
)
from .helpers import get_integer_length


def build_content(page_index, entries, sort_by):
    """
    Builds the top-list listing.
    
    Parameters
    ----------
    page_index : `int`
        The page to show. Used to calculate entry index.
    entries : `list` of `tuple` (``ClientUserBase``, ``ActionCounter``)
        Top list entries.
    sort_by : `int`
        The actions' identifier to sort by. Used to highlight that specific row.
    
    Returns
    -------
    listing : `str`
    """
    style_ban = STYLE_BAN
    style_kick = STYLE_KICK
    style_mute = STYLE_MUTE
    style_all = STYLE_ALL
    
    if sort_by == TYPE_BAN:
        style_ban = STYLE_FOCUS
    elif sort_by == TYPE_KICK:
        style_kick = STYLE_FOCUS
    elif sort_by == TYPE_MUTE:
        style_mute = STYLE_FOCUS
    else:
        style_all = STYLE_FOCUS
    
    result_parts = ['```']
    
    # We only need a chunk of it here.
    entries = entries[page_index * PAGE_SIZE : (page_index + 1) * PAGE_SIZE]
    
    if entries:
        result_parts.append('ansi\n')
    
        index_adjust = get_integer_length(page_index * PAGE_SIZE + len(entries))
        all_adjust = max(get_integer_length(max(item[1].all for item in entries)), len(NAME_ALL))
        ban_adjust = max(get_integer_length(max(item[1].ban for item in entries)), len(NAME_BAN))
        kick_adjust = max(get_integer_length(max(item[1].kick for item in entries)), len(NAME_KICK))
        mute_adjust = max(get_integer_length(max(item[1].mute for item in entries)), len(NAME_MUTE))
        
        result_parts.append(' ' * index_adjust)
        result_parts.append('   ')
        result_parts.append(style_all)
        result_parts.append(NAME_ALL_HEADER.rjust(all_adjust))
        result_parts.append(' ')
        result_parts.append(style_ban)
        result_parts.append(NAME_BAN_HEADER.rjust(ban_adjust))
        result_parts.append(' ')
        result_parts.append(style_kick)
        result_parts.append(NAME_KICK_HEADER.rjust(kick_adjust))
        result_parts.append(' ')
        result_parts.append(style_mute)
        result_parts.append(NAME_MUTE_HEADER.rjust(mute_adjust))
        result_parts.append('\n')
        
        for index, (user, counter) in enumerate(entries, 1 + page_index * PAGE_SIZE):
            result_parts.append(STYLE_NUMBER)
            result_parts.append(str(index).rjust(index_adjust))
            result_parts.append('.: ')
            result_parts.append(style_all)
            result_parts.append(str(counter.all).rjust(all_adjust))
            result_parts.append(' ')
            result_parts.append(style_ban)
            result_parts.append(str(counter.ban).rjust(ban_adjust))
            result_parts.append(' ')
            result_parts.append(style_kick)
            result_parts.append(str(counter.kick).rjust(kick_adjust))
            result_parts.append(' ')
            result_parts.append(style_mute)
            result_parts.append(str(counter.mute).rjust(mute_adjust))
            result_parts.append(' ')
            result_parts.append(STYLE_NAME)
            result_parts.append(user.full_name)
            result_parts.append('\n')
    else:
        result_parts.append('\nno result\n')
    
    result_parts.append('```')
    return ''.join(result_parts)


def build_components(page_index, entry_count, sort_by, days):
    """
    Builds top-list components.
    
    Parameters
    ----------
    page_index : `int`
        Current page index.
    entry_count : `int`
        Total entry count.
    sort_by : `int`
        The actions' identifier to sort by.
    days : `int`
        The days to query for.
    
    Returns
    -------
    components : ``Component``
    """
    if page_index == PAGE_MIN:
        button_back = BUTTON_PAGE_PREVIOUS_DISABLED
    else:
        button_back = Button(
            f'Page {page_index}',
            EMOJI_PAGE_PREVIOUS,
            custom_id = f'{CUSTOM_ID_PAGE_BASE}{page_index - 1};s={sort_by!s};d={days!s}',
        )
    
    if page_index == PAGE_MAX:
        button_next = BUTTON_PAGE_NEXT_DISABLED
    elif (page_index + 1 ) * PAGE_SIZE >= entry_count:
        button_next = BUTTON_PAGE_NEXT_DISABLED.copy_with(
            label = f'Page {page_index + 2}'
        )
    else:
        button_next = Button(
            f'Page {page_index + 2}',
            EMOJI_PAGE_NEXT,
            custom_id = f'{CUSTOM_ID_PAGE_BASE}{page_index + 1 !s};s={sort_by!s};d={days!s}',
        )
    
    return Row(button_back, button_next, BUTTON_CLOSE)


def build_top_list_response(page_index, entries, sort_by, days):
    """
    Builds the top-list response.
    
    Parameters
    ----------
    page_index : `int`
        The page to show.
    entries : `list` of `tuple` (``ClientUserBase``, ``ActionCounter``)
        Top list entries.
    sort_by : `int`
        The actions' identifier to sort by.
    days : `int`
        The days to query for.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    embed = Embed(
        'Mod top-list',
        build_content(page_index, entries, sort_by),
    ).add_field(
        'Sorted by',
        (
            f'```\n'
            f'{TYPE_TO_NAME.get(sort_by, NAME_ALL)}\n'
            f'```'
        ),
        inline = True,
    ).add_field(
        'Days',
        (
            f'```\n'
            f'{days}\n'
            f'```'
        ),
        inline = True,
    ).add_field(
        'Page',
        (
            f'```\n'
            f'{page_index + 1}\n'
            f'```'
        ),
        inline = True,
    )
    
    components = build_components(page_index, len(entries), sort_by, days)
    
    return InteractionResponse(
        embed = embed,
        components = components,
    )
