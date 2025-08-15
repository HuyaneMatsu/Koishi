from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from hata import BUILTIN_EMOJIS, Component, create_button, create_row, create_separator, create_text_display

from ...adventure_core import ACTION_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION, AdventureAction, LOOT_STATE_SUCCESS, build_loot_data
from ...item_core import ITEM_ID_PEACH

from ..component_builders import build_adventure_action_view_components


def _iter_options():
    adventure_entry_id = 9998
    user_id = 202508050000
    adventure_action_entry_id = 8889
    
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
        user_id,
        adventure_action,
        True,
        5,
        False,
        0,
        [
            create_text_display('### Action Gardening'),
            create_separator(),
            create_text_display(
                f'Occurred at: <t:{adventure_action.created_at.timestamp():.0f}:T>\n'
                f'Used health: 0\n'
                f'Used energy: 0'
            ),
            create_separator(),
            create_row(
                create_button(
                    'View adventure',
                    enabled = True,
                    custom_id = f'adventure.view.{user_id:x}.{adventure_entry_id:x}.{True:x}.{5:x}',
                ),
                create_button(
                    'Back to actions',
                    enabled = False,
                    custom_id = f'adventure.action_listing.{user_id:x}.{adventure_entry_id:x}.{True:x}.{5:x}.{0:x}',
                ),
                create_button(
                    'View battle logs',
                    enabled = False,
                    custom_id = f'adventure.action.battle.{user_id:x}.{adventure_entry_id:x}.{adventure_action_entry_id:x}',
                ),
            ),
        ],
    )
    
    adventure_entry_id = 9999
    user_id = 202508050000
    adventure_action_entry_id = 8881
    
    adventure_action = AdventureAction(
        adventure_entry_id,
        ACTION_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION,
        DateTime(2016, 5, 14, tzinfo = TimeZone.utc),
        None,
        build_loot_data([
            (LOOT_STATE_SUCCESS, ITEM_ID_PEACH, 5),
        ]),
        5,
        10,
    )
    adventure_action.entry_id = adventure_action_entry_id
    
    yield (
        user_id,
        adventure_action,
        False,
        0,
        True,
        5,
        [
            create_text_display('### Action Gardening'),
            create_separator(),
            create_text_display(
                f'Occurred at: <t:{adventure_action.created_at.timestamp():.0f}:T>\n'
                f'Used health: 5\n'
                f'Used energy: 10'
            ),
            create_separator(),
            create_text_display(
                f'### Loot:\n'
                f'- {BUILTIN_EMOJIS["peach"]} Peach x5'
            ),
            create_separator(),
            create_row(
                create_button(
                    'View adventure',
                    enabled = True,
                    custom_id = f'adventure.view.{user_id:x}.{adventure_entry_id:x}.{False:x}.{0:x}',
                ),
                create_button(
                    'Back to actions',
                    enabled = True,
                    custom_id = f'adventure.action_listing.{user_id:x}.{adventure_entry_id:x}.{False:x}.{0:x}.{5:x}',
                ),
                create_button(
                    'View battle logs',
                    enabled = False,
                    custom_id = f'adventure.action.battle.{user_id:x}.{adventure_entry_id:x}.{adventure_action_entry_id:x}',
                ),
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_adventure_action_view_components(
    user_id,
    adventure_action,
    allow_switching_to_adventure_listing_view,
    adventure_listing_page_index,
    allow_switching_to_adventure_action_listing_view,
    adventure_action_listing_page_index,
):
    """
    Tests whether ``build_adventure_action_view_components`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        The owner user's identifier.
    
    adventure_action : ``AdventureAction``
        The adventure action to display.
    
    allow_switching_to_adventure_listing_view : `bool`
        Whether switching to adventure listing is allowed from adventure view.
    
    adventure_listing_page_index : `int`
        Adventure listing page index to direct to from adventure view.
    
    allow_switching_to_adventure_action_listing_view : `bool`
        Whether switching to action listing view is allowed from a action view.
    
    adventure_action_listing_page_index : `int`
        Adventure action listing page index to direct to from action view.
    
    Returns
    -------
    output : ``list<Component>``
    """
    output = build_adventure_action_view_components(
        user_id,
        adventure_action,
        allow_switching_to_adventure_listing_view,
        adventure_listing_page_index,
        allow_switching_to_adventure_action_listing_view,
        adventure_action_listing_page_index,
    )
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
