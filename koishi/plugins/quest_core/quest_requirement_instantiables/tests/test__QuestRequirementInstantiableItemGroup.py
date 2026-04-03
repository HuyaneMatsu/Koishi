import vampytest

from ...amount_types import AMOUNT_TYPE_VALUE, AMOUNT_TYPE_WEIGHT
from ...quest_requirement_serialisables import QuestRequirementSerialisableItemGroup
from ...quest_requirement_types import QUEST_REQUIREMENT_TYPE_ITEM_GROUP

from ..item_group import QuestRequirementInstantiableItemGroup


def _assert_fields_set(quest_requirement_instantiable_item_group):
    """
    Asserts whether the instance has all of its fields set.
    
    Parameters
    ----------
    quest_requirement_instantiable_item_group : ``QuestRequirementInstantiableItemGroup``
        The instance to check.
    """
    vampytest.assert_instance(quest_requirement_instantiable_item_group, QuestRequirementInstantiableItemGroup)
    vampytest.assert_eq(quest_requirement_instantiable_item_group.TYPE, QUEST_REQUIREMENT_TYPE_ITEM_GROUP)
    vampytest.assert_instance(quest_requirement_instantiable_item_group.amount_type, int)
    vampytest.assert_instance(quest_requirement_instantiable_item_group.amount_required, int)
    vampytest.assert_instance(quest_requirement_instantiable_item_group.item_group_id, int)


def test__QuestRequirementInstantiableItemGroup__new():
    """
    Tests whether ``QuestRequirementInstantiableItemGroup.__new__`` works as intended.
    """
    item_group_id = 4
    amount_type = AMOUNT_TYPE_VALUE
    amount_required = 5
    
    quest_requirement_instantiable_item_group = QuestRequirementInstantiableItemGroup(
        item_group_id,
        amount_type,
        amount_required,
    )
    _assert_fields_set(quest_requirement_instantiable_item_group)
    
    vampytest.assert_eq(quest_requirement_instantiable_item_group.item_group_id, item_group_id)
    vampytest.assert_eq(quest_requirement_instantiable_item_group.amount_type, amount_type)
    vampytest.assert_eq(quest_requirement_instantiable_item_group.amount_required, amount_required)


def test__QuestRequirementInstantiableItemGroup__repr():
    """
    Tests whether ``QuestRequirementInstantiableItemGroup.__repr__`` works as intended.
    """
    item_group_id = 4
    amount_type = AMOUNT_TYPE_VALUE
    amount_required = 5
    
    quest_requirement_instantiable_item_group = QuestRequirementInstantiableItemGroup(
        item_group_id,
        amount_type,
        amount_required,
    )
    
    output = repr(quest_requirement_instantiable_item_group)
    vampytest.assert_instance(output, str)


def _iter_options__eq():
    item_group_id = 4
    amount_type = AMOUNT_TYPE_VALUE
    amount_required = 5
    
    yield (
        (
            item_group_id,
            amount_type,
            amount_required,
        ),
        (
            item_group_id,
            amount_type,
            amount_required,
        ),
        True,
    )
    
    yield (
        (
            item_group_id,
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
            item_group_id,
            amount_type,
            amount_required,
        ),
        (
            item_group_id,
            AMOUNT_TYPE_WEIGHT,
            amount_required,
        ),
        False,
    )
    
    yield (
        (
            item_group_id,
            amount_type,
            amount_required,
        ),
        (
            item_group_id,
            amount_type,
            10,
        ),
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__QuestRequirementInstantiableItemGroup__eq(position_parameters_0, position_parameters_1):
    """
    Tests whether ``QuestRequirementInstantiableItemGroup.__eq__`` works as intended.
    
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
    quest_requirement_instantiable_item_group_0 = QuestRequirementInstantiableItemGroup(*position_parameters_0)
    quest_requirement_instantiable_item_group_1 = QuestRequirementInstantiableItemGroup(*position_parameters_1)
    
    output = quest_requirement_instantiable_item_group_0 == quest_requirement_instantiable_item_group_1
    vampytest.assert_instance(output, bool)
    return output


def test__QuestRequirementInstantiableItemGroup__instantiate():
    """
    Tests whether ``QuestRequirementInstantiableItemGroup.instantiate`` works as intended.
    """
    item_group_id = 4
    amount_type = AMOUNT_TYPE_VALUE
    amount_required = 5
    
    quest_requirement_instantiable_item_group = QuestRequirementInstantiableItemGroup(
        item_group_id,
        amount_type,
        amount_required,
    )
    
    output = quest_requirement_instantiable_item_group.instantiate()
    
    vampytest.assert_instance(output, QuestRequirementSerialisableItemGroup)
    vampytest.assert_eq(output.item_group_id, item_group_id)
    vampytest.assert_eq(output.amount_type, amount_type)
    vampytest.assert_eq(output.amount_required, amount_required)
