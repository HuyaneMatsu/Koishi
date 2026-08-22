from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from hata import Component, create_button, create_row, create_separator, create_text_display

from ...adventure_core import ACTION_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION, AdventureAction, LOOT_STATE_SUCCESS, build_loot_data, \
    Adventure, LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS, TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION, LOCATIONS, TARGETS
from ...item_core import ITEM_ID_SCARLET_ONION, get_item_nullable

from ..component_building import build_adventure_action_notification_components


def _iter_options():
    item_peach = get_item_nullable(ITEM_ID_SCARLET_ONION)
    assert item_peach is not None
    
    adventure_entry_id = 9998
    user_id = 202608190002
    adventure_action_entry_id = 8889
    
    adventure = Adventure(
        user_id,
        LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS,
        TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION,
        0,
        0,
        0,
        0,
        0,
    )
    adventure.entry_id = adventure_entry_id
    
    adventure_action = AdventureAction(
        adventure_entry_id,
        ACTION_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION,
        DateTime(2016, 5, 14, tzinfo = TimeZone.utc),
        None,
        None,
        0,
        0,
    )
    adventure_action.entry_id = adventure_action_entry_id
    
    yield (
        adventure,
        adventure_action,
        [
            create_text_display(
                f'### Gardening at {LOCATIONS[LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS].name} for '
                f'{TARGETS[TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION].name}'
            ),
            create_separator(),
            create_row(
                create_button(
                    'View adventure',
                    enabled = True,
                    custom_id = f'adventure.view.{user_id:x}.{adventure_entry_id:x}.{False:x}.{0:x}',
                ),
                create_button(
                    'View battle logs',
                    enabled = False,
                    custom_id = (
                        f'adventure.action.battle.{user_id:x}.{adventure_entry_id:x}.{adventure_action_entry_id:x}'
                    ),
                ),
                create_button(
                    'I don\'t want notifs, nya!!',
                    custom_id = 'user_settings.notification_adventure_action.disable',
                ),
            ),
        ],
    )

    adventure_entry_id = 9999
    user_id = 202608190003
    adventure_action_entry_id = 8881
    
    
    adventure = Adventure(
        user_id,
        LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS,
        TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION,
        0,
        0,
        0,
        0,
        0,
    )
    adventure.entry_id = adventure_entry_id
    
    adventure_action = AdventureAction(
        adventure_entry_id,
        ACTION_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION,
        DateTime(2016, 5, 14, tzinfo = TimeZone.utc),
        None,
        build_loot_data([
            (LOOT_STATE_SUCCESS, ITEM_ID_SCARLET_ONION, 5),
        ]),
        5,
        10,
    )
    adventure_action.entry_id = adventure_action_entry_id
    
    yield (
        adventure,
        adventure_action,
        [
            create_text_display(
                f'### Gardening at {LOCATIONS[LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS].name} for '
                f'{TARGETS[TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION].name}'
            ),
            create_separator(),
            create_text_display(
                f'### Loot:\n'
                f'- {item_peach.emoji} {item_peach.name} x5 ({item_peach.weight * 5 / 1000:.03f} kg)'
            ),
            create_separator(),
            create_row(
                create_button(
                    'View adventure',
                    enabled = True,
                    custom_id = f'adventure.view.{user_id:x}.{adventure_entry_id:x}.{False:x}.{0:x}',
                ),
                create_button(
                    'View battle logs',
                    enabled = False,
                    custom_id = (
                        f'adventure.action.battle.{user_id:x}.{adventure_entry_id:x}.{adventure_action_entry_id:x}'
                    ),
                ),
                create_button(
                    'I don\'t want notifs, nya!!',
                    custom_id = 'user_settings.notification_adventure_action.disable',
                ),
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_adventure_action_notification_components(adventure, adventure_action):
    """
    Tests whether ``build_adventure_action_notification_components`` works as intended.
    
    Parameters
    ----------
    adventure : ``Adventure``
        The adventure the user is on.
    
    adventure_action : ``AdventureAction``
        The adventure action to display.
    
    Returns
    -------
    output : ``list<Component>``
    """
    output = build_adventure_action_notification_components(adventure, adventure_action)
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
