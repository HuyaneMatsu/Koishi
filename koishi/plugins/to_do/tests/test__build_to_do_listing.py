from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from hata import Component, create_button, create_row, create_separator, create_text_display

from ..component_building import build_to_do_listing
from ..constants import EMOJI_CLOSE, EMOJI_PAGE_DECREMENT, EMOJI_PAGE_INCREMENT
from ..to_do import ToDo


def _iter_options():
    created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    creator_id = 202409190012
    description = 'nyan nyan'
    name = 'miau'
    
    entry_id_0 = 134
    entry_id_1 = 135
    entry_id_2 = 136
    
    to_do_0 = ToDo(name, description, created_at, creator_id)
    to_do_0.entry_id = entry_id_0
    
    to_do_1 = ToDo(name, description, created_at, creator_id)
    to_do_1.entry_id = entry_id_1
    
    to_do_2 = ToDo(name, description, created_at, creator_id)
    to_do_2.entry_id = entry_id_2
    
    yield (
        [
            to_do_0,
            to_do_1,
            to_do_2,
        ],
        0,
        None,
        [
            create_text_display(
                'Page: 1 / 1'
            ),
            create_separator(),
            create_text_display(
                '\\#134: miau\n'
                '\\#135: miau\n'
                '\\#136: miau'
            ),
            create_separator(),
            create_row(
                create_button(
                    'Page 0',
                    EMOJI_PAGE_DECREMENT,
                    custom_id = 'to_do_listing.page_decrement_disabled',
                    enabled = False,
                ),
                create_button(
                    'Page 2',
                    EMOJI_PAGE_INCREMENT,
                    custom_id = 'to_do_listing.page_increment_disabled',
                    enabled = False,
                ),
                create_button(
                    'Close',
                    EMOJI_CLOSE,
                    custom_id = 'to_do_listing.close',
                ),
            ),
        ],
    )
    
    yield (
        [],
        1,
        'shrimp',
        [
            create_text_display(
                'Page: 2 / 0\n'
                'Query: shrimp'
            ),
            create_separator(),
            create_row(
                create_button(
                    'Page 1',
                    EMOJI_PAGE_DECREMENT,
                    custom_id = 'to_do_listing.page.0.c2hyaW1w',
                    enabled = True,
                ),
                create_button(
                    'Page 3',
                    EMOJI_PAGE_INCREMENT,
                    custom_id = 'to_do_listing.page_increment_disabled',
                    enabled = False,
                ),
                create_button(
                    'Close',
                    EMOJI_CLOSE,
                    custom_id = 'to_do_listing.close',
                ),
            ),
        ],
    )
    
    
@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_to_do_listing(to_do_listing, page_index, query):
    """
    Tests whether ``build_to_do_listing`` works as intended.
    
    Parameters
    ----------
    to_do_listing : ``list<ToDo>``
        To-do listing to render.
    
    page_index : `int`
        Page index to show.
    
    query : `None | str`
        Query to match the to-do entries.
    
    Returns
    -------
    output : ``list<Component>``
    """
    output = build_to_do_listing(to_do_listing, page_index, query)
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
