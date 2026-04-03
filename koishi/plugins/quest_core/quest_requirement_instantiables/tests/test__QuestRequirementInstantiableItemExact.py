import vampytest

from ...amount_types import AMOUNT_TYPE_VALUE, AMOUNT_TYPE_WEIGHT
from ...quest_requirement_serialisables import QuestRequirementSerialisableItemExact
from ...quest_requirement_types import QUEST_REQUIREMENT_TYPE_ITEM_EXACT

from ..item_exact import QuestRequirementInstantiableItemExact


def _assert_fields_set(quest_requirement_instantiable_item_exact):
    """
    Asserts whether the instance has all of its fields set.
    
    Parameters
    ----------
    quest_requirement_instantiable_item_exact : ``QuestRequirementInstantiableItemExact``
        The instance to check.
    """
    vampytest.assert_instance(quest_requirement_instantiable_item_exact, QuestRequirementInstantiableItemExact)
    vampytest.assert_eq(quest_requirement_instantiable_item_exact.TYPE, QUEST_REQUIREMENT_TYPE_ITEM_EXACT)
    vampytest.assert_instance(quest_requirement_instantiable_item_exact.amount_type, int)
    vampytest.assert_instance(quest_requirement_instantiable_item_exact.amount_required, int)
    vampytest.assert_instance(quest_requirement_instantiable_item_exact.item_id, int)


def test__QuestRequirementInstantiableItemExact__new():
    """
    Tests whether ``QuestRequirementInstantiableItemExact.__new__`` works as intended.
    """
    item_id = 4
    amount_type = AMOUNT_TYPE_VALUE
    amount_required = 5
    
    quest_requirement_instantiable_item_exact = QuestRequirementInstantiableItemExact(
        item_id,
        amount_type,
        amount_required,
    )
    _assert_fields_set(quest_requirement_instantiable_item_exact)
    
    vampytest.assert_eq(quest_requirement_instantiable_item_exact.item_id, item_id)
    vampytest.assert_eq(quest_requirement_instantiable_item_exact.amount_type, amount_type)
    vampytest.assert_eq(quest_requirement_instantiable_item_exact.amount_required, amount_required)


def test__QuestRequirementInstantiableItemExact__repr():
    """
    Tests whether ``QuestRequirementInstantiableItemExact.__repr__`` works as intended.
    """
    item_id = 4
    amount_type = AMOUNT_TYPE_VALUE
    amount_required = 5
    
    quest_requirement_instantiable_item_exact = QuestRequirementInstantiableItemExact(
        item_id,
        amount_type,
        amount_required,
    )
    
    output = repr(quest_requirement_instantiable_item_exact)
    vampytest.assert_instance(output, str)


def _iter_options__eq():
    item_id = 4
    amount_type = AMOUNT_TYPE_VALUE
    amount_required = 5
    
    yield (
        (
            item_id,
            amount_type,
            amount_required,
        ),
        (
            item_id,
            amount_type,
            amount_required,
        ),
        True,
    )
    
    yield (
        (
            item_id,
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
            item_id,
            amount_type,
            amount_required,
        ),
        (
            item_id,
            AMOUNT_TYPE_WEIGHT,
            amount_required,
        ),
        False,
    )
    
    yield (
        (
            item_id,
            amount_type,
            amount_required,
        ),
        (
            item_id,
            amount_type,
            10,
        ),
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__QuestRequirementInstantiableItemExact__eq(position_parameters_0, position_parameters_1):
    """
    Tests whether ``QuestRequirementInstantiableItemExact.__eq__`` works as intended.
    
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
    quest_requirement_instantiable_item_exact_0 = QuestRequirementInstantiableItemExact(*position_parameters_0)
    quest_requirement_instantiable_item_exact_1 = QuestRequirementInstantiableItemExact(*position_parameters_1)
    
    output = quest_requirement_instantiable_item_exact_0 == quest_requirement_instantiable_item_exact_1
    vampytest.assert_instance(output, bool)
    return output


def test__QuestRequirementInstantiableItemExact__instantiate():
    """
    Tests whether ``QuestRequirementInstantiableItemExact.instantiate`` works as intended.
    """
    item_id = 4
    amount_type = AMOUNT_TYPE_VALUE
    amount_required = 5
    
    quest_requirement_instantiable_item_exact = QuestRequirementInstantiableItemExact(
        item_id,
        amount_type,
        amount_required,
    )
    
    output = quest_requirement_instantiable_item_exact.instantiate()
    
    vampytest.assert_instance(output, QuestRequirementSerialisableItemExact)
    vampytest.assert_eq(output.item_id, item_id)
    vampytest.assert_eq(output.amount_type, amount_type)
    vampytest.assert_eq(output.amount_required, amount_required)
