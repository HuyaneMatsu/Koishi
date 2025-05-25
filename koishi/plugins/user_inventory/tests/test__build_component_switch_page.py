import vampytest
from hata import Component, create_button, create_row

from ..component_builders import build_component_switch_page
from ..constants import EMOJI_CLOSE, EMOJI_LEFT, EMOJI_RIGHT


def _iter_options():
    yield (
        1,
        3,
        0,
        0,
        create_row(
            create_button(
                'Page 0',
                EMOJI_LEFT,
                custom_id = 'inventory.page.D',
                enabled = False,
            ),
            create_button(
                'Page 2',
                EMOJI_RIGHT,
                custom_id = 'inventory.page.I',
                enabled = False,
            ),
            create_button(
                'Close',
                EMOJI_CLOSE,
                custom_id = 'inventory.page.close',
            ),
        )
    )
    
    yield (
        1,
        3,
        1,
        3,
        create_row(
            create_button(
                'Page 1',
                EMOJI_LEFT,
                custom_id = 'inventory.page.1.3.0',
            ),
            create_button(
                'Page 3',
                EMOJI_RIGHT,
                custom_id = 'inventory.page.1.3.2',
            ),
            create_button(
                'Close',
                EMOJI_CLOSE,
                custom_id = 'inventory.page.close',
            ),
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_component_switch_page(sort_by, sort_order, page_index, page_count):
    """
    Tests whether ``build_component_switch_page`` works as intended.
    
    Parameters
    ----------
    sort_by : `int`
        Identifier to determine how item entries should be sorted.
    
    sort_order : `int`
        Identifier to determine sorting order.
    
    page_index : `int`
        The current page's index.
    
    page_count : `int`
        Amount of pages.
    
    Returns
    -------
    component : ``Component``
    """
    output = build_component_switch_page(sort_by, sort_order, page_index, page_count)
    vampytest.assert_instance(output, Component)
    return output
