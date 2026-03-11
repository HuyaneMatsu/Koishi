import vampytest

from ...amount_types import AMOUNT_TYPE_VALUE, AMOUNT_TYPE_WEIGHT
from ...quest_requirement_serialisables import QuestRequirementSerialisableItemCategory
from ...quest_requirement_types import QUEST_REQUIREMENT_TYPE_ITEM_CATEGORY

from ..item_category import QuestRequirementInstantiableItemCategory


def _assert_fields_set(quest_requirement_instantiable_item_category):
    """
    Asserts whether the instance has all of its fields set.
    
    Parameters
    ----------
    quest_requirement_instantiable_item_category : ``QuestRequirementInstantiableItemCategory``
        The instance to check.
    """
    vampytest.assert_instance(quest_requirement_instantiable_item_category, QuestRequirementInstantiableItemCategory)
    vampytest.assert_eq(quest_requirement_instantiable_item_category.TYPE, QUEST_REQUIREMENT_TYPE_ITEM_CATEGORY)
    vampytest.assert_instance(quest_requirement_instantiable_item_category.amount_type, int)
    vampytest.assert_instance(quest_requirement_instantiable_item_category.amount_required, int)
    vampytest.assert_instance(quest_requirement_instantiable_item_category.item_flags, int)


def test__QuestRequirementInstantiableItemCategory__new():
    """
    Tests whether ``QuestRequirementInstantiableItemCategory.__new__`` works as intended.
    """
    item_flags = 4
    amount_type = AMOUNT_TYPE_VALUE
    amount_required = 5
    
    quest_requirement_instantiable_item_category = QuestRequirementInstantiableItemCategory(
        item_flags,
        amount_type,
        amount_required,
    )
    _assert_fields_set(quest_requirement_instantiable_item_category)
    
    vampytest.assert_eq(quest_requirement_instantiable_item_category.item_flags, item_flags)
    vampytest.assert_eq(quest_requirement_instantiable_item_category.amount_type, amount_type)
    vampytest.assert_eq(quest_requirement_instantiable_item_category.amount_required, amount_required)


def test__QuestRequirementInstantiableItemCategory__repr():
    """
    Tests whether ``QuestRequirementInstantiableItemCategory.__repr__`` works as intended.
    """
    item_flags = 4
    amount_type = AMOUNT_TYPE_VALUE
    amount_required = 5
    
    quest_requirement_instantiable_item_category = QuestRequirementInstantiableItemCategory(
        item_flags,
        amount_type,
        amount_required,
    )
    
    output = repr(quest_requirement_instantiable_item_category)
    vampytest.assert_instance(output, str)


def _iter_options__eq():
    item_flags = 4
    amount_type = AMOUNT_TYPE_VALUE
    amount_required = 5
    
    yield (
        (
            item_flags,
            amount_type,
            amount_required,
        ),
        (
            item_flags,
            amount_type,
            amount_required,
        ),
        True,
    )
    
    yield (
        (
            item_flags,
            amount_type,
            amount_required,
        ),
        (
            2,
            amount_type,
            amount_required,
        ),
        False,
    )
    
    yield (
        (
            item_flags,
            amount_type,
            amount_required,
        ),
        (
            item_flags,
            AMOUNT_TYPE_WEIGHT,
            amount_required,
        ),
        False,
    )
    
    yield (
        (
            item_flags,
            amount_type,
            amount_required,
        ),
        (
            item_flags,
            amount_type,
            10,
        ),
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__QuestRequirementInstantiableItemCategory__eq(position_parameters_0, position_parameters_1):
    """
    Tests whether ``QuestRequirementInstantiableItemCategory.__eq__`` works as intended.
    
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
    quest_requirement_instantiable_item_category_0 = QuestRequirementInstantiableItemCategory(*position_parameters_0)
    quest_requirement_instantiable_item_category_1 = QuestRequirementInstantiableItemCategory(*position_parameters_1)
    
    output = quest_requirement_instantiable_item_category_0 == quest_requirement_instantiable_item_category_1
    vampytest.assert_instance(output, bool)
    return output


def test__QuestRequirementInstantiableItemCategory__instantiate():
    """
    Tests whether ``QuestRequirementInstantiableItemCategory.instantiate`` works as intended.
    """
    item_flags = 4
    amount_type = AMOUNT_TYPE_VALUE
    amount_required = 5
    
    quest_requirement_instantiable_item_category = QuestRequirementInstantiableItemCategory(
        item_flags,
        amount_type,
        amount_required,
    )
    
    output = quest_requirement_instantiable_item_category.instantiate()
    
    vampytest.assert_instance(output, QuestRequirementSerialisableItemCategory)
    vampytest.assert_eq(output.item_flags, item_flags)
    vampytest.assert_eq(output.amount_type, amount_type)
    vampytest.assert_eq(output.amount_required, amount_required)
