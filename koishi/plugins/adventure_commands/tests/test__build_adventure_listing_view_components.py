from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from hata import Component, create_button, create_row, create_section, create_separator, create_text_display

from ...adventure_core import (
    Adventure, LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS, LOCATIONS,
    TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION, TARGETS
)

from ..component_builders import build_adventure_listing_view_components


def _iter_options():
    user_id = 202508060030
    
    yield (
        user_id,
        None,
        0,
        1,
        [
            create_text_display('### Adventures (page 1)'),
            create_separator(),
            create_row(
                create_button(
                    'Page 0',
                    custom_id = f'adventure.listing.{user_id:x}.{0:x}',
                    enabled = False,
                ),
                create_button(
                    'Page 2',
                    custom_id = f'adventure.listing.{user_id:x}.{1:x}',
                    enabled = False,
                ),
            ),
        ],
    )
    
    user_id = 202508060031
    adventure_entry_id_0 = 5555
    
    adventure = Adventure(
        user_id,
        LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS,
        TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION,
        0,
        0,
        0,
        100,
        100,
    )
    adventure.created_at = DateTime(2016, 5, 13, tzinfo = TimeZone.utc)
    adventure.entry_id = adventure_entry_id_0
    
    yield (
        user_id,
        [
            adventure,
        ],
        1,
        50,
        [
            create_text_display('### Adventures (page 2)'),
            create_separator(),
            create_section(
                create_text_display(
                    f'2016-05-13 00:00:00 UTC {LOCATIONS[LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS].name} for '
                    f'{TARGETS[TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION].name}'
                ),
                thumbnail = create_button(
                    'View',
                    custom_id = f'adventure.view.{user_id:x}.{adventure_entry_id_0:x}.{True:x}.{1:x}',
                ),
            ),
            create_separator(),
            create_row(
                create_button(
                    'Page 1',
                    custom_id = f'adventure.listing.{user_id:x}.{0:x}',
                    enabled = True,
                ),
                create_button(
                    'Page 3',
                    custom_id = f'adventure.listing.{user_id:x}.{2:x}',
                    enabled = True,
                ),
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_adventure_listing_view_components(user_id, adventure_listing, page_index, page_count):
    """
    Tests whether ``build_adventure_listing_view_components`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        The owner user's identifier.
    
    adventure_listing : ``None | list<Adventure>``
        Adventures to display.
    
    page_index : `int`
        The shown page's index,
    
    page_count : `int`
        The amount of pages.
    
    Returns
    -------
    output : ``list<Component>``
    """
    output = build_adventure_listing_view_components(user_id, adventure_listing, page_index, page_count)
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
