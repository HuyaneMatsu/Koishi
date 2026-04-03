import vampytest

from ...inventory_core import Inventory, ItemEntry
from ...item_core import (
    ITEM_FLAG_WEAPON, ITEM_GROUP_ID_KNIFE, ITEM_ID_CARROT, ITEM_ID_FISHING_ROD, ITEM_ID_PEACH, ITEM_ID_POKING_KNIFE,
    get_item_nullable
)
from ...quest_core import (
    AMOUNT_TYPE_COUNT, QuestRequirementSerialisableBase, QuestRequirementSerialisableItemCategory,
    QuestRequirementSerialisableItemExact, QuestRequirementSerialisableItemGroup
)

from ..helpers import iter_submission_requirement_item_entries_of_requirement


def _iter_options():
    item_peach = get_item_nullable(ITEM_ID_PEACH)
    assert item_peach is not None
    
    item_fishing_rod = get_item_nullable(ITEM_ID_FISHING_ROD)
    assert item_fishing_rod is not None
    
    item_poking_knife = get_item_nullable(ITEM_ID_POKING_KNIFE)
    assert item_poking_knife is not None
    
    item_carrot = get_item_nullable(ITEM_ID_CARROT)
    assert item_carrot is not None
    
    
    inventory = Inventory(202603030000)
    inventory.modify_item_amount(item_peach, 6)
    inventory.modify_item_amount(item_fishing_rod, 7)
    inventory.modify_item_amount(item_poking_knife, 8)
    inventory.modify_item_amount(item_carrot, 9)
    
    yield (
        inventory,
        QuestRequirementSerialisableBase(),
        [],
    )
    
    yield (
        inventory,
        QuestRequirementSerialisableItemExact(ITEM_ID_PEACH, AMOUNT_TYPE_COUNT, 200, 0),
        [
            ItemEntry(item_peach, 6),
        ],
    )
    
    yield (
        inventory,
        QuestRequirementSerialisableItemGroup(ITEM_GROUP_ID_KNIFE, AMOUNT_TYPE_COUNT, 200, 0),
        [
            ItemEntry(item_poking_knife, 8),
        ],
    )
    
    yield (
        inventory,
        QuestRequirementSerialisableItemCategory(ITEM_FLAG_WEAPON, AMOUNT_TYPE_COUNT, 200, 0),
        [
            ItemEntry(item_fishing_rod, 7),
            ItemEntry(item_poking_knife, 8),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__iter_submission_requirement_item_entries_of_requirement(inventory, requirement):
    """
    Tests whether ``iter_submission_requirement_item_entries_of_requirement`` works as intended.
    
    Parameters
    ----------
    inventory : ``Inventory``
        Inventory to filter from.
    
    requirement : ``QuestRequirementSerialisableBase``
        Requirement to match items for.
    
    Returns
    -------
    output : ``list<ItemEntry>``
    """
    output = [*iter_submission_requirement_item_entries_of_requirement(inventory, requirement)]
    for element in output:
        vampytest.assert_instance(element, ItemEntry)
    
    return output
