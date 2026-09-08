import vampytest
from hata import Component, create_button, create_row, create_separator, create_text_display

from ...adventure_core import (
    ACTION_ID_SYSTEM_CANCELLATION_NOW, ACTION_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION,
    ADVENTURE_STATE_FINALIZED, LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS, LOCATIONS, LOOT_STATE_SUCCESS,
    TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION, TARGETS, adventure_action_create, adventure_create,
    loot_data_build
)
from ...item_core import ITEM_ID_PEACH, get_item_nullable

from ..component_building import build_adventure_view_finalized_components


def _iter_options():
    adventure_entry_id = 9999
    user_id = 202508040006
    
    item_peach = get_item_nullable(ITEM_ID_PEACH)
    assert item_peach is not None
    
    adventure_action_0 = adventure_action_create(
        ACTION_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION,
        1463184000,
        None,
        loot_data_build([
            (LOOT_STATE_SUCCESS, ITEM_ID_PEACH, 5),
        ]),
        0,
        10,
    )
    
    adventure_action_1 = adventure_action_create(
        ACTION_ID_SYSTEM_CANCELLATION_NOW,
        1463270400,
        None,
        None,
        0,
        0,
    )
    
    adventure = adventure_create(
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
    adventure.created_at = 1463097600
    adventure.updated_at = 1463356800
    adventure.state = ADVENTURE_STATE_FINALIZED
    adventure.action_listing = [adventure_action_0, adventure_action_1]
    adventure.entry_id = adventure_entry_id
    
    yield (
        adventure,
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
                f'- {item_peach.emoji} {item_peach.name} x5 ({item_peach.weight * 5 / 1000:.03f} kg)'
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
    allow_switching_to_adventure_listing_view,
    adventure_listing_page_index,
):
    """
    Tests whether ``build_adventure_view_finalized_components`` works as intended.
    
    Parameters
    ----------
    adventure : ``Adventure``
        The parent adventure.
    
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
        allow_switching_to_adventure_listing_view,
        adventure_listing_page_index,
    )
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
