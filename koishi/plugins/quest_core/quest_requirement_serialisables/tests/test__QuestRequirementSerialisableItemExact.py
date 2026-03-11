import vampytest

from ...amount_types import AMOUNT_TYPE_VALUE, AMOUNT_TYPE_WEIGHT

from ...quest_requirement_types import QUEST_REQUIREMENT_TYPE_ITEM_EXACT

from ..item_exact import QuestRequirementSerialisableItemExact


def _assert_fields_set(quest_requirement_serialisable_item_exact):
    """
    Asserts whether the instance has all of its fields set.
    
    Parameters
    ----------
    quest_requirement_serialisable_item_exact : ``QuestRequirementSerialisableItemExact``
        The instance to check.
    """
    vampytest.assert_instance(
        quest_requirement_serialisable_item_exact, QuestRequirementSerialisableItemExact
    )
    vampytest.assert_eq(quest_requirement_serialisable_item_exact.TYPE, QUEST_REQUIREMENT_TYPE_ITEM_EXACT)
    vampytest.assert_instance(quest_requirement_serialisable_item_exact.amount_required, int)
    vampytest.assert_instance(quest_requirement_serialisable_item_exact.amount_submitted, int)
    vampytest.assert_instance(quest_requirement_serialisable_item_exact.amount_type, int)
    vampytest.assert_instance(quest_requirement_serialisable_item_exact.item_id, int)


def test__QuestRequirementSerialisableItemExact__new():
    """
    Tests whether ``QuestRequirementSerialisableItemExact.__new__`` works as intended.
    """
    item_id = 4
    amount_type = AMOUNT_TYPE_VALUE
    amount_required = 5
    amount_submitted = 4
    
    quest_requirement_serialisable_item_exact = QuestRequirementSerialisableItemExact(
        item_id,
        amount_type,
        amount_required,
        amount_submitted,
    )
    _assert_fields_set(quest_requirement_serialisable_item_exact)
    
    vampytest.assert_eq(quest_requirement_serialisable_item_exact.item_id, item_id)
    vampytest.assert_eq(quest_requirement_serialisable_item_exact.amount_type, amount_type)
    vampytest.assert_eq(quest_requirement_serialisable_item_exact.amount_required, amount_required)
    vampytest.assert_eq(quest_requirement_serialisable_item_exact.amount_submitted, amount_submitted)


def test__QuestRequirementSerialisableItemExact__repr():
    """
    Tests whether ``QuestRequirementSerialisableItemExact.__repr__`` works as intended.
    """
    item_id = 4
    amount_type = AMOUNT_TYPE_VALUE
    amount_required = 5
    amount_submitted = 4
    
    quest_requirement_serialisable_item_exact = QuestRequirementSerialisableItemExact(
        item_id,
        amount_type,
        amount_required,
        amount_submitted,
    )
    
    output = repr(quest_requirement_serialisable_item_exact)
    vampytest.assert_instance(output, str)


def _iter_options__eq():
    item_id = 4
    amount_type = AMOUNT_TYPE_VALUE
    amount_required = 5
    amount_submitted = 4
    
    yield (
        (
            item_id,
            amount_type,
            amount_required,
            amount_submitted,
        ),
        (
            item_id,
            amount_type,
            amount_required,
            amount_submitted,
        ),
        True,
    )
    
    yield (
        (
            item_id,
            amount_type,
            amount_required,
            amount_submitted,
        ),
        (
            2,
            amount_type,
            amount_required,
            amount_submitted,
        ),
        False,
    )
    
    yield (
        (
            item_id,
            amount_type,
            amount_required,
            amount_submitted,
        ),
        (
            item_id,
            AMOUNT_TYPE_WEIGHT,
            amount_required,
            amount_submitted,
        ),
        False,
    )
    
    yield (
        (
            item_id,
            amount_type,
            amount_required,
            amount_submitted,
        ),
        (
            item_id,
            amount_type,
            12,
            amount_submitted,
        ),
        False,
    )
    
    yield (
        (
            item_id,
            amount_type,
            amount_required,
            amount_submitted,
        ),
        (
            item_id,
            amount_type,
            amount_required,
            3,
        ),
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__QuestRequirementSerialisableItemExact__eq(position_parameters_0, position_parameters_1):
    """
    Tests whether ``QuestRequirementSerialisableItemExact.__eq__`` works as intended.
    
    Parameters
    ----------
    position_parameters_0 : `tuple<object>`
        Positional parameters to create instance form.
    
    position_parameters_1 : `tuple<object>`
        Positional parameters to create instance form.
    
    Returns
    -------
    output : `bool`
    """
    quest_requirement_serialisable_item_exact_0 = QuestRequirementSerialisableItemExact(*position_parameters_0)
    quest_requirement_serialisable_item_exact_1 = QuestRequirementSerialisableItemExact(*position_parameters_1)
    
    output = quest_requirement_serialisable_item_exact_0 == quest_requirement_serialisable_item_exact_1
    vampytest.assert_instance(output, bool)
    return output


def test__QuestRequirementSerialisableItemExact__deserialise():
    """
    Tests whether ``QuestRequirementSerialisableItemExact.deserialise`` works as as intended.
    """
    item_id = 4
    amount_type = AMOUNT_TYPE_VALUE
    amount_required = 5
    amount_submitted = 4
    
    data = b''.join([
        item_id.to_bytes(4, 'little'),
        amount_type.to_bytes(1, 'little'),
        amount_required.to_bytes(8, 'little'),
        amount_submitted.to_bytes(8, 'little'),
    ])
    start_index = 0
    
    quest_requirement_serialisable_item_exact, end_index = QuestRequirementSerialisableItemExact.deserialise(
        data, start_index
    )
    
    _assert_fields_set(quest_requirement_serialisable_item_exact)
    vampytest.assert_eq(end_index, 21)
    
    vampytest.assert_eq(quest_requirement_serialisable_item_exact.item_id, item_id)
    vampytest.assert_eq(quest_requirement_serialisable_item_exact.amount_type, amount_type)
    vampytest.assert_eq(quest_requirement_serialisable_item_exact.amount_required, amount_required)
    vampytest.assert_eq(quest_requirement_serialisable_item_exact.amount_submitted, amount_submitted)


def test__QuestRequirementSerialisableItemExact__serialise():
    """
    Tests whether ``QuestRequirementSerialisableItemExact.serialise`` works as intended.
    """
    item_id = 4
    amount_type = AMOUNT_TYPE_VALUE
    amount_required = 5
    amount_submitted = 4
    
    quest_requirement_serialisable_item_exact = QuestRequirementSerialisableItemExact(
        item_id,
        amount_type,
        amount_required,
        amount_submitted,
    )
    
    output = [*quest_requirement_serialisable_item_exact.serialise()]
    
    for element in output:
        vampytest.assert_instance(element, bytes)
    
    vampytest.assert_eq(
        b''.join(output),
        b''.join([
            item_id.to_bytes(4, 'little'),
            amount_type.to_bytes(1, 'little'),
            amount_required.to_bytes(8, 'little'),
            amount_submitted.to_bytes(8, 'little'),
        ]),
    )
