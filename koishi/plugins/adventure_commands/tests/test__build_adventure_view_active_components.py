from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from hata import (
    BUILTIN_EMOJIS, Component, create_button, create_row, create_section, create_separator, create_text_display
)

from ...adventure_core import (
    ACTION_ID_SYSTEM_CANCELLATION, ACTION_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION, ADVENTURE_STATE_ACTIONING,
    ADVENTURE_STATE_CANCELLED, Adventure, AdventureAction, LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS, LOCATIONS,
    LOOT_STATE_SUCCESS, TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION, TARGETS, build_loot_data
)
from ...item_core import ITEM_ID_PEACH

from ..component_builders import build_adventure_view_active_components


def _iter_options():
    adventure_entry_id = 9999
    user_id = 202508040004
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
    adventure.energy_exhausted = 10
    adventure.created_at = DateTime(2016, 5, 13, tzinfo = TimeZone.utc)
    adventure.state = ADVENTURE_STATE_CANCELLED
    adventure.action_count = 2
    adventure.entry_id = adventure_entry_id
    
    adventure_action_0 = AdventureAction(
        adventure_entry_id,
        ACTION_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION,
        DateTime(2016, 5, 14, tzinfo = TimeZone.utc),
        None,
        None,
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
        False,
        0,
        DateTime(2016, 5, 16, tzinfo = TimeZone.utc),
        56000,
        12000,
        [
            create_text_display(
                f'### Adventure to {LOCATIONS[LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS].name} for '
                f'{TARGETS[TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION].name}'
            ),
            create_separator(),
            create_text_display(
                'Departed at: 2016-05-13 00:00:00 UTC\n'
                'Used health: 0 / 100\n'
                'Used energy: 10 / 100\n'
                'Used inventory: 12.000 / 56.000 kg\n'
                'Elapsed time: 3 days\n'
                'You are currently returning home.'
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
                        f'{False:x}.{0:x}.{False:x}.{0:x}'
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
                        f'{False:x}.{0:x}.{False:x}.{0:x}'
                    ),
                    enabled = False,
                ),
            ),
            create_separator(),
            create_row(
                create_button(
                    'Refresh',
                    enabled = True,
                    custom_id = f'adventure.view.{user_id:x}.{adventure_entry_id:x}.{False:x}.{0:x}',
                ),
                create_button(
                    'Back to adventures',
                    enabled = False,
                    custom_id = f'adventure.listing.{user_id:x}.{0:x}',
                ),
                create_button(
                    'View all action',
                    enabled = False,
                    custom_id = f'adventure.action_listing.{user_id:x}.{adventure_entry_id:x}.{False:x}.{0:x}.0',
                ),
                create_button(
                    'Cancel',
                    enabled = False,
                    custom_id = f'adventure.cancel.{user_id:x}.{adventure_entry_id:x}',
                ),
            ),
        ],
    )


    adventure_entry_id = 9999
    user_id = 202508040005
    adventure_action_entry_id_0 = 8888
    adventure_action_entry_id_1 = 8887
    adventure_action_entry_id_2 = 8886
    adventure_action_entry_id_3 = 8885
    adventure_action_entry_id_4 = 8884
    adventure_action_entry_id_5 = 8883
    
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
    adventure.state = ADVENTURE_STATE_ACTIONING
    adventure.created_at = DateTime(2016, 5, 13, tzinfo = TimeZone.utc)
    adventure.action_count = 6
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
        0,
    )
    adventure_action_0.entry_id = adventure_action_entry_id_0
    
    adventure_action_1 = AdventureAction(
        adventure_entry_id,
        ACTION_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION,
        DateTime(2016, 5, 15, 0, 0, 0, tzinfo = TimeZone.utc),
        None,
        None,
        0,
        0,
    )
    adventure_action_1.entry_id = adventure_action_entry_id_1
    
    adventure_action_2 = AdventureAction(
        adventure_entry_id,
        ACTION_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION,
        DateTime(2016, 5, 15, 1, 0, 0, tzinfo = TimeZone.utc),
        None,
        None,
        0,
        0,
    )
    adventure_action_2.entry_id = adventure_action_entry_id_2
    
    adventure_action_3 = AdventureAction(
        adventure_entry_id,
        ACTION_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION,
        DateTime(2016, 5, 15, 2, 0, 0, tzinfo = TimeZone.utc),
        None,
        None,
        0,
        0,
    )
    adventure_action_3.entry_id = adventure_action_entry_id_3
    
    adventure_action_4 = AdventureAction(
        adventure_entry_id,
        ACTION_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION,
        DateTime(2016, 5, 15, 3, 0, 0, tzinfo = TimeZone.utc),
        None,
        None,
        0,
        0,
    )
    adventure_action_4.entry_id = adventure_action_entry_id_4
    
    adventure_action_5 = AdventureAction(
        adventure_entry_id,
        ACTION_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION,
        DateTime(2016, 5, 15, 4, 0, 0, tzinfo = TimeZone.utc),
        None,
        None,
        0,
        0,
    )
    adventure_action_5.entry_id = adventure_action_entry_id_5
    
    yield (
        adventure,
        [
            adventure_action_0,
            adventure_action_1,
            adventure_action_2,
            adventure_action_3,
            adventure_action_4,
            adventure_action_5,
        ],
        True,
        56,
        DateTime(2016, 5, 16, tzinfo = TimeZone.utc),
        56000,
        12000,
        [
            create_text_display(
                f'### Adventure to {LOCATIONS[LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS].name} for '
                f'{TARGETS[TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION].name}'
            ),
            create_separator(),
            create_text_display(
                'Departed at: 2016-05-13 00:00:00 UTC\n'
                'Used health: 0 / 100\n'
                'Used energy: 0 / 100\n'
                'Used inventory: 12.000 / 56.000 kg\n'
                'Elapsed time: 3 days\n'
                'You are currently working on your target task.'
            ),
            create_separator(),
            create_text_display(
                f'### Loot:\n'
                f'- {BUILTIN_EMOJIS["peach"]} Peach x5'
            ),
            create_separator(),
            create_text_display('+ 2 truncated (showing latest 5)'),
            create_section(
                create_text_display(
                    f'<t:{adventure_action_1.created_at.timestamp():.0f}:T> Gardening'
                ),
                thumbnail = create_button(
                    'View',
                    custom_id = (
                        f'adventure.action.view.{user_id:x}.{adventure_entry_id:x}.{adventure_action_entry_id_1:x}.'
                        f'{True:x}.{56:x}.{False:x}.{0:x}'
                    ),
                    enabled = False,
                ),
            ),
            create_section(
                create_text_display(
                    f'<t:{adventure_action_2.created_at.timestamp():.0f}:T> Gardening'
                ),
                thumbnail = create_button(
                    'View',
                    custom_id = (
                        f'adventure.action.view.{user_id:x}.{adventure_entry_id:x}.{adventure_action_entry_id_2:x}.'
                        f'{True:x}.{56:x}.{False:x}.{0:x}'
                    ),
                    enabled = False,
                ),
            ),
            create_section(
                create_text_display(
                    f'<t:{adventure_action_3.created_at.timestamp():.0f}:T> Gardening'
                ),
                thumbnail = create_button(
                    'View',
                    custom_id = (
                        f'adventure.action.view.{user_id:x}.{adventure_entry_id:x}.{adventure_action_entry_id_3:x}.'
                        f'{True:x}.{56:x}.{False:x}.{0:x}'
                    ),
                    enabled = False,
                ),
            ),
            create_section(
                create_text_display(
                    f'<t:{adventure_action_4.created_at.timestamp():.0f}:T> Gardening'
                ),
                thumbnail = create_button(
                    'View',
                    custom_id = (
                        f'adventure.action.view.{user_id:x}.{adventure_entry_id:x}.{adventure_action_entry_id_4:x}.'
                        f'{True:x}.{56:x}.{False:x}.{0:x}'
                    ),
                    enabled = False,
                ),
            ),
            create_section(
                create_text_display(
                    f'<t:{adventure_action_5.created_at.timestamp():.0f}:T> Gardening'
                ),
                thumbnail = create_button(
                    'View',
                    custom_id = (
                        f'adventure.action.view.{user_id:x}.{adventure_entry_id:x}.{adventure_action_entry_id_5:x}.'
                        f'{True:x}.{56:x}.{False:x}.{0:x}'
                    ),
                    enabled = False,
                ),
            ),
            create_separator(),
            create_row(
                create_button(
                    'Refresh',
                    enabled = True,
                    custom_id = f'adventure.view.{user_id:x}.{adventure_entry_id:x}.{True:x}.{56:x}',
                ),
                create_button(
                    'Back to adventures',
                    enabled = True,
                    custom_id = f'adventure.listing.{user_id:x}.{56:x}',
                ),
                create_button(
                    'View all action',
                    enabled = True,
                    custom_id = f'adventure.action_listing.{user_id:x}.{adventure_entry_id:x}.{True:x}.{56:x}.0',
                ),
                create_button(
                    'Cancel',
                    enabled = True,
                    custom_id = f'adventure.cancel.{user_id:x}.{adventure_entry_id:x}',
                ),
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_adventure_view_active_components(
    adventure,
    adventure_action_listing,
    allow_switching_to_adventure_listing_view,
    adventure_listing_page_index,
    now,
    inventory_total,
    inventory_exhausted,
):
    """
    Tests whether ``build_adventure_view_active_components`` works as intended.
    
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
    
    now : `DateTime`
        The current time.
    
    inventory_total : `int`
        The user's total inventory.
    
    inventory_exhausted : `int`
        The user's used inventory.
    
    Returns
    -------
    output : ``list<Component>``
    """
    output = build_adventure_view_active_components(
        adventure,
        adventure_action_listing,
        allow_switching_to_adventure_listing_view,
        adventure_listing_page_index,
        now,
        inventory_total,
        inventory_exhausted,
    )
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
