import vampytest

from ...inventory_core import Inventory
from ...item_core import ITEM_ID_STRAWBERRY, Item, get_item_nullable
from ...quest_core import quest_requirement_serialisable_create_item_exact
from ...unit_core import AMOUNT_TYPE_COUNT, AMOUNT_TYPE_WEIGHT

from ..helpers import try_submit_item


def _iter_options():
    item_strawberry = get_item_nullable(ITEM_ID_STRAWBERRY)
    assert item_strawberry is not None
    
    yield (
        'requirement full',
        quest_requirement_serialisable_create_item_exact(ITEM_ID_STRAWBERRY, AMOUNT_TYPE_COUNT, 20, 20),
        [
            (item_strawberry, 24)
        ],
        item_strawberry,
        (
            None,
            quest_requirement_serialisable_create_item_exact(ITEM_ID_STRAWBERRY, AMOUNT_TYPE_COUNT, 20, 20),
            [
                (item_strawberry, 24)
            ],
        ),
    )
    
    yield (
        'none -> full submit',
        quest_requirement_serialisable_create_item_exact(ITEM_ID_STRAWBERRY, AMOUNT_TYPE_COUNT, 20, 0),
        [
            (item_strawberry, 24)
        ],
        item_strawberry,
        (
            [
                (item_strawberry, AMOUNT_TYPE_COUNT, 20, 0, 20)
            ],
            quest_requirement_serialisable_create_item_exact(ITEM_ID_STRAWBERRY, AMOUNT_TYPE_COUNT, 20, 20),
            [
                (item_strawberry, 4)
            ],
        ),
    )
    
    yield (
        'none -> full submit, no item left',
        quest_requirement_serialisable_create_item_exact(ITEM_ID_STRAWBERRY, AMOUNT_TYPE_COUNT, 20, 0),
        [
            (item_strawberry, 20)
        ],
        item_strawberry,
        (
            [
                (item_strawberry, AMOUNT_TYPE_COUNT, 20, 0, 20)
            ],
            quest_requirement_serialisable_create_item_exact(ITEM_ID_STRAWBERRY, AMOUNT_TYPE_COUNT, 20, 20),
            [],
        ),
    )
    
    yield (
        'none -> partial submit',
        quest_requirement_serialisable_create_item_exact(ITEM_ID_STRAWBERRY, AMOUNT_TYPE_COUNT, 20, 0),
        [
            (item_strawberry, 14)
        ],
        item_strawberry,
        (
            [
                (item_strawberry, AMOUNT_TYPE_COUNT, 20, 0, 14)
            ],
            quest_requirement_serialisable_create_item_exact(ITEM_ID_STRAWBERRY, AMOUNT_TYPE_COUNT, 20, 14),
            [],
        ),
    )
    
    yield (
        'some -> full submit',
        quest_requirement_serialisable_create_item_exact(ITEM_ID_STRAWBERRY, AMOUNT_TYPE_COUNT, 20, 4),
        [
            (item_strawberry, 24)
        ],
        item_strawberry,
        (
            [
                (item_strawberry, AMOUNT_TYPE_COUNT, 20, 4, 16)
            ],
            quest_requirement_serialisable_create_item_exact(ITEM_ID_STRAWBERRY, AMOUNT_TYPE_COUNT, 20, 20),
            [
                (item_strawberry, 8)
            ],
        ),
    )
    
    yield (
        'some -> partial submit',
        quest_requirement_serialisable_create_item_exact(ITEM_ID_STRAWBERRY, AMOUNT_TYPE_COUNT, 20, 4),
        [
            (item_strawberry, 14)
        ],
        item_strawberry,
        (
            [
                (item_strawberry, AMOUNT_TYPE_COUNT, 20, 4, 14)
            ],
            quest_requirement_serialisable_create_item_exact(ITEM_ID_STRAWBERRY, AMOUNT_TYPE_COUNT, 20, 18),
            [],
        ),
    )
    
    yield (
        'none -> full submit (weight)',
        quest_requirement_serialisable_create_item_exact(
            ITEM_ID_STRAWBERRY, AMOUNT_TYPE_WEIGHT, 20 * item_strawberry.weight + 1, 0
        ),
        [
            (item_strawberry, 24)
        ],
        item_strawberry,
        (
            [
                (item_strawberry, AMOUNT_TYPE_WEIGHT, 20 * item_strawberry.weight + 1, 0, 21 * item_strawberry.weight)
            ],
            quest_requirement_serialisable_create_item_exact(
                ITEM_ID_STRAWBERRY, AMOUNT_TYPE_WEIGHT, 20 * item_strawberry.weight + 1, 21 * item_strawberry.weight
            ),
            [
                (item_strawberry, 3)
            ],
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).named_first().returning_last())
def test__try_submit_item(requirement, item_amount_pairs, submitted_item):
    """
    Tests whether ``try_submit_item`` works as intended.
    
    Parameters
    ----------
    requirement : ``QuestSubTypeSerialisable``
        Requirement to submit to.
    
    item_amount_pairs : ``list<(Item, int)>``
        Items in the user's inventory.
    
    submitted_item : ``Item``
        Specific item to submit.
    
    Returns
    -------
    output : ``(list<(Item, int, int, int, int)>, QuestSubTypeSerialisable, list<(Item, int)>)``
    """
    requirement, index = requirement.behaviour.deserialise(
        b''.join([*requirement.behaviour.serialise(requirement.configuration)]),
        0
    )
    assert requirement is not None
    
    inventory = Inventory(0)
    
    for item, amount in item_amount_pairs:
        inventory.modify_item_amount(item, amount)
    
    item_entry = inventory.get_item_entry_by_id(submitted_item.id)
    assert item_entry is not None
    
    submissions_normalised = None
    
    submissions_normalised = try_submit_item(requirement, inventory, item_entry, submissions_normalised)
    
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
