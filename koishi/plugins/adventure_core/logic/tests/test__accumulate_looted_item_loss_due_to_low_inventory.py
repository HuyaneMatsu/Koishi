import vampytest

from ....item_core import ITEM_ID_PEACH, ITEM_ID_STRAWBERRY

from ...adventure import LOOT_STATE_LOST_DUE_FULL_INVENTORY

from ..helpers import accumulate_looted_item_loss_due_to_low_inventory
from ..loot_accumulation import LootAccumulation


def _iter_options():
    # no items.
    yield (
        {},
        1000,
        (
            {},
            set(),
        ),
    )
    
    # all items pass
    yield (
        {
            ITEM_ID_PEACH: LootAccumulation(4, 900, 80),
            ITEM_ID_STRAWBERRY: LootAccumulation(2, 100, 10),
        },
        1000,
        (
            {
                ITEM_ID_PEACH: LootAccumulation(4, 900, 80),
                ITEM_ID_STRAWBERRY: LootAccumulation(2, 100, 10),
            },
            set(),
        ),
    )
    
    # negative inventory
    yield (
        {
            ITEM_ID_PEACH: LootAccumulation(4, 900, 80),
            ITEM_ID_STRAWBERRY: LootAccumulation(2, 100, 10),
        },
        -100,
        (
            {},
            {
                (LOOT_STATE_LOST_DUE_FULL_INVENTORY, ITEM_ID_PEACH, 4),
                (LOOT_STATE_LOST_DUE_FULL_INVENTORY, ITEM_ID_STRAWBERRY, 2),
            },
        ),
    )
    
    # not enough inventory
    yield (
        {
            ITEM_ID_PEACH: LootAccumulation(4, 900, 160),
            ITEM_ID_STRAWBERRY: LootAccumulation(2, 100, 20),
        },
        500,
        (
            {
                ITEM_ID_PEACH: LootAccumulation(2, 900, 160),
                ITEM_ID_STRAWBERRY: LootAccumulation(1, 100, 20),
            },
            {
                (LOOT_STATE_LOST_DUE_FULL_INVENTORY, ITEM_ID_PEACH, 2),
                (LOOT_STATE_LOST_DUE_FULL_INVENTORY, ITEM_ID_STRAWBERRY, 1),
            },
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__accumulate_looted_item_loss_due_to_low_inventory(loot_accumulations, available_inventory):
    """
    Tests whether ``accumulate_looted_item_loss_due_to_low_inventory`` works as intended.
    
    Parameters
    ----------
    loot_accumulations : ``dict<int, LootAccumulation>``
        Accumulated loot from the action.
    
    available_inventory : `int`
        The available inventory of the user.
    
    Returns
    -------
    output : ``(dict<int, LootAccumulation>, set<(int, int, int)>)``
    """
    loot_accumulations = {
        item_id: loot_accumulation.copy() for item_id, loot_accumulation in loot_accumulations.items()
    }
    looted_items = []
    accumulate_looted_item_loss_due_to_low_inventory(loot_accumulations, looted_items, available_inventory)
    return (loot_accumulations, {*looted_items})
