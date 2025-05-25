import vampytest
from hata import create_button, create_row

from ..builders import build_components
from ..constants import (
    BUTTON_CLOSE, BUTTON_PAGE_NEXT_DISABLED, BUTTON_PAGE_PREVIOUS_DISABLED, CUSTOM_ID_PAGE_BASE, EMOJI_PAGE_NEXT,
    EMOJI_PAGE_PREVIOUS, PAGE_MAX, PAGE_SIZE, TYPE_ALL, TYPE_BAN, TYPE_KICK, TYPE_MUTE
)


def _iter_options():
    yield (
        0,
        PAGE_SIZE,
        TYPE_BAN,
        10,
        create_row(
            BUTTON_PAGE_PREVIOUS_DISABLED,
            BUTTON_PAGE_NEXT_DISABLED.copy_with(
                label = 'Page 2',
            ),
            BUTTON_CLOSE,
        ),
    )
    
    yield (
        0,
        PAGE_SIZE + 1,
        TYPE_BAN,
        10,
        create_row(
            BUTTON_PAGE_PREVIOUS_DISABLED,
            create_button(
                'Page 2',
                EMOJI_PAGE_NEXT,
                custom_id = f'{CUSTOM_ID_PAGE_BASE}{1!s};s={TYPE_BAN!s};d={10!s}',
            ),
            BUTTON_CLOSE,
        ),
    )
    
    yield (
        6,
        6 * PAGE_SIZE,
        TYPE_ALL,
        45,
        create_row(
            create_button(
                'Page 6',
                emoji = EMOJI_PAGE_PREVIOUS,
                custom_id = f'{CUSTOM_ID_PAGE_BASE}{5!s};s={TYPE_ALL!s};d={45!s}',
            ),
            BUTTON_PAGE_NEXT_DISABLED.copy_with(
                label = 'Page 8',
            ),
            BUTTON_CLOSE,
        ),
    )
    
    yield (
        6,
        PAGE_SIZE * 10,
        TYPE_KICK,
        45,
        create_row(
            create_button(
                'Page 6',
                EMOJI_PAGE_PREVIOUS,
                custom_id = f'{CUSTOM_ID_PAGE_BASE}{5!s};s={TYPE_KICK!s};d={45!s}',
            ),
            create_button(
                'Page 8',
                EMOJI_PAGE_NEXT,
                custom_id = f'{CUSTOM_ID_PAGE_BASE}{7!s};s={TYPE_KICK!s};d={45!s}',
            ),
            BUTTON_CLOSE,
        ),
    )
    
    yield (
        PAGE_MAX,
        PAGE_MAX * PAGE_SIZE + 2,
        TYPE_MUTE,
        45,
        create_row(
            create_button(
                f'Page {PAGE_MAX}',
                EMOJI_PAGE_PREVIOUS,
                custom_id = f'{CUSTOM_ID_PAGE_BASE}{PAGE_MAX - 1!s};s={TYPE_MUTE!s};d={45!s}',
            ),
            BUTTON_PAGE_NEXT_DISABLED,
            BUTTON_CLOSE,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_components(page_index, entry_count, sort_by, days):
    """
    Tests whether ``build_components`` works as intended.
    
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
    output : ``Component``
    """
    return build_components(page_index, entry_count, sort_by, days)
