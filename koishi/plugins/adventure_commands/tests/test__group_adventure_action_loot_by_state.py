from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ...adventure_core import (
    AdventureAction, LOOT_STATE_SUCCESS, LOOT_STATE_LOST_DUE_FULL_INVENTORY, LOOT_STATE_LOST_DUE_LOW_ENERGY,
    build_loot_data
)
from ...item_core import ITEM_ID_PEACH, ITEM_ID_STRAWBERRY

from ..component_builders import group_adventure_action_loot_by_state


def _iter_options():
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    yield (
        AdventureAction(
            0,
            0,
            now,
            None,
            None,
            0,
            0,
        ),
        {},
    )
    
    yield (
        AdventureAction(
            0,
            0,
            now,
            None,
            build_loot_data([
                (LOOT_STATE_SUCCESS, ITEM_ID_PEACH, 5),
                (LOOT_STATE_LOST_DUE_FULL_INVENTORY, ITEM_ID_PEACH, 4),
                (LOOT_STATE_LOST_DUE_LOW_ENERGY, ITEM_ID_PEACH, 3),
            ]),
            0,
            0,
        ),
        {
            LOOT_STATE_SUCCESS : {
                ITEM_ID_PEACH : 5,
            },
            LOOT_STATE_LOST_DUE_FULL_INVENTORY : {
                ITEM_ID_PEACH : 4,
            },
            LOOT_STATE_LOST_DUE_LOW_ENERGY : {
                ITEM_ID_PEACH : 3,
            },
        },
    )
    
    yield (
        AdventureAction(
            0,
            0,
            now,
            None,
            build_loot_data([
                (LOOT_STATE_LOST_DUE_FULL_INVENTORY, ITEM_ID_PEACH, 6),
                (LOOT_STATE_LOST_DUE_FULL_INVENTORY, ITEM_ID_STRAWBERRY, 7),
            ]),
            0,
            0,
        ),
        {
            LOOT_STATE_LOST_DUE_FULL_INVENTORY : {
                ITEM_ID_PEACH : 6,
                ITEM_ID_STRAWBERRY : 7,
            },
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__group_adventure_action_loot_by_state(adventure_action):
    """
    Tests whether ``group_adventure_action_loot_by_state`` works as intended.
    
    Parameters
    ----------
    adventure_action : ``AdventureAction``
        Adventure actions to group its loot of.
    
    Returns
    -------
    output : `dict<int, dict<int, int>>`
    """
    output = group_adventure_action_loot_by_state(adventure_action)
    
    vampytest.assert_instance(output, dict)
    
    for key, value in output.items():
        vampytest.assert_instance(key, int)
        vampytest.assert_instance(value, dict)
        
        for key, value in value.items():
            vampytest.assert_instance(key, int)
            vampytest.assert_instance(value, int)
    
    return output
