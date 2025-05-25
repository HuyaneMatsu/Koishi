import vampytest
from hata import create_button, create_row

from ..builders import build_components
from ..constants import (
    BUTTON_CLOSE, BUTTON_PAGE_NEXT_DISABLED, BUTTON_PAGE_PREVIOUS_DISABLED, CUSTOM_ID_PAGE_BASE, EMOJI_PAGE_NEXT,
    EMOJI_PAGE_PREVIOUS, PAGE_SIZE
)


def _iter_options():
    yield (
        0,
        PAGE_SIZE - 1,
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
        PAGE_SIZE,
        create_row(
            BUTTON_PAGE_PREVIOUS_DISABLED,
            create_button(
                'Page 2',
                EMOJI_PAGE_NEXT,
                custom_id = f'{CUSTOM_ID_PAGE_BASE}{1!s}',
            ),
            BUTTON_CLOSE,
        ),
    )
    
    yield (
        6,
        PAGE_SIZE - 1,
        create_row(
            create_button(
                'Page 6',
                emoji = EMOJI_PAGE_PREVIOUS,
                custom_id = f'{CUSTOM_ID_PAGE_BASE}{5!s}',
            ),
            BUTTON_PAGE_NEXT_DISABLED.copy_with(
                label = 'Page 8',
            ),
            BUTTON_CLOSE,
        ),
    )
    
    yield (
        6,
        PAGE_SIZE,
        create_row(
            create_button(
                'Page 6',
                EMOJI_PAGE_PREVIOUS,
                custom_id = f'{CUSTOM_ID_PAGE_BASE}{5!s}',
            ),
            create_button(
                'Page 8',
                EMOJI_PAGE_NEXT,
                custom_id = f'{CUSTOM_ID_PAGE_BASE}{7!s}',
            ),
            BUTTON_CLOSE,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_components(page_index, entry_count):
    """
    Tests whether ``build_components`` works as intended.
    
    Parameters
    ----------
    page_index : `int`
        Page index (0 based).
    entry_count : `int`
        The entry count on this page.
    
    Returns
    -------
    output : ``Component``
    """
    return build_components(page_index, entry_count)
