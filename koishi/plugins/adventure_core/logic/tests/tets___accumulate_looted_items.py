import vampytest

from ....inventory_core import Inventory
from ....item_core import ITEM_ID_PEACH, ITEM_ID_STRAWBERRY
from ....user_stats_core import UserStats

from ...adventure import Adventure, LOOT_STATE_SUCCESS

from ..helpers import accumulate_looted_items
from ..loot_accumulation import LootAccumulation


def _iter_options():
    user_id_0 = 202507310000
    
    adventure_0 = Adventure(
        user_id_0,
        9999,
        0,
        0,
        0,
        0,
        0,
        0,
    )
    
    user_stats_0 = UserStats(
        user_id_0,
    )
    user_stats_0.stat_housewife = 10
    user_stats_0.stat_cuteness = 10
    user_stats_0.stat_bedroom = 10
    user_stats_0.stat_charm = 10
    user_stats_0.stat_loyalty = 10
    
    inventory_0 = Inventory(
        user_id_0,
    )
    
    # no items.
    yield (
        adventure_0,
        user_stats_0,
        inventory_0,
        {},
        2.0,
        (
            set(),
            0,
        ),
    )
    
    # all items pass
    yield (
        adventure_0,
        user_stats_0,
        inventory_0,
        {
            ITEM_ID_PEACH: LootAccumulation(4, 900, 80),
            ITEM_ID_STRAWBERRY: LootAccumulation(2, 100, 10),
        },
        2.0,
        (
            {
                (LOOT_STATE_SUCCESS, ITEM_ID_PEACH, 8),
                (LOOT_STATE_SUCCESS, ITEM_ID_STRAWBERRY, 4),
            },
            90,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__accumulate_looted_items(adventure, user_stats, inventory, loot_accumulations, multiplier):
    """
    Tests whether ``accumulate_looted_items`` works as intended.
    
    Parameters
    ----------
    adventure : ``Adventure``
        Adventure in context.
    
    user_stats : ``UserStats``
        The user's stats.
    
    inventory : ``Inventory``
        The user's inventory.
    
    loot_accumulations : ``dict<int, LootAccumulation>``
        Accumulated loot from the action.
    
    multiplier : `float`
        Multiplier of the user for this given action.
    
    Returns
    -------
    output : `(set<(int, int, int)>, int)`
        The accumulated looted items and the used energy by it. 
    """
    loot_accumulations = {
        item_id: loot_accumulation.copy() for item_id, loot_accumulation in loot_accumulations.items()
    }
    output = accumulate_looted_items(adventure, user_stats, inventory, loot_accumulations, multiplier)
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(len(output), 2)
    
    vampytest.assert_instance(output[0], list)
    for element in output[0]:
        vampytest.assert_instance(element, tuple)
        vampytest.assert_eq(len(element), 3)
        vampytest.assert_instance(element[0], int)
        vampytest.assert_instance(element[1], int)
        vampytest.assert_instance(element[1], int)
    
    vampytest.assert_instance(output[1], int)
    
    vampytest.assert_false(loot_accumulations)
    
    return ({*output[0]}, output[1])
