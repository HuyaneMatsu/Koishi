from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from hata import Component, create_button, create_row, create_section, create_separator, create_text_display

from ...adventure_core import (
    ACTION_ID_SYSTEM_CANCELLATION, ACTION_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION, ADVENTURE_STATE_ACTIONING, ADVENTURE_STATE_FINALIZED,
    Adventure, AdventureAction, LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS, LOCATIONS, LOOT_STATE_SUCCESS,
    TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION, TARGETS, build_loot_data
)
from ...item_core import ITEM_ID_PEACH

from ..component_builders import build_adventure_action_listing_view_components


def _iter_options():
    # show depart, +2, no return
    # page at index 0, disallow stepping.
    
    adventure_entry_id = 9999
    user_id = 202508060000
    adventure_action_entry_id_0 = 8888
    adventure_action_entry_id_1 = 8887
    
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
    adventure.updated_at = DateTime(2016, 5, 16, tzinfo = TimeZone.utc)
    adventure.state = ADVENTURE_STATE_FINALIZED
    adventure.action_count = 2
    adventure.entry_id = adventure_entry_id
    
    adventure_action_0 = AdventureAction(
        adventure_entry_id,
        ACTION_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION,
        DateTime(2016, 5, 14, tzinfo = TimeZone.utc),
        None,
        build_loot_data([
            (LOOT_STATE_SUCCESS, ITEM_ID_PEACH, 5),
        ]),
        0,
        10,
    )
    adventure_action_0.entry_id = adventure_action_entry_id_0
    
    adventure_action_1 = AdventureAction(
        adventure_entry_id,
        ACTION_ID_SYSTEM_CANCELLATION,
        DateTime(2016, 5, 15, tzinfo = TimeZone.utc),
        None,
        None,
        0,
        0,
    )
    adventure_action_1.entry_id = adventure_action_entry_id_1
    
    yield (
        adventure,
        [
            adventure_action_0,
            adventure_action_1,
        ],
        True,
        5,
        0,
        [
            create_text_display(
                f'### Actions of {LOCATIONS[LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS].name} for '
                f'{TARGETS[TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION].name} (page 1)'
            ),
            create_separator(),
            create_section(
                create_text_display(
                    f'<t:{adventure.created_at.timestamp():.0f}:T> Depart'
                ),
                thumbnail = create_button(
                    'View',
                    custom_id = 'adventure.action.view.depart',
                    enabled = False,
                ),
            ),
            create_section(
                create_text_display(
                    f'<t:{adventure_action_0.created_at.timestamp():.0f}:T> Gardening'
                ),
                thumbnail = create_button(
                    'View',
                    custom_id = (
                        f'adventure.action.view.{user_id:x}.{adventure_entry_id:x}.{adventure_action_entry_id_0:x}.'
                        f'{True:x}.{5:x}.{True:x}.{0:x}'
                    ),
                    enabled = True,
                ),
            ),
            create_section(
                create_text_display(
                    f'<t:{adventure_action_1.created_at.timestamp():.0f}:T> Cancellation'
                ),
                thumbnail = create_button(
                    'View',
                    custom_id = (
                        f'adventure.action.view.{user_id:x}.{adventure_entry_id:x}.{adventure_action_entry_id_1:x}.'
                        f'{True:x}.{5:x}.{True:x}.{0:x}'
                    ),
                    enabled = False,
                )
            ),
            create_section(
                create_text_display(
                    f'<t:{adventure.updated_at.timestamp():.0f}:T> Return'
                ),
                thumbnail = create_button(
                    'View',
                    custom_id = 'adventure.action.view.return',
                    enabled = False,
                ),
            ),
            create_separator(),
            create_row(
                create_button(
                    'View adventure',
                    enabled = True,
                    custom_id = f'adventure.view.{user_id:x}.{adventure_entry_id:x}.{True:x}.{5:x}',
                ),
                create_button(
                    'Page 0',
                    enabled = False,
                    custom_id = f'adventure.action_listing.{user_id:x}.{adventure_entry_id:x}.{True:x}.{5:x}.{0:x}',
                ),
                create_button(
                    'Page 2',
                    enabled = False,
                    custom_id = f'adventure.action_listing.{user_id:x}.{adventure_entry_id:x}.{True:x}.{5:x}.{1:x}',
                ),
            ),
        ],
    )
    
    
    adventure_entry_id = 9998
    user_id = 202508060001
    
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
    adventure.state = ADVENTURE_STATE_ACTIONING
    adventure.action_count = 0
    adventure.entry_id = adventure_entry_id
    
    # show depart, +0, no return
    # page at index 0, disallow stepping.
    
    yield (
        adventure,
        None,
        False,
        0,
        0,
        [
            create_text_display(
                f'### Actions of {LOCATIONS[LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS].name} for '
                f'{TARGETS[TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION].name} (page 1)'
            ),
            create_separator(),
            create_section(
                create_text_display(
                    f'<t:{adventure.created_at.timestamp():.0f}:T> Depart'
                ),
                thumbnail = create_button(
                    'View',
                    custom_id = 'adventure.action.view.depart',
                    enabled = False,
                ),
            ),
            create_separator(),
            create_row(
                create_button(
                    'View adventure',
                    enabled = True,
                    custom_id = f'adventure.view.{user_id:x}.{adventure_entry_id:x}.{False:x}.{0:x}',
                ),
                create_button(
                    'Page 0',
                    enabled = False,
                    custom_id = f'adventure.action_listing.{user_id:x}.{adventure_entry_id:x}.{False:x}.{0:x}.{0:x}',
                ),
                create_button(
                    'Page 2',
                    enabled = False,
                    custom_id = f'adventure.action_listing.{user_id:x}.{adventure_entry_id:x}.{False:x}.{0:x}.{1:x}',
                ),
            ),
        ],
    )
    
    # show depart, +0, no return
    # page at index 2, allow step backwards.
    
    yield (
        adventure,
        None,
        False,
        0,
        2,
        [
            create_text_display(
                f'### Actions of {LOCATIONS[LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS].name} for '
                f'{TARGETS[TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION].name} (page 3)'
            ),
            create_separator(),
            create_row(
                create_button(
                    'View adventure',
                    enabled = True,
                    custom_id = f'adventure.view.{user_id:x}.{adventure_entry_id:x}.{False:x}.{0:x}',
                ),
                create_button(
                    'Page 2',
                    enabled = True,
                    custom_id = f'adventure.action_listing.{user_id:x}.{adventure_entry_id:x}.{False:x}.{0:x}.{1:x}',
                ),
                create_button(
                    'Page 4',
                    enabled = False,
                    custom_id = f'adventure.action_listing.{user_id:x}.{adventure_entry_id:x}.{False:x}.{0:x}.{3:x}',
                ),
            ),
        ],
    )
    
    # show depart, +8, return
    # page at index 0, disallow stepping
    
    adventure_entry_id = 9997
    user_id = 202508060002
    
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
    adventure.updated_at = DateTime(2016, 5, 16, tzinfo = TimeZone.utc)
    adventure.state = ADVENTURE_STATE_FINALIZED
    adventure.action_count = 8
    adventure.entry_id = adventure_entry_id
    adventure.energy_exhausted = 8
    
    adventure_action_listing = []
    
    for index in range(0, 8):
        adventure_action = AdventureAction(
            adventure_entry_id,
            ACTION_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION,
            DateTime(2016, 5, 14, 1 + index, tzinfo = TimeZone.utc),
            None,
            None,
            0,
            1,
        )
        adventure_action.entry_id = 100 + index
        adventure_action_listing.append(adventure_action)
        
    
    yield (
        adventure,
        adventure_action_listing,
        False,
        0,
        0,
        [
            create_text_display(
                f'### Actions of {LOCATIONS[LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS].name} for '
                f'{TARGETS[TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION].name} (page 1)'
            ),
            create_separator(),
            create_section(
                create_text_display(
                    f'<t:{adventure.created_at.timestamp():.0f}:T> Depart'
                ),
                thumbnail = create_button(
                    'View',
                    custom_id = 'adventure.action.view.depart',
                    enabled = False,
                ),
            ),
            *(
                create_section(
                    create_text_display(
                        f'<t:{DateTime(2016, 5, 14, 1 + index, tzinfo = TimeZone.utc).timestamp():.0f}:T> Gardening'
                    ),
                    thumbnail = create_button(
                        'View',
                        custom_id = (
                            f'adventure.action.view.{user_id:x}.{adventure_entry_id:x}.{(100 + index):x}.'
                            f'{False:x}.{0:x}.{True:x}.{0:x}'
                        ),
                        enabled = True,
                    ),
                ) for index in range(0, 8)
            ),
            create_section(
                create_text_display(
                    f'<t:{adventure.updated_at.timestamp():.0f}:T> Return'
                ),
                thumbnail = create_button(
                    'View',
                    custom_id = 'adventure.action.view.return',
                    enabled = False,
                ),
            ),
            create_separator(),
            create_row(
                create_button(
                    'View adventure',
                    enabled = True,
                    custom_id = f'adventure.view.{user_id:x}.{adventure_entry_id:x}.{False:x}.{0:x}',
                ),
                create_button(
                    'Page 0',
                    enabled = False,
                    custom_id = f'adventure.action_listing.{user_id:x}.{adventure_entry_id:x}.{False:x}.{0:x}.{0:x}',
                ),
                create_button(
                    'Page 2',
                    enabled = False,
                    custom_id = f'adventure.action_listing.{user_id:x}.{adventure_entry_id:x}.{False:x}.{0:x}.{1:x}',
                ),
            ),
        ],
    )
    
    # has depart, has +19, has return
    # show page index 1, so allow page index 0 and page index2
    
    adventure_entry_id = 9996
    user_id = 202508060003
    
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
    adventure.updated_at = DateTime(2016, 5, 16, tzinfo = TimeZone.utc)
    adventure.state = ADVENTURE_STATE_FINALIZED
    adventure.action_count = 19
    adventure.entry_id = adventure_entry_id
    adventure.energy_exhausted = 19
    
    adventure_action_listing = []
    
    for index in range(0, 19):
        adventure_action = AdventureAction(
            adventure_entry_id,
            ACTION_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION,
            DateTime(2016, 5, 14, 1 + index, tzinfo = TimeZone.utc),
            None,
            None,
            0,
            1,
        )
        adventure_action.entry_id = 100 + index
        adventure_action_listing.append(adventure_action)
    
    yield (
        adventure,
        adventure_action_listing,
        False,
        0,
        1,
        [
            create_text_display(
                f'### Actions of {LOCATIONS[LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS].name} for '
                f'{TARGETS[TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION].name} (page 2)'
            ),
            create_separator(),
            *(
                create_section(
                    create_text_display(
                        f'<t:{DateTime(2016, 5, 14, 1 + index, tzinfo = TimeZone.utc).timestamp():.0f}:T> Gardening'
                    ),
                    thumbnail = create_button(
                        'View',
                        custom_id = (
                            f'adventure.action.view.{user_id:x}.{adventure_entry_id:x}.{(100 + index):x}.'
                            f'{False:x}.{0:x}.{True:x}.{1:x}'
                        ),
                    ),
                ) for index in range(9, 19)
            ),
            create_separator(),
            create_row(
                create_button(
                    'View adventure',
                    enabled = True,
                    custom_id = f'adventure.view.{user_id:x}.{adventure_entry_id:x}.{False:x}.{0:x}',
                ),
                create_button(
                    'Page 1',
                    enabled = True,
                    custom_id = f'adventure.action_listing.{user_id:x}.{adventure_entry_id:x}.{False:x}.{0:x}.{0:x}',
                ),
                create_button(
                    'Page 3',
                    enabled = True,
                    custom_id = f'adventure.action_listing.{user_id:x}.{adventure_entry_id:x}.{False:x}.{0:x}.{2:x}',
                ),
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_adventure_action_listing_view_components(
    adventure,
    adventure_action_listing,
    allow_switching_to_adventure_listing_view,
    adventure_listing_page_index,
    adventure_action_listing_page_index,
):
    """
    Tests whether ``build_adventure_action_listing_view_components`` works as intended.
    
    Parameters
    ----------
    adventure : ``Adventure``
        The parent adventure.
    
    adventure_action_listing : ``None | list<AdventureActions>``
        The adventure's actions.
    
    allow_switching_to_adventure_listing_view : `bool`
        Whether switching to adventure listing is allowed from adventure view.
    
    adventure_listing_page_index : `int`
        Adventure listing page index to direct to from adventure view.
    
    adventure_action_listing_page_index : `int`
        The page index to show.
    
    Returns
    -------
    output : ``list<Component>``
    """
    output = build_adventure_action_listing_view_components(
        adventure,
        adventure_action_listing,
        allow_switching_to_adventure_listing_view,
        adventure_listing_page_index,
        adventure_action_listing_page_index,
    )
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
