__all__ = ()

from math import floor, log10

from hata import DiscordException, ERROR_CODES, ZEROUSER
from hata.ext.slash import Button, Row

from ...bot_utils.constants import EMOJI__HEART_CURRENCY
from ...bot_utils.user_getter import get_user

from .constants import (
    BUTTON_CLOSE, BUTTON_PAGE_NEXT_DISABLED, BUTTON_PAGE_PREVIOUS_DISABLED, CUSTOM_ID_PAGE_BASE, EMOJI_PAGE_NEXT,
    EMOJI_PAGE_PREVIOUS, PAGE_SIZE, STYLE_HEARTS, STYLE_NAME, STYLE_NUMBER, STYLE_RESET
)


async def process_entries(page_index, entries):
    """
    Processed the given entries.
    
    This function is a coroutine.
    
    Parameters
    ----------
    page_index : `int`
        Page index (0 based).
    entries : `list<sqlalchemy.engine.result.RowProxy>`
        Raw entries to process.
    
    Returns
    -------
    processed_entries : `list<(int, int, ClientUserBase)`
    """
    processed_entries = []

    for number, (user_id, total_hearts) in enumerate(entries, (page_index * 20) + 1):
        try:
            user = await get_user(user_id)
        except BaseException as err:
            if isinstance(err, ConnectionError):
                return
            
            if isinstance(err, DiscordException):
                if err.code == ERROR_CODES.unknown_user:
                    user = ZEROUSER
                else:
                    raise
            
            else:
                raise
        
        processed_entries.append((number, total_hearts, user))
    
    return processed_entries


def build_content(page_index, processed_entries):
    """
    Builds a page_number of entries.
    
    Parameters
    ----------
    page_index : `int`
        Page index (0 based).
    processed_entries : `list<(int, int, ClientUserBase)`
        Professed entries.
    
    Returns
    -------
    content : `str`
    """
    content_parts = [
        EMOJI__HEART_CURRENCY.as_emoji,
        ' **Top-list** ',
        EMOJI__HEART_CURRENCY.as_emoji,
        ' *[Page ',
        str(page_index + 1),
        ']*\n```ansi\n',
    ]
    
    if processed_entries:
        index_adjust = floor(log10(page_index * PAGE_SIZE + len(processed_entries))) + 1
        hearts_adjust = floor(log10(max(entry[1] for entry in processed_entries))) + 1
        
        for number, total_hearts, user in processed_entries:
            content_parts.append(STYLE_NUMBER)
            content_parts.append(str(number).rjust(index_adjust))
            content_parts.append(STYLE_RESET)
            content_parts.append('.: ')
            content_parts.append(STYLE_HEARTS)
            content_parts.append(str(total_hearts).rjust(hearts_adjust))
            content_parts.append(' ')
            content_parts.append(STYLE_NAME)
            content_parts.append(user.full_name)
            content_parts.append('\n')
    else:
        content_parts.append('no result\n')
    
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
            emoji = EMOJI_PAGE_PREVIOUS,
            custom_id = f'{CUSTOM_ID_PAGE_BASE}{page_index - 1!s}',
        )
    
    if entry_count < PAGE_SIZE:
        button_next = BUTTON_PAGE_NEXT_DISABLED
    else:
        button_next = Button(
            emoji = EMOJI_PAGE_NEXT,
            custom_id = f'{CUSTOM_ID_PAGE_BASE}{page_index + 1!s}',
        )
    
    return Row(button_previous, button_next, BUTTON_CLOSE)
