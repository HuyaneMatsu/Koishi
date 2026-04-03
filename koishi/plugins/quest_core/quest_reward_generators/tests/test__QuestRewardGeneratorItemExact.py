from random import Random

import vampytest

from ...quest_reward_instantiables import QuestRewardInstantiableItemExact
from ...quest_reward_types import QUEST_REWARD_TYPE_ITEM_EXACT

from ..item_exact import QuestRewardGeneratorItemExact


def _assert_fields_set(quest_reward_generator_item_exact):
    """
    Asserts whether the instance has all of its fields set.
    
    Parameters
    ----------
    quest_reward_generator_item_exact : ``QuestRewardGeneratorItemExact``
        The instance to check.
    """
    vampytest.assert_instance(quest_reward_generator_item_exact, QuestRewardGeneratorItemExact)
    vampytest.assert_eq(quest_reward_generator_item_exact.TYPE, QUEST_REWARD_TYPE_ITEM_EXACT)
    vampytest.assert_instance(quest_reward_generator_item_exact.item_id, int)
    vampytest.assert_instance(quest_reward_generator_item_exact.amount_base, int)
    vampytest.assert_instance(quest_reward_generator_item_exact.amount_require_multiple_of, int)
    vampytest.assert_instance(quest_reward_generator_item_exact.amount_variance_percentage_lower_threshold, int)
    vampytest.assert_instance(quest_reward_generator_item_exact.amount_variance_percentage_upper_threshold, int)


def test__QuestRewardGeneratorItemExact__new():
    """
    Tests whether ``QuestRewardGeneratorItemExact.__new__`` works as intended.
    """
    item_id = 4
    amount_base = 3600
    amount_require_multiple_of = 100
    amount_variance_percentage_lower_threshold = 80
    amount_variance_percentage_upper_threshold = 120
    
    quest_reward_generator_item_exact = QuestRewardGeneratorItemExact(
        item_id,
        amount_base,
        amount_require_multiple_of,
        amount_variance_percentage_lower_threshold,
        amount_variance_percentage_upper_threshold,
    )
    _assert_fields_set(quest_reward_generator_item_exact)
    
    vampytest.assert_eq(quest_reward_generator_item_exact.item_id, item_id)
    vampytest.assert_eq(quest_reward_generator_item_exact.amount_base, amount_base)
    vampytest.assert_eq(
        quest_reward_generator_item_exact.amount_require_multiple_of,
        amount_require_multiple_of,
    )
    vampytest.assert_eq(
        quest_reward_generator_item_exact.amount_variance_percentage_lower_threshold,
        amount_variance_percentage_lower_threshold,
    )
    vampytest.assert_eq(
        quest_reward_generator_item_exact.amount_variance_percentage_upper_threshold,
        amount_variance_percentage_upper_threshold,
    )


def test__QuestRewardGeneratorItemExact__repr():
    """
    Tests whether ``QuestRewardGeneratorItemExact.__repr__`` works as intended.
    """
    item_id = 4
    amount_base = 3600
    amount_require_multiple_of = 100
    amount_variance_percentage_lower_threshold = 80
    amount_variance_percentage_upper_threshold = 120
    
    quest_reward_generator_item_exact = QuestRewardGeneratorItemExact(
        item_id,
        amount_base,
        amount_require_multiple_of,
        amount_variance_percentage_lower_threshold,
        amount_variance_percentage_upper_threshold,
    )
    
    output = repr(quest_reward_generator_item_exact)
    vampytest.assert_instance(output, str)


def _iter_options__eq():
    item_id = 4
    amount_base = 3600
    amount_require_multiple_of = 100
    amount_variance_percentage_lower_threshold = 80
    amount_variance_percentage_upper_threshold = 120
    
    yield (
        (
            item_id,
            amount_base,
            amount_require_multiple_of,
            amount_variance_percentage_lower_threshold,
            amount_variance_percentage_upper_threshold,
        ),
        (
            item_id,
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
            amount_base,
            amount_require_multiple_of,
            amount_variance_percentage_lower_threshold,
            amount_variance_percentage_upper_threshold,
        ),
        (
            2,
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
            amount_base,
            amount_require_multiple_of,
            amount_variance_percentage_lower_threshold,
            amount_variance_percentage_upper_threshold,
        ),
        (
            item_id,
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
            amount_base,
            amount_require_multiple_of,
            amount_variance_percentage_lower_threshold,
            amount_variance_percentage_upper_threshold,
        ),
        (
            item_id,
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
            amount_base,
            amount_require_multiple_of,
            amount_variance_percentage_lower_threshold,
            amount_variance_percentage_upper_threshold,
        ),
        (
            item_id,
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
            amount_base,
            amount_require_multiple_of,
            amount_variance_percentage_lower_threshold,
            amount_variance_percentage_upper_threshold,
        ),
        (
            item_id,
            amount_base,
            amount_require_multiple_of,
            amount_variance_percentage_lower_threshold,
            100,
        ),
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__QuestRewardGeneratorItemExact__eq(position_parameters_0, position_parameters_1):
    """
    Tests whether ``QuestRewardGeneratorItemExact.__eq__`` works as intended.
    
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
    quest_reward_generator_item_exact_0 = QuestRewardGeneratorItemExact(*position_parameters_0)
    quest_reward_generator_item_exact_1 = QuestRewardGeneratorItemExact(*position_parameters_1)
    
    output = quest_reward_generator_item_exact_0 == quest_reward_generator_item_exact_1
    vampytest.assert_instance(output, bool)
    return output


def test__QuestRewardGeneratorItemExact__generate_with_diversion():
    """
    Tests whether ``QuestRewardGeneratorItemExact.generate_with_diversion`` works as intended.
    """
    item_id = 4
    amount_base = 3600
    amount_require_multiple_of = 100
    amount_variance_percentage_lower_threshold = 80
    amount_variance_percentage_upper_threshold = 120
    
    quest_reward_generator_item_exact = QuestRewardGeneratorItemExact(
        item_id,
        amount_base,
        amount_require_multiple_of,
        amount_variance_percentage_lower_threshold,
        amount_variance_percentage_upper_threshold,
    )
    
    random_number_generator = Random(5)
    accumulated_diversion = 2.0
    
    generated, diversion = quest_reward_generator_item_exact.generate_with_diversion(
        random_number_generator, accumulated_diversion
    )
    
    vampytest.assert_eq(
        generated,
        QuestRewardInstantiableItemExact(
            item_id,
            7600,
        ),
    )
    
    vampytest.assert_eq(
        diversion,
        0.9473684210526315,
    )
