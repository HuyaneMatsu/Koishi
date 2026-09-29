import vampytest

from ....item_core import ITEM_ID_PEACH, ITEM_ID_STRAWBERRY

from ..adventure_action import adventure_action_create
from ..loot_packing_and_unpacking import loot_data_build
from ..loot_states import LOOT_STATE_SUCCESS, LOOT_STATE_LOST_DUE_FULL_INVENTORY, LOOT_STATE_LOST_DUE_LOW_ENERGY

from ..utils import adventure_action_listing_group_loot_by_state


def _iter_options():
    now = 127000
    yield (
        None,
        {},
    )
    
    yield (
        [
            adventure_action_create(
                0,
                now,
                None,
                loot_data_build([
                    (LOOT_STATE_SUCCESS, ITEM_ID_PEACH, 5),
                    (LOOT_STATE_LOST_DUE_FULL_INVENTORY, ITEM_ID_PEACH, 4),
                    (LOOT_STATE_LOST_DUE_LOW_ENERGY, ITEM_ID_PEACH, 3),
                ]),
                0,
                0,
            ),
            adventure_action_create(
                0,
                now,
                None,
                loot_data_build([
                    (LOOT_STATE_SUCCESS, ITEM_ID_PEACH, 6),
                    (LOOT_STATE_LOST_DUE_FULL_INVENTORY, ITEM_ID_STRAWBERRY, 7),
                ]),
                0,
                0,
            ),
            adventure_action_create(
                0,
                now,
                None,
                None,
                0,
                0,
            ),
        ],
        {
            LOOT_STATE_SUCCESS : {
                ITEM_ID_PEACH : 11,
            },
            LOOT_STATE_LOST_DUE_FULL_INVENTORY : {
                ITEM_ID_PEACH : 4,
                ITEM_ID_STRAWBERRY : 7,
            },
            LOOT_STATE_LOST_DUE_LOW_ENERGY : {
                ITEM_ID_PEACH : 3,
            },
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__adventure_action_listing_group_loot_by_state(adventure_action_listing):
    """
    Tests whether ``adventure_action_listing_group_loot_by_state`` works as intended.
    
    Parameters
    ----------
    adventure_action_listing : ``None | list<AdventureAction>``
        Adventure action listing to group their loot of.
    
    Returns
    -------
    output : `dict<int, dict<int, int>>`
    """
    output = adventure_action_listing_group_loot_by_state(adventure_action_listing)
    
    vampytest.assert_instance(output, dict)
    
    for key, value in output.items():
        vampytest.assert_instance(key, int)
        vampytest.assert_instance(value, dict)
        
        for key, value in value.items():
            vampytest.assert_instance(key, int)
            vampytest.assert_instance(value, int)
    
    return output
