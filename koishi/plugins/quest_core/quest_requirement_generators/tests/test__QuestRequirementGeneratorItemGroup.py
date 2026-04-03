from random import Random

import vampytest

from ...amount_types import AMOUNT_TYPE_VALUE, AMOUNT_TYPE_WEIGHT
from ...quest_requirement_instantiables import QuestRequirementInstantiableItemGroup
from ...quest_requirement_types import QUEST_REQUIREMENT_TYPE_ITEM_GROUP

from ..item_group import QuestRequirementGeneratorItemGroup


def _assert_fields_set(quest_requirement_generator_item_group):
    """
    Asserts whether the instance has all of its fields set.
    
    Parameters
    ----------
    quest_requirement_generator_item_group : ``QuestRequirementGeneratorItemGroup``
        The instance to check.
    """
    vampytest.assert_instance(quest_requirement_generator_item_group, QuestRequirementGeneratorItemGroup)
    vampytest.assert_eq(quest_requirement_generator_item_group.TYPE, QUEST_REQUIREMENT_TYPE_ITEM_GROUP)
    vampytest.assert_instance(quest_requirement_generator_item_group.item_group_id, int)
    vampytest.assert_instance(quest_requirement_generator_item_group.amount_base, int)
    vampytest.assert_instance(quest_requirement_generator_item_group.amount_require_multiple_of, int)
    vampytest.assert_instance(quest_requirement_generator_item_group.amount_type, int)
    vampytest.assert_instance(quest_requirement_generator_item_group.amount_variance_percentage_lower_threshold, int)
    vampytest.assert_instance(quest_requirement_generator_item_group.amount_variance_percentage_upper_threshold, int)


def test__QuestRequirementGeneratorItemGroup__new():
    """
    Tests whether ``QuestRequirementGeneratorItemGroup.__new__`` works as intended.
    """
    item_group_id = 4
    amount_type = AMOUNT_TYPE_WEIGHT
    amount_base = 3600
    amount_require_multiple_of = 100
    amount_variance_percentage_lower_threshold = 80
    amount_variance_percentage_upper_threshold = 120
    
    quest_requirement_generator_item_group = QuestRequirementGeneratorItemGroup(
        item_group_id,
        amount_type,
        amount_base,
        amount_require_multiple_of,
        amount_variance_percentage_lower_threshold,
        amount_variance_percentage_upper_threshold,
    )
    _assert_fields_set(quest_requirement_generator_item_group)
    
    vampytest.assert_eq(quest_requirement_generator_item_group.item_group_id, item_group_id)
    vampytest.assert_eq(quest_requirement_generator_item_group.amount_type, amount_type)
    vampytest.assert_eq(quest_requirement_generator_item_group.amount_base, amount_base)
    vampytest.assert_eq(
        quest_requirement_generator_item_group.amount_require_multiple_of,
        amount_require_multiple_of,
    )
    vampytest.assert_eq(
        quest_requirement_generator_item_group.amount_variance_percentage_lower_threshold,
        amount_variance_percentage_lower_threshold,
    )
    vampytest.assert_eq(
        quest_requirement_generator_item_group.amount_variance_percentage_upper_threshold,
        amount_variance_percentage_upper_threshold,
    )


def test__QuestRequirementGeneratorItemGroup__repr():
    """
    Tests whether ``QuestRequirementGeneratorItemGroup.__repr__`` works as intended.
    """
    item_group_id = 4
    amount_type = AMOUNT_TYPE_WEIGHT
    amount_base = 3600
    amount_require_multiple_of = 100
    amount_variance_percentage_lower_threshold = 80
    amount_variance_percentage_upper_threshold = 120
    
    quest_requirement_generator_item_group = QuestRequirementGeneratorItemGroup(
        item_group_id,
        amount_type,
        amount_base,
        amount_require_multiple_of,
        amount_variance_percentage_lower_threshold,
        amount_variance_percentage_upper_threshold,
    )
    
    output = repr(quest_requirement_generator_item_group)
    vampytest.assert_instance(output, str)


