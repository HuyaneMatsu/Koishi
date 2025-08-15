from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from hata import Component, create_button, create_section, create_text_display

from ...adventure_core import (
    ACTION_ID_SYSTEM_CANCELLATION, ACTION_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION, ADVENTURE_STATE_CANCELLED, ADVENTURE_STATE_DEPARTING,
    ADVENTURE_STATE_RETURNING, Adventure, AdventureAction, LOOT_STATE_SUCCESS, build_loot_data
)
from ...item_core import ITEM_ID_PEACH

from ..component_builders import iter_build_adventure_action_components


def _iter_options():
    adventure_entry_id = 9997
    user_id = 202508040000
    
    adventure = Adventure(
        user_id,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
    )
    adventure.state = ADVENTURE_STATE_DEPARTING
    adventure.action_count = 1
    adventure.created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    adventure.entry_id = adventure_entry_id
    
    yield (
        adventure,
        None,
        True,
        False,
        False,
        0,
        False,
        0,
        [
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
        ],
    )
    
    adventure_entry_id = 9998
    user_id = 202508040001
    
    adventure = Adventure(
        user_id,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
    )
    adventure.state = ADVENTURE_STATE_RETURNING
    adventure.action_count = 2
    adventure.updated_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    adventure.entry_id = adventure_entry_id
    
    yield (
        adventure,
        None,
        False,
        True,
        False,
        0,
        False,
        0,
        [
            create_section(
                create_text_display(
                    f'<t:{adventure.updated_at.timestamp():.0f}:T> Return'
                ),
                thumbnail = create_button(
                    'View',
                    custom_id = 'adventure.action.view.return',
                    enabled = False,
                ),
            )
        ],
    )
    
    adventure_entry_id = 9999
    user_id = 202508040002
    adventure_action_entry_id_0 = 8888
    adventure_action_entry_id_1 = 8887
    
    adventure = Adventure(
        user_id,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
    )
    adventure.state = ADVENTURE_STATE_CANCELLED
    adventure.action_count = 3
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
        False,
        False,
        0,
        False,
        0,
        [
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
        ],
    )
    
    yield (
        adventure,
        [
            adventure_action_0,
        ],
        False,
        False,
        True,
        4,
        True,
        5,
        [
            create_section(
                create_text_display(
                    f'<t:{adventure_action_0.created_at.timestamp():.0f}:T> Gardening'
                ),
                thumbnail = create_button(
                    'View',
                    custom_id = (
                        f'adventure.action.view.{user_id:x}.{adventure_entry_id:x}.{adventure_action_entry_id_0:x}.'
                        f'{True:x}.{4:x}.{True:x}.{5:x}'
                    ),
                ),
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__iter_build_adventure_action_components(
    adventure,
    adventure_action_listing,
    produce_depart,
    produce_return,
    allow_switching_to_adventure_listing_view,
    adventure_listing_page_index,
    allow_switching_to_adventure_action_listing_view,
    adventure_action_listing_page_index,
):
    """
    Tests whether ``iter_build_adventure_action_components`` works as intended.
    
    Parameters
    ----------
    adventure : ``Adventure``
        The parent adventure.
    
    adventure_action_listing : ``None | list<AdventureActions>``
        Adventure actions to render components for.
    
    produce_depart : `bool`
        Whether to produce depart component.
    
    produce_return : `bool`
        Whether to produce return component.
    
    allow_switching_to_adventure_listing_view : `bool`
        Whether switching to adventure listing is allowed from adventure view.
    
    adventure_listing_page_index : `int`
        Adventure listing page index to direct to from adventure view.
    
    allow_switching_to_adventure_action_listing_view : `bool`
        Whether switching to adventure action listing view is allowed from a action view.
    
    adventure_action_listing_page_index : `int`
        Adventure action listing page index to direct to from adventure action view.
    
    Yields
    ------
    component : ``list<Component>``
    """
    output = [*iter_build_adventure_action_components(
        adventure,
        adventure_action_listing,
        produce_depart,
        produce_return,
        allow_switching_to_adventure_listing_view,
        adventure_listing_page_index,
        allow_switching_to_adventure_action_listing_view,
        adventure_action_listing_page_index,
    )]
    
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
