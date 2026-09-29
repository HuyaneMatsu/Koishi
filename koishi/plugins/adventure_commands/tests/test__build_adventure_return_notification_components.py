import vampytest
from hata import Component, create_button, create_row, create_separator, create_text_display

from ...adventure_core import (
    ADVENTURE_STATE_FINALISED, LOCATIONS, LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS, TARGETS,
    TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION, adventure_create, adventure_action_create,
    LOOT_STATE_SUCCESS, ACTION_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION, loot_data_build
)
from ...item_core import ITEM_ID_PEACH, get_item_nullable

from ..component_building import build_adventure_return_notification_components
from ..constants import ADVENTURE_VIEW_MODE_DEFAULT, ADVENTURE_VIEW_MODE_DETAILED


def _iter_options():
    adventure_entry_id = 9998
    user_id = 202508140002
    
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
    
    adventure = adventure_create(
        user_id,
        LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS,
        TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION,
        0,
        0,
        None,
        0,
        100,
        100,
    )
    adventure.energy_exhausted = 10
    adventure.created_at = adventure.updated_at = 1463097600
    adventure.state = ADVENTURE_STATE_FINALISED
    adventure.action_listing = [adventure_action_0]
    adventure.entry_id = adventure_entry_id
    
    yield (
        adventure,
        [            
            create_text_display(
                f'### You have returned from adventure at {LOCATIONS[LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS].name} for '
                f'{TARGETS[TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION].name}'
            ),
            create_separator(),
            create_text_display(
                f'You are recovering for 20 minutes, until <t:{adventure.updated_at + 1200}:T>.'
            ),
            create_separator(),
            create_text_display(
                f'### Loot:\n'
                f'- {item_peach.emoji} {item_peach.name} x5 ({5 * item_peach.weight / 1000:.02f} kg)'
            ),
            create_separator(),
            create_row(
                create_button(
                    'Refresh',
                    enabled = False,
                    custom_id = (
                        f'adventure.view.{user_id:x}.{adventure_entry_id:x}.{ADVENTURE_VIEW_MODE_DEFAULT:x}.'
                        f'{False:x}.{0:x}'
                    ),
                ),
                create_button(
                    'Back to adventures',
                    enabled = False,
                    custom_id = f'adventure.listing.{user_id:x}.{0:x}',
                ),
                create_button(
                    'View all action',
                    enabled = True,
                    custom_id = (
                        f'adventure.action_listing.{user_id:x}.{adventure_entry_id:x}.{ADVENTURE_VIEW_MODE_DEFAULT:x}.'
                        f'{False:x}.{0:x}.0'
                    ),
                ),
                create_button(
                    'Cancel',
                    enabled = False,
                    custom_id = f'adventure.cancel.{user_id:x}.{adventure_entry_id:x}',
                ),
                create_button(
                    'Detailed',
                    enabled = True,
                    custom_id = (
                        f'adventure.view.{user_id:x}.{adventure_entry_id:x}.{ADVENTURE_VIEW_MODE_DETAILED:x}.'
                        f'{False:x}.{0:x}'
                    ),
                ),
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_adventure_return_notification_components(adventure):
    """
    Tests whether ``build_adventure_return_notification_components`` works as intended.
    
    Parameters
    ----------
    adventure : ``Adventure``
        The adventure the user returned from.
    
    Returns
    -------
    output : ``list<Component>``
    """
    output = build_adventure_return_notification_components(adventure)
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
