import vampytest

from ...amount_types import AMOUNT_TYPE_VALUE, AMOUNT_TYPE_WEIGHT

from ...quest_requirement_types import QUEST_REQUIREMENT_TYPE_ITEM_CATEGORY

from ..item_category import QuestRequirementSerialisableItemCategory


def _assert_fields_set(quest_requirement_serialisable_item_category):
    """
    Asserts whether the instance has all of its fields set.
    
    Parameters
    ----------
    quest_requirement_serialisable_item_category : ``QuestRequirementSerialisableItemCategory``
        The instance to check.
    """
    vampytest.assert_instance(
        quest_requirement_serialisable_item_category, QuestRequirementSerialisableItemCategory
    )
    vampytest.assert_eq(quest_requirement_serialisable_item_category.TYPE, QUEST_REQUIREMENT_TYPE_ITEM_CATEGORY)
    vampytest.assert_instance(quest_requirement_serialisable_item_category.amount_required, int)
    vampytest.assert_instance(quest_requirement_serialisable_item_category.amount_submitted, int)
    vampytest.assert_instance(quest_requirement_serialisable_item_category.amount_type, int)
    vampytest.assert_instance(quest_requirement_serialisable_item_category.item_flags, int)


def test__QuestRequirementSerialisableItemCategory__new():
    """
    Tests whether ``QuestRequirementSerialisableItemCategory.__new__`` works as intended.
    """
    item_flags = 4
    amount_type = AMOUNT_TYPE_VALUE
    amount_required = 5
    amount_submitted = 4
    
    quest_requirement_serialisable_item_category = QuestRequirementSerialisableItemCategory(
        item_flags,
        amount_type,
        amount_required,
        amount_submitted,
    )
    _assert_fields_set(quest_requirement_serialisable_item_category)
    
    vampytest.assert_eq(quest_requirement_serialisable_item_category.item_flags, item_flags)
    vampytest.assert_eq(quest_requirement_serialisable_item_category.amount_type, amount_type)
    vampytest.assert_eq(quest_requirement_serialisable_item_category.amount_required, amount_required)
    vampytest.assert_eq(quest_requirement_serialisable_item_category.amount_submitted, amount_submitted)


def test__QuestRequirementSerialisableItemCategory__repr():
    """
    Tests whether ``QuestRequirementSerialisableItemCategory.__repr__`` works as intended.
    """
    item_flags = 4
    amount_type = AMOUNT_TYPE_VALUE
    amount_required = 5
    amount_submitted = 4
    
    quest_requirement_serialisable_item_category = QuestRequirementSerialisableItemCategory(
        item_flags,
        amount_type,
        amount_required,
        amount_submitted,
    )
    
    output = repr(quest_requirement_serialisable_item_category)
    vampytest.assert_instance(output, str)


def _iter_options__eq():
    item_flags = 4
    amount_type = AMOUNT_TYPE_VALUE
    amount_required = 5
    amount_submitted = 4
    
    yield (
        (
            item_flags,
            amount_type,
            amount_required,
            amount_submitted,
        ),
        (
            item_flags,
            amount_type,
            amount_required,
            amount_submitted,
        ),
        True,
    )
    
    yield (
        (
            item_flags,
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
            item_flags,
            amount_type,
            amount_required,
            amount_submitted,
        ),
        (
            item_flags,
            AMOUNT_TYPE_WEIGHT,
            amount_required,
            amount_submitted,
        ),
        False,
    )
    
    yield (
        (
            item_flags,
            amount_type,
            amount_required,
            amount_submitted,
        ),
        (
            item_flags,
            amount_type,
            12,
            amount_submitted,
        ),
        False,
    )
    
    yield (
        (
            item_flags,
            amount_type,
            amount_required,
            amount_submitted,
        ),
        (
            item_flags,
            amount_type,
            amount_required,
            3,
        ),
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__QuestRequirementSerialisableItemCategory__eq(position_parameters_0, position_parameters_1):
    """
    Tests whether ``QuestRequirementSerialisableItemCategory.__eq__`` works as intended.
    
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
    quest_requirement_serialisable_item_category_0 = QuestRequirementSerialisableItemCategory(*position_parameters_0)
    quest_requirement_serialisable_item_category_1 = QuestRequirementSerialisableItemCategory(*position_parameters_1)
    
    output = quest_requirement_serialisable_item_category_0 == quest_requirement_serialisable_item_category_1
    vampytest.assert_instance(output, bool)
    return output


def test__QuestRequirementSerialisableItemCategory__deserialise():
    """
    Tests whether ``QuestRequirementSerialisableItemCategory.deserialise`` works as as intended.
    """
    item_flags = 4
    amount_type = AMOUNT_TYPE_VALUE
    amount_required = 5
    amount_submitted = 4
    
    data = b''.join([
        item_flags.to_bytes(8, 'little'),
        amount_type.to_bytes(1, 'little'),
        amount_required.to_bytes(8, 'little'),
        amount_submitted.to_bytes(8, 'little'),
    ])
    start_index = 0
    
    quest_requirement_serialisable_item_category, end_index = QuestRequirementSerialisableItemCategory.deserialise(
        data, start_index
    )
    
    _assert_fields_set(quest_requirement_serialisable_item_category)
    vampytest.assert_eq(end_index, 25)
    
    vampytest.assert_eq(quest_requirement_serialisable_item_category.item_flags, item_flags)
    vampytest.assert_eq(quest_requirement_serialisable_item_category.amount_type, amount_type)
    vampytest.assert_eq(quest_requirement_serialisable_item_category.amount_required, amount_required)
    vampytest.assert_eq(quest_requirement_serialisable_item_category.amount_submitted, amount_submitted)


def test__QuestRequirementSerialisableItemCategory__serialise():
    """
    Tests whether ``QuestRequirementSerialisableItemCategory.serialise`` works as intended.
    """
    item_flags = 4
    amount_type = AMOUNT_TYPE_VALUE
    amount_required = 5
    amount_submitted = 4
    
    quest_requirement_serialisable_item_category = QuestRequirementSerialisableItemCategory(
        item_flags,
        amount_type,
        amount_required,
        amount_submitted,
    )
    
    output = [*quest_requirement_serialisable_item_category.serialise()]
    
    for element in output:
        vampytest.assert_instance(element, bytes)
    
    vampytest.assert_eq(
        b''.join(output),
        b''.join([
            item_flags.to_bytes(8, 'little'),
            amount_type.to_bytes(1, 'little'),
            amount_required.to_bytes(8, 'little'),
            amount_submitted.to_bytes(8, 'little'),
        ]),
    )
