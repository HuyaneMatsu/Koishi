import vampytest

from ...inventory_core import Inventory, ItemEntry
from ...item_core import (
    ITEM_FLAG_WEAPON, ITEM_GROUP_ID_KNIFE, ITEM_ID_CARROT, ITEM_ID_FISHING_ROD, ITEM_ID_PEACH, ITEM_ID_POKING_KNIFE,
    get_item_nullable
)
from ...quest_core import (
    AMOUNT_TYPE_COUNT, QUEST_REQUIREMENT_TYPE_NONE, QUEST_REQUIREMENT_TYPE_ITEM_CATEGORY,
    QUEST_REQUIREMENT_TYPE_ITEM_EXACT, QUEST_REQUIREMENT_TYPE_ITEM_GROUP
)

from ..helpers import iter_submission_requirement_item_entries_of_normalised


def _iter_options():
    item_peach = get_item_nullable(ITEM_ID_PEACH)
    assert item_peach is not None
    
    item_fishing_rod = get_item_nullable(ITEM_ID_FISHING_ROD)
    assert item_fishing_rod is not None
    
    item_poking_knife = get_item_nullable(ITEM_ID_POKING_KNIFE)
    assert item_poking_knife is not None
    
    item_carrot = get_item_nullable(ITEM_ID_CARROT)
    assert item_carrot is not None
    
    
    inventory = Inventory(202603030001)
    inventory.modify_item_amount(item_peach, 6)
    inventory.modify_item_amount(item_fishing_rod, 7)
    inventory.modify_item_amount(item_poking_knife, 8)
    inventory.modify_item_amount(item_carrot, 9)
    
    yield (
        inventory,
        (QUEST_REQUIREMENT_TYPE_NONE, ITEM_ID_PEACH, AMOUNT_TYPE_COUNT, 200, 0),
        [],
    )
    
    yield (
        inventory,
        (QUEST_REQUIREMENT_TYPE_ITEM_EXACT, ITEM_ID_PEACH, AMOUNT_TYPE_COUNT, 200, 0),
        [
            ItemEntry(item_peach, 6),
        ],
    )
    
    yield (
        inventory,
        (QUEST_REQUIREMENT_TYPE_ITEM_GROUP, ITEM_GROUP_ID_KNIFE, AMOUNT_TYPE_COUNT, 200, 0),
        [
            ItemEntry(item_poking_knife, 8),
        ],
    )
    
    yield (
        inventory,
        (QUEST_REQUIREMENT_TYPE_ITEM_CATEGORY, ITEM_FLAG_WEAPON, AMOUNT_TYPE_COUNT, 200, 0),
        [
            ItemEntry(item_fishing_rod, 7),
            ItemEntry(item_poking_knife, 8),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__iter_submission_requirement_item_entries_of_normalised(inventory, submission_requirement_normalised):
    """
    Tests whether ``iter_submission_requirement_item_entries_of_normalised`` works as intended.
    
    Parameters
    ----------
    inventory : ``Inventory``
        Inventory to filter from.
    
    submission_requirement_normalised : `(int, int, int, int, int)`
        Normalised requirement to match items for.
    
    Returns
    -------
    output : ``list<ItemEntry>``
    """
    output = [*iter_submission_requirement_item_entries_of_normalised(inventory, submission_requirement_normalised)]
    for element in output:
        vampytest.assert_instance(element, ItemEntry)
    
    return output