def _iter_options__eq():
    item_group_id = 4
    amount_type = AMOUNT_TYPE_WEIGHT
    amount_base = 3600
    amount_require_multiple_of = 100
    amount_variance_percentage_lower_threshold = 80
    amount_variance_percentage_upper_threshold = 120
    
    yield (
        (
            item_group_id,
            amount_type,
            amount_base,
            amount_require_multiple_of,
            amount_variance_percentage_lower_threshold,
            amount_variance_percentage_upper_threshold,
        ),
        (
            item_group_id,
            amount_type,
            amount_base,
            amount_require_multiple_of,
            amount_variance_percentage_lower_threshold,
            amount_variance_percentage_upper_threshold,
        ),
        True,
    )
    
    yield (
        (
            item_group_id,
            amount_type,
            amount_base,
            amount_require_multiple_of,
            amount_variance_percentage_lower_threshold,
            amount_variance_percentage_upper_threshold,
        ),
        (
            item_group_id,
            AMOUNT_TYPE_VALUE,
            amount_base,
            amount_require_multiple_of,
            amount_variance_percentage_lower_threshold,
            amount_variance_percentage_upper_threshold,
        ),
        False,
    )
    
    yield (
        (
            item_group_id,
            amount_type,
            amount_base,
            amount_require_multiple_of,
            amount_variance_percentage_lower_threshold,
            amount_variance_percentage_upper_threshold,
        ),
        (
            2,
            amount_type,
            amount_base,
            amount_require_multiple_of,
            amount_variance_percentage_lower_threshold,
            amount_variance_percentage_upper_threshold,
        ),
        False,
    )
    
    yield (
        (
            item_group_id,
            amount_type,
            amount_base,
            amount_require_multiple_of,
            amount_variance_percentage_lower_threshold,
            amount_variance_percentage_upper_threshold,
        ),
        (
            item_group_id,
            amount_type,
            7200,
            amount_require_multiple_of,
            amount_variance_percentage_lower_threshold,
            amount_variance_percentage_upper_threshold,
        ),
        False,
    )
    
    yield (
        (
            item_group_id,
            amount_type,
            amount_base,
            amount_require_multiple_of,
            amount_variance_percentage_lower_threshold,
            amount_variance_percentage_upper_threshold,
        ),
        (
            item_group_id,
            amount_type,
            amount_base,
            200,
            amount_variance_percentage_lower_threshold,
            amount_variance_percentage_upper_threshold,
        ),
        False,
    )
    
    yield (
        (
            item_group_id,
            amount_type,
            amount_base,
            amount_require_multiple_of,
            amount_variance_percentage_lower_threshold,
            amount_variance_percentage_upper_threshold,
        ),
        (
            item_group_id,
            amount_type,
            amount_base,
            amount_require_multiple_of,
            100,
            amount_variance_percentage_upper_threshold,
        ),
        False,
    )
    
    yield (
        (
            item_group_id,
            amount_type,
            amount_base,
            amount_require_multiple_of,
            amount_variance_percentage_lower_threshold,
            amount_variance_percentage_upper_threshold,
        ),
        (
            item_group_id,
            amount_type,
            amount_base,
            amount_require_multiple_of,
            amount_variance_percentage_lower_threshold,
            100,
        ),
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__QuestRequirementGeneratorItemGroup__eq(position_parameters_0, position_parameters_1):
    """
    Tests whether ``QuestRequirementGeneratorItemGroup.__eq__`` works as intended.
    
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
    quest_requirement_generator_item_group_0 = QuestRequirementGeneratorItemGroup(*position_parameters_0)
    quest_requirement_generator_item_group_1 = QuestRequirementGeneratorItemGroup(*position_parameters_1)
    
    output = quest_requirement_generator_item_group_0 == quest_requirement_generator_item_group_1
    vampytest.assert_instance(output, bool)
    return output


def test__QuestRequirementGeneratorItemGroup__generate():
    """
    Tests whether ``QuestRequirementGeneratorItemGroup.generate`` works as intended.
    """
    item_group_id = 4
    amount_type = AMOUNT_TYPE_WEIGHT
    amount_base = 3600
    amount_require_multiple_of = 100
    amount_variance_percentage_lower_threshold = 80
    amount_variance_percentage_upper_threshold = 120
    
    quest_requirement_generator_item_group = QuestRequirementGeneratorItemGroup(
        item_group_id,
        amount_type,
        amount_base,
        amount_require_multiple_of,
        amount_variance_percentage_lower_threshold,
        amount_variance_percentage_upper_threshold,
    )
    
    random_number_generator = Random(5)
    
    generated, diversion = quest_requirement_generator_item_group.generate(random_number_generator)
    
    vampytest.assert_eq(
        generated,
        QuestRequirementInstantiableItemGroup(
            item_group_id,
            amount_type,
            3800,
        ),
    )
    
    vampytest.assert_eq(
        diversion,
        1.0555555555555556,
    )
