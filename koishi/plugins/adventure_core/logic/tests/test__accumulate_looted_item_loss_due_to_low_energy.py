import vampytest

from ....item_core import ITEM_ID_PEACH, ITEM_ID_STRAWBERRY

from ...adventure import LOOT_STATE_LOST_DUE_LOW_ENERGY

from ..helpers import accumulate_looted_item_loss_due_to_low_energy
from ..loot_accumulation import LootAccumulation


def _iter_options():
    # no items.
    yield (
        {},
        100,
        (
            0,
            {},
            set(),
        ),
    )
    
    # all items pass
    yield (
        {
            ITEM_ID_PEACH: LootAccumulation(20, 900, 80),
            ITEM_ID_STRAWBERRY: LootAccumulation(2, 100, 10),
        },
        100,
        (
            90,
            {
                ITEM_ID_PEACH: LootAccumulation(20, 900, 80),
                ITEM_ID_STRAWBERRY: LootAccumulation(2, 100, 10),
            },
            set(),
        ),
    )
    
    # negative energy
    yield (
        {
            ITEM_ID_PEACH: LootAccumulation(20, 900, 80),
            ITEM_ID_STRAWBERRY: LootAccumulation(2, 100, 10),
        },
        -100,
        (
            0,
            {},
            {
                (LOOT_STATE_LOST_DUE_LOW_ENERGY, ITEM_ID_PEACH, 20),
                (LOOT_STATE_LOST_DUE_LOW_ENERGY, ITEM_ID_STRAWBERRY, 2),
            },
        ),
    )
    
    # not enough energy
    yield (
        {
            ITEM_ID_PEACH: LootAccumulation(20, 900, 160),
            ITEM_ID_STRAWBERRY: LootAccumulation(2, 100, 20),
        },
        100,
        (
            100,
            {
                ITEM_ID_PEACH: LootAccumulation(11, 900, 160),
                ITEM_ID_STRAWBERRY: LootAccumulation(1, 100, 20),
            },
            {
                (LOOT_STATE_LOST_DUE_LOW_ENERGY, ITEM_ID_PEACH, 9),
                (LOOT_STATE_LOST_DUE_LOW_ENERGY, ITEM_ID_STRAWBERRY, 1),
            },
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__accumulate_looted_item_loss_due_to_low_energy(loot_accumulations, available_energy):
    """
    Tests whether ``accumulate_looted_item_loss_due_to_low_energy`` works as intended.
    
    Parameters
    ----------
    loot_accumulations : ``dict<int, LootAccumulation>``
        Accumulated loot from the action.
    
    available_energy : `int`
        The available energy of the user.
    
    Returns
    -------
    output : ``(int, dict<int, LootAccumulation>, set<(int, int, int)>)``
    """
    loot_accumulations = {
        item_id: loot_accumulation.copy() for item_id, loot_accumulation in loot_accumulations.items()
    }
    looted_items = []
    energy_exhausted = accumulate_looted_item_loss_due_to_low_energy(loot_accumulations, looted_items, available_energy)
    vampytest.assert_instance(energy_exhausted, int)
    return (energy_exhausted, loot_accumulations, {*looted_items})
