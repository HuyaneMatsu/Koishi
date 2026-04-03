from random import Random

import vampytest

from ...amount_types import AMOUNT_TYPE_VALUE, AMOUNT_TYPE_WEIGHT
from ...quest_requirement_instantiables import QuestRequirementInstantiableItemExact
from ...quest_requirement_types import QUEST_REQUIREMENT_TYPE_ITEM_EXACT

from ..item_exact import QuestRequirementGeneratorItemExact


def _assert_fields_set(quest_requirement_generator_item_exact):
    """
    Asserts whether the instance has all of its fields set.
    
    Parameters
    ----------
    quest_requirement_generator_item_exact : ``QuestRequirementGeneratorItemExact``
        The instance to check.
    """
    vampytest.assert_instance(quest_requirement_generator_item_exact, QuestRequirementGeneratorItemExact)
    vampytest.assert_eq(quest_requirement_generator_item_exact.TYPE, QUEST_REQUIREMENT_TYPE_ITEM_EXACT)
    vampytest.assert_instance(quest_requirement_generator_item_exact.item_id, int)
    vampytest.assert_instance(quest_requirement_generator_item_exact.amount_base, int)
    vampytest.assert_instance(quest_requirement_generator_item_exact.amount_require_multiple_of, int)
    vampytest.assert_instance(quest_requirement_generator_item_exact.amount_type, int)
    vampytest.assert_instance(quest_requirement_generator_item_exact.amount_variance_percentage_lower_threshold, int)
    vampytest.assert_instance(quest_requirement_generator_item_exact.amount_variance_percentage_upper_threshold, int)


def test__QuestRequirementGeneratorItemExact__new():
    """
    Tests whether ``QuestRequirementGeneratorItemExact.__new__`` works as intended.
    """
    item_id = 4
    amount_type = AMOUNT_TYPE_WEIGHT
    amount_base = 3600
    amount_require_multiple_of = 100
    amount_variance_percentage_lower_threshold = 80
    amount_variance_percentage_upper_threshold = 120
    
    quest_requirement_generator_item_exact = QuestRequirementGeneratorItemExact(
        item_id,
        amount_type,
        amount_base,
        amount_require_multiple_of,
        amount_variance_percentage_lower_threshold,
        amount_variance_percentage_upper_threshold,
    )
    _assert_fields_set(quest_requirement_generator_item_exact)
    
    vampytest.assert_eq(quest_requirement_generator_item_exact.item_id, item_id)
    vampytest.assert_eq(quest_requirement_generator_item_exact.amount_type, amount_type)
    vampytest.assert_eq(quest_requirement_generator_item_exact.amount_base, amount_base)
    vampytest.assert_eq(
        quest_requirement_generator_item_exact.amount_require_multiple_of,
        amount_require_multiple_of,
    )
    vampytest.assert_eq(
        quest_requirement_generator_item_exact.amount_variance_percentage_lower_threshold,
        amount_variance_percentage_lower_threshold,
    )
    vampytest.assert_eq(
        quest_requirement_generator_item_exact.amount_variance_percentage_upper_threshold,
        amount_variance_percentage_upper_threshold,
    )


def test__QuestRequirementGeneratorItemExact__repr():
    """
    Tests whether ``QuestRequirementGeneratorItemExact.__repr__`` works as intended.
    """
    item_id = 4
    amount_type = AMOUNT_TYPE_WEIGHT
    amount_base = 3600
    amount_require_multiple_of = 100
    amount_variance_percentage_lower_threshold = 80
    amount_variance_percentage_upper_threshold = 120
    
    quest_requirement_generator_item_exact = QuestRequirementGeneratorItemExact(
        item_id,
        amount_type,
        amount_base,
        amount_require_multiple_of,
        amount_variance_percentage_lower_threshold,
        amount_variance_percentage_upper_threshold,
    )
    
    output = repr(quest_requirement_generator_item_exact)
    vampytest.assert_instance(output, str)


def _iter_options__eq():
    item_id = 4
    amount_type = AMOUNT_TYPE_WEIGHT
    amount_base = 3600
    amount_require_multiple_of = 100
    amount_variance_percentage_lower_threshold = 80
    amount_variance_percentage_upper_threshold = 120
    
    yield (
        (
            item_id,
            amount_type,
            amount_base,
            amount_require_multiple_of,
            amount_variance_percentage_lower_threshold,
            amount_variance_percentage_upper_threshold,
        ),
        (
            item_id,
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
            item_id,
            amount_type,
            amount_base,
            amount_require_multiple_of,
            amount_variance_percentage_lower_threshold,
            amount_variance_percentage_upper_threshold,
        ),
        (
            item_id,
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
            item_id,
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
            item_id,
            amount_type,
            amount_base,
            amount_require_multiple_of,
            amount_variance_percentage_lower_threshold,
            amount_variance_percentage_upper_threshold,
        ),
        (
            item_id,
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
            item_id,
            amount_type,
            amount_base,
            amount_require_multiple_of,
            amount_variance_percentage_lower_threshold,
            amount_variance_percentage_upper_threshold,
        ),
        (
            item_id,
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
            item_id,
            amount_type,
            amount_base,
            amount_require_multiple_of,
            amount_variance_percentage_lower_threshold,
            amount_variance_percentage_upper_threshold,
        ),
        (
            item_id,
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
            item_id,
            amount_type,
            amount_base,
            amount_require_multiple_of,
            amount_variance_percentage_lower_threshold,
            amount_variance_percentage_upper_threshold,
        ),
        (
            item_id,
            amount_type,
            amount_base,
            amount_require_multiple_of,
            amount_variance_percentage_lower_threshold,
            100,
        ),
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__QuestRequirementGeneratorItemExact__eq(position_parameters_0, position_parameters_1):
    """
    Tests whether ``QuestRequirementGeneratorItemExact.__eq__`` works as intended.
    
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
    quest_requirement_generator_item_exact_0 = QuestRequirementGeneratorItemExact(*position_parameters_0)
    quest_requirement_generator_item_exact_1 = QuestRequirementGeneratorItemExact(*position_parameters_1)
    
    output = quest_requirement_generator_item_exact_0 == quest_requirement_generator_item_exact_1
    vampytest.assert_instance(output, bool)
    return output


def test__QuestRequirementGeneratorItemExact__generate():
    """
    Tests whether ``QuestRequirementGeneratorItemExact.generate`` works as intended.
    """
    item_id = 4
    amount_type = AMOUNT_TYPE_WEIGHT
    amount_base = 3600
    amount_require_multiple_of = 100
    amount_variance_percentage_lower_threshold = 80
    amount_variance_percentage_upper_threshold = 120
    
    quest_requirement_generator_item_exact = QuestRequirementGeneratorItemExact(
        item_id,
        amount_type,
        amount_base,
        amount_require_multiple_of,
        amount_variance_percentage_lower_threshold,
        amount_variance_percentage_upper_threshold,
    )
    
    random_number_generator = Random(5)
    
    generated, diversion = quest_requirement_generator_item_exact.generate(random_number_generator)
    
    vampytest.assert_eq(
        generated,
        QuestRequirementInstantiableItemExact(
            item_id,
            amount_type,
            3800,
        ),
    )
    
    vampytest.assert_eq(
        diversion,
        1.0555555555555556,
    )
