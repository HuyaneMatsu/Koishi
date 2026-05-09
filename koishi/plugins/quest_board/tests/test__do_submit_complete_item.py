import vampytest

from ...inventory_core import Inventory
from ...item_core import ITEM_ID_STRAWBERRY, Item, get_item_nullable
from ...quest_core import (
    AMOUNT_TYPE_COUNT, AMOUNT_TYPE_WEIGHT, QuestRequirementSerialisableItemExact, QuestRequirementSerialisableItemGroup
)

from ..helpers import do_submit_complete_item


def _iter_options():
    item_strawberry = get_item_nullable(ITEM_ID_STRAWBERRY)
    assert item_strawberry is not None
    
    yield (
        'none -> full submit x1',
        QuestRequirementSerialisableItemExact(ITEM_ID_STRAWBERRY, AMOUNT_TYPE_COUNT, 20, 0),
        [
            (item_strawberry, 24)
        ],
        item_strawberry,
        1,
        (
            [
                (item_strawberry, AMOUNT_TYPE_COUNT, 20, 0, 20)
            ],
            QuestRequirementSerialisableItemExact(ITEM_ID_STRAWBERRY, AMOUNT_TYPE_COUNT, 20, 20),
            [
                (item_strawberry, 4)
            ],
        ),
    )
    
    yield (
        'some -> full submit x1',
        QuestRequirementSerialisableItemExact(ITEM_ID_STRAWBERRY, AMOUNT_TYPE_COUNT, 20, 2),
        [
            (item_strawberry, 24)
        ],
        item_strawberry,
        1,
        (
            [
                (item_strawberry, AMOUNT_TYPE_COUNT, 20, 2, 18)
            ],
            QuestRequirementSerialisableItemExact(ITEM_ID_STRAWBERRY, AMOUNT_TYPE_COUNT, 20, 20),
            [
                (item_strawberry, 6)
            ],
        ),
    )
    
    yield (
        'some -> none to submit',
        QuestRequirementSerialisableItemExact(ITEM_ID_STRAWBERRY, AMOUNT_TYPE_COUNT, 20, 20),
        [
            (item_strawberry, 24)
        ],
        item_strawberry,
        1,
        (
            None,
            QuestRequirementSerialisableItemExact(ITEM_ID_STRAWBERRY, AMOUNT_TYPE_COUNT, 20, 20),
            [
                (item_strawberry, 24)
            ],
        ),
    )
    
    yield (
        'none -> full submit, no item left x1',
        QuestRequirementSerialisableItemExact(ITEM_ID_STRAWBERRY, AMOUNT_TYPE_COUNT, 20, 0),
        [
            (item_strawberry, 20)
        ],
        item_strawberry,
        1,
        (
            [
                (item_strawberry, AMOUNT_TYPE_COUNT, 20, 0, 20)
            ],
            QuestRequirementSerialisableItemExact(ITEM_ID_STRAWBERRY, AMOUNT_TYPE_COUNT, 20, 20),
            [],
        ),
    )
    
    yield (
        'none -> full submit (weight) x1',
        QuestRequirementSerialisableItemExact(
            ITEM_ID_STRAWBERRY, AMOUNT_TYPE_WEIGHT, 20 * item_strawberry.weight + 1, 0
        ),
        [
            (item_strawberry, 24)
        ],
        item_strawberry,
        1,
        (
            [
                (item_strawberry, AMOUNT_TYPE_WEIGHT, 20 * item_strawberry.weight + 1, 0, 21 * item_strawberry.weight)
            ],
            QuestRequirementSerialisableItemExact(
                ITEM_ID_STRAWBERRY, AMOUNT_TYPE_WEIGHT, 20 * item_strawberry.weight + 1, 21 * item_strawberry.weight
            ),
            [
                (item_strawberry, 3)
            ],
        ),
    )
    
    yield (
        'none -> full submit x3',
        QuestRequirementSerialisableItemExact(ITEM_ID_STRAWBERRY, AMOUNT_TYPE_COUNT, 20, 0),
        [
            (item_strawberry, 64)
        ],
        item_strawberry,
        3,
        (
            [
                (item_strawberry, AMOUNT_TYPE_COUNT, 60, 0, 60)
            ],
            QuestRequirementSerialisableItemExact(ITEM_ID_STRAWBERRY, AMOUNT_TYPE_COUNT, 20, 20),
            [
                (item_strawberry, 4)
            ],
        ),
    )
    
    yield (
        'none -> full submit, no item left x3',
        QuestRequirementSerialisableItemExact(ITEM_ID_STRAWBERRY, AMOUNT_TYPE_COUNT, 20, 0),
        [
            (item_strawberry, 60)
        ],
        item_strawberry,
        3,
        (
            [
                (item_strawberry, AMOUNT_TYPE_COUNT, 60, 0, 60)
            ],
            QuestRequirementSerialisableItemExact(ITEM_ID_STRAWBERRY, AMOUNT_TYPE_COUNT, 20, 20),
            [],
        ),
    )
    
    yield (
        'none -> full submit (weight) x3',
        QuestRequirementSerialisableItemExact(
            ITEM_ID_STRAWBERRY, AMOUNT_TYPE_WEIGHT, 20 * item_strawberry.weight + 1, 0
        ),
        [
            (item_strawberry, 64)
        ],
        item_strawberry,
        3,
        (
            [
                (item_strawberry, AMOUNT_TYPE_WEIGHT, 60 * item_strawberry.weight + 3, 0, 61 * item_strawberry.weight)
            ],
            QuestRequirementSerialisableItemExact(
                ITEM_ID_STRAWBERRY, AMOUNT_TYPE_WEIGHT, 20 * item_strawberry.weight + 1, 21 * item_strawberry.weight - 2
            ),
            [
                (item_strawberry, 3)
            ],
        ),
    )
    
    yield (
        'some -> full submit (weight) x3',
        QuestRequirementSerialisableItemExact(
            ITEM_ID_STRAWBERRY, AMOUNT_TYPE_WEIGHT, 20 * item_strawberry.weight + 1, 1
        ),
        [
            (item_strawberry, 64)
        ],
        item_strawberry,
        3,
        (
            [
                (item_strawberry, AMOUNT_TYPE_WEIGHT, 60 * item_strawberry.weight + 3, 1, 61 * item_strawberry.weight)
            ],
            QuestRequirementSerialisableItemExact(
                ITEM_ID_STRAWBERRY,
                AMOUNT_TYPE_WEIGHT,
                20 * item_strawberry.weight + 1,
                21 * item_strawberry.weight - 2 + 1
            ),
            [
                (item_strawberry, 3)
            ],
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).named_first().returning_last())
def test__do_submit_complete_item(requirement, item_amount_pairs, submitted_item, submission_count):
    """
    Tests whether ``do_submit_complete_item`` works as intended.
    
    Parameters
    ----------
    requirement : ``QuestRequirementSerialisableItemExact | QuestRequirementSerialisableItemGroup | QuestRequirementSerialisable``
        Requirement to submit to.
    
    item_amount_pairs : ``list<(Item, int)>``
        Items in the user's inventory.
    
    submitted_item : ``Item``
        Specific item to submit.
    
    submission_count : `int`
        How much times to submit the requirement.
    
    Returns
    -------
    output : ``(None | list<(Item, int, int, int, int)>, QuestRequirementSerialisableItemExact | QuestRequirementSerialisableItemGroup | QuestRequirementSerialisable, list<(Item, int)>)``
    """
    requirement, index = type(requirement).deserialise(b''.join([*requirement.serialise()]), 0)
    assert requirement is not None
    
    inventory = Inventory(0)
    
    for item, amount in item_amount_pairs:
        inventory.modify_item_amount(item, amount)
    
    item_entry = inventory.get_item_entry_by_id(submitted_item.id)
    assert item_entry is not None
    
    submissions_normalised = None
    
    submissions_normalised = do_submit_complete_item(
        requirement, inventory, item_entry, submissions_normalised, submission_count
    )
    
    vampytest.assert_instance(submissions_normalised, list, nullable = True)
    if (submissions_normalised is not None):
        for element in submissions_normalised:
            vampytest.assert_instance(element, tuple)
            vampytest.assert_eq(len(element), 5)
            item, amount_type, amount_required, amount_submitted, amount_used = element
            vampytest.assert_instance(item, Item)
            vampytest.assert_instance(amount_type, int)
            vampytest.assert_instance(amount_required, int)
            vampytest.assert_instance(amount_submitted, int)
            vampytest.assert_instance(amount_used, int)
    
    return (
        submissions_normalised,
        requirement,
        [(item_entry.item, item_entry.amount) for item_entry in inventory.iter_item_entries()],
    )
