from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from hata import BUILTIN_EMOJIS, Component, create_button, create_row, create_separator, create_text_display

from ...adventure_core import (
    ACTION_ID_SYSTEM_CANCELLATION, ACTION_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION, ADVENTURE_STATE_FINALIZED,
    Adventure, AdventureAction, LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS, LOCATIONS, LOOT_STATE_SUCCESS,
    TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION, TARGETS, build_loot_data
)
from ...item_core import ITEM_ID_PEACH

from ..component_builders import build_adventure_view_finalized_components


def _iter_options():
    adventure_entry_id = 9999
    user_id = 202508040006
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
        4,
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
                'Total duration: 3 days\n'
                'Recovery time: 20 minutes'
            ),
            create_separator(),
            create_text_display(
                f'### Loot:\n'
                f'- {BUILTIN_EMOJIS["peach"]} Peach x5'
            ),
            create_separator(),
            create_row(
                create_button(
                    'Refresh',
                    enabled = False,
                    custom_id = f'adventure.view.{user_id:x}.{adventure_entry_id:x}.{True:x}.{4:x}',
                ),
                create_button(
                    'Back to adventures',
                    enabled = True,
                    custom_id = f'adventure.listing.{user_id:x}.{4:x}',
                ),
                create_button(
                    'View all action',
                    enabled = True,
                    custom_id = f'adventure.action_listing.{user_id:x}.{adventure_entry_id:x}.{True:x}.{4:x}.0',
                ),
                create_button(
                    'Cancel',
                    enabled = False,
                    custom_id = f'adventure.cancel.{user_id:x}.{adventure_entry_id:x}',
                ),
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_adventure_view_finalized_components(
    adventure,
    adventure_action_listing,
    allow_switching_to_adventure_listing_view,
    adventure_listing_page_index,
):
    """
    Tests whether ``build_adventure_view_finalized_components`` works as intended.
    
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
    
    Returns
    -------
    output : ``list<Component>``
    """
    output = build_adventure_view_finalized_components(
        adventure,
        adventure_action_listing,
        allow_switching_to_adventure_listing_view,
        adventure_listing_page_index,
    )
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
