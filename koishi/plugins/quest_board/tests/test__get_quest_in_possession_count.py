import vampytest

from ...inventory_core import Inventory
from ...item_core import (
    ITEM_FLAG_EDIBLE, ITEM_GROUP_ID_KNIFE, ITEM_ID_CARROT, ITEM_ID_FISHING_ROD, ITEM_ID_PEACH, ITEM_ID_POKING_KNIFE,
    get_item_nullable
)
from ...quest_core import (
    AMOUNT_TYPE_COUNT, AMOUNT_TYPE_WEIGHT, QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY, Quest,
    QuestRequirementInstantiableItemCategory, QuestRequirementInstantiableItemExact,
    QuestRequirementInstantiableItemGroup
)

from ..helpers import get_quest_in_possession_count


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
    inventory.modify_item_amount(item_peach, 20)
    inventory.modify_item_amount(item_fishing_rod, 7)
    inventory.modify_item_amount(item_poking_knife, 8)
    inventory.modify_item_amount(item_carrot, 9)
    
    quest_00 = Quest(
        QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
        [
            QuestRequirementInstantiableItemExact(ITEM_ID_PEACH, AMOUNT_TYPE_COUNT, 30),
        ],
        None,
    )
    
    yield (
        'Not enough exact item count',
        quest_00,
        inventory,
        0,
    )
    
    
    quest_01 = Quest(
        QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
        [
            QuestRequirementInstantiableItemExact(ITEM_ID_PEACH, AMOUNT_TYPE_WEIGHT, 30 * item_peach.weight),
        ],
        None,
    )
    
    yield (
        'Not enough exact item weight',
        quest_01,
        inventory,
        0,
    )
    
    
    quest_02 = Quest(
        QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
        [
            QuestRequirementInstantiableItemGroup(ITEM_GROUP_ID_KNIFE, AMOUNT_TYPE_COUNT, 1),
        ],
        None,
    )
    
    yield (
        'Enough group item count x1',
        quest_02,
        inventory,
        0,
    )
    
    
    quest_03 = Quest(
        QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
        [
            QuestRequirementInstantiableItemGroup(ITEM_GROUP_ID_KNIFE, AMOUNT_TYPE_WEIGHT, 1 * item_poking_knife.weight),
        ],
        None,
    )
    
    yield (
        'Enough group item weight x1',
        quest_03,
        inventory,
        0,
    )
    
    
    quest_04 = Quest(
        QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
        [
            QuestRequirementInstantiableItemExact(ITEM_ID_PEACH, AMOUNT_TYPE_COUNT, 20),
        ],
        None,
    )
    
    yield (
        'Enough exact item count x1',
        quest_04,
        inventory,
        1,
    )
    
    
    quest_05 = Quest(
        QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
        [
            QuestRequirementInstantiableItemExact(ITEM_ID_PEACH, AMOUNT_TYPE_WEIGHT, 20 * item_peach.weight),
        ],
        None,
    )
    
    
    yield (
        'Enough exact item weight x4',
        quest_05,
        inventory,
        1,
    )
    
    
    quest_06 = Quest(
        QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
        [
            QuestRequirementInstantiableItemExact(ITEM_ID_PEACH, AMOUNT_TYPE_COUNT, 5),
        ],
        None,
    )
    
    yield (
        'Enough exact item count x4',
        quest_06,
        inventory,
        4,
    )
    
    
    quest_07 = Quest(
        QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
        [
            QuestRequirementInstantiableItemExact(ITEM_ID_PEACH, AMOUNT_TYPE_WEIGHT, 5 * item_peach.weight),
        ],
        None,
    )
    
    yield (
        'Enough exact item weight x4',
        quest_07,
        inventory,
        4,
    )
    
    # Note that if we did not allow stacked completion, this would be just 5.
    quest_08 = Quest(
        QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
        [
            QuestRequirementInstantiableItemExact(ITEM_ID_PEACH, AMOUNT_TYPE_WEIGHT, 3 * item_peach.weight + 1),
        ],
        None,
    )
    
    yield (
        'Enough exact item weight with amount overflow',
        quest_08,
        inventory,
        6,
    )
    
    
    quest_09 = Quest(
        QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
        [
            QuestRequirementInstantiableItemExact(ITEM_ID_PEACH, AMOUNT_TYPE_COUNT, 5),
            QuestRequirementInstantiableItemExact(ITEM_ID_CARROT, AMOUNT_TYPE_COUNT, 10),
        ],
        None,
    )
    
    yield (
        'Multiple item exact, enough for one, not enough for other',
        quest_09,
        inventory,
        0,
    )
    
    
    quest_10 = Quest(
        QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
        [
            QuestRequirementInstantiableItemExact(ITEM_ID_PEACH, AMOUNT_TYPE_COUNT, 5),
            QuestRequirementInstantiableItemExact(ITEM_ID_CARROT, AMOUNT_TYPE_COUNT, 4),
        ],
        None,
    )
    
    yield (
        'Multiple item exact, enough for both, select lower',
        quest_10,
        inventory,
        2,
    )
    
    
    quest_11 = Quest(
        QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
        [
            QuestRequirementInstantiableItemExact(ITEM_ID_PEACH, AMOUNT_TYPE_COUNT, 5),
            QuestRequirementInstantiableItemGroup(ITEM_GROUP_ID_KNIFE, AMOUNT_TYPE_COUNT, 1),
        ],
        None,
    )
    
    yield (
        'Item exact with item group, enough',
        quest_11,
        inventory,
        0,
    )
    
    
    quest_12 = Quest(
        QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
        [
            QuestRequirementInstantiableItemCategory(ITEM_FLAG_EDIBLE, AMOUNT_TYPE_COUNT, 1),
        ],
        None,
    )
    
    yield (
        'Enough category item count x1',
        quest_12,
        inventory,
        0,
    )
    
    
    quest_13 = Quest(
        QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
        [
            QuestRequirementInstantiableItemCategory(ITEM_FLAG_EDIBLE, AMOUNT_TYPE_WEIGHT, 1 * item_carrot.weight),
        ],
        None,
    )
    
    yield (
        'Enough category item weight x1',
        quest_13,
        inventory,
        0,
    )
    
    
    quest_14 = Quest(
        QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
        [
            QuestRequirementInstantiableItemExact(ITEM_ID_PEACH, AMOUNT_TYPE_COUNT, 5),
            QuestRequirementInstantiableItemCategory(ITEM_FLAG_EDIBLE, AMOUNT_TYPE_COUNT, 1),
        ],
        None,
    )
    
    yield (
        'Item exact with item category, enough',
        quest_14,
        inventory,
        0,
    )


@vampytest._(vampytest.call_from(_iter_options()).named_first().returning_last())
def test__get_quest_in_possession_count(quest, inventory):
    """
    Tests whether ``get_quest_in_possession_count`` works as intended.
    
    Parameters
    ----------
    quest : ``Quest``
        Quest to work with.
    
    inventory : ``Inventory``
        The user's inventory.
    
    Returns
    -------
    possession_count : `int`
    """
    output = get_quest_in_possession_count(quest, inventory)
    vampytest.assert_instance(output, int)
    return output
