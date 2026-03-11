from random import Random

import vampytest

from ...quest_reward_instantiables import QuestRewardInstantiableBalance
from ...quest_reward_types import QUEST_REWARD_TYPE_BALANCE

from ..balance import QuestRewardGeneratorBalance


def _assert_fields_set(quest_reward_generator_balance):
    """
    Asserts whether the instance has all of its fields set.
    
    Parameters
    ----------
    quest_reward_generator_balance : ``QuestRewardGeneratorBalance``
        The instance to check.
    """
    vampytest.assert_instance(quest_reward_generator_balance, QuestRewardGeneratorBalance)
    vampytest.assert_eq(quest_reward_generator_balance.TYPE, QUEST_REWARD_TYPE_BALANCE)
    vampytest.assert_instance(quest_reward_generator_balance.balance_base, int)
    vampytest.assert_instance(quest_reward_generator_balance.balance_require_multiple_of, int)
    vampytest.assert_instance(quest_reward_generator_balance.balance_variance_percentage_lower_threshold, int)
    vampytest.assert_instance(quest_reward_generator_balance.balance_variance_percentage_upper_threshold, int)


def test__QuestRewardGeneratorBalance__new():
    """
    Tests whether ``QuestRewardGeneratorBalance.__new__`` works as intended.
    """
    balance_base = 3600
    balance_require_multiple_of = 100
    balance_variance_percentage_lower_threshold = 80
    balance_variance_percentage_upper_threshold = 120
    
    quest_reward_generator_balance = QuestRewardGeneratorBalance(
        balance_base,
        balance_require_multiple_of,
        balance_variance_percentage_lower_threshold,
        balance_variance_percentage_upper_threshold,
    )
    _assert_fields_set(quest_reward_generator_balance)
    
    vampytest.assert_eq(quest_reward_generator_balance.balance_base, balance_base)
    vampytest.assert_eq(
        quest_reward_generator_balance.balance_require_multiple_of,
        balance_require_multiple_of,
    )
    vampytest.assert_eq(
        quest_reward_generator_balance.balance_variance_percentage_lower_threshold,
        balance_variance_percentage_lower_threshold,
    )
    vampytest.assert_eq(
        quest_reward_generator_balance.balance_variance_percentage_upper_threshold,
        balance_variance_percentage_upper_threshold,
    )


def test__QuestRewardGeneratorBalance__repr():
    """
    Tests whether ``QuestRewardGeneratorBalance.__repr__`` works as intended.
    """
    balance_base = 3600
    balance_require_multiple_of = 100
    balance_variance_percentage_lower_threshold = 80
    balance_variance_percentage_upper_threshold = 120
    
    quest_reward_generator_balance = QuestRewardGeneratorBalance(
        balance_base,
        balance_require_multiple_of,
        balance_variance_percentage_lower_threshold,
        balance_variance_percentage_upper_threshold,
    )
    
    output = repr(quest_reward_generator_balance)
    vampytest.assert_instance(output, str)


def _iter_options__eq():
    balance_base = 3600
    balance_require_multiple_of = 100
    balance_variance_percentage_lower_threshold = 80
    balance_variance_percentage_upper_threshold = 120
    
    yield (
        (
            balance_base,
            balance_require_multiple_of,
            balance_variance_percentage_lower_threshold,
            balance_variance_percentage_upper_threshold,
        ),
        (
            balance_base,
            balance_require_multiple_of,
            balance_variance_percentage_lower_threshold,
            balance_variance_percentage_upper_threshold,
        ),
        True,
    )
    
    yield (
        (
            balance_base,
            balance_require_multiple_of,
            balance_variance_percentage_lower_threshold,
            balance_variance_percentage_upper_threshold,
        ),
        (
            7200,
            balance_require_multiple_of,
            balance_variance_percentage_lower_threshold,
            balance_variance_percentage_upper_threshold,
        ),
        False,
    )
    
    yield (
        (
            balance_base,
            balance_require_multiple_of,
            balance_variance_percentage_lower_threshold,
            balance_variance_percentage_upper_threshold,
        ),
        (
            balance_base,
            200,
            balance_variance_percentage_lower_threshold,
            balance_variance_percentage_upper_threshold,
        ),
        False,
    )
    
    yield (
        (
            balance_base,
            balance_require_multiple_of,
            balance_variance_percentage_lower_threshold,
            balance_variance_percentage_upper_threshold,
        ),
        (
            balance_base,
            balance_require_multiple_of,
            100,
            balance_variance_percentage_upper_threshold,
        ),
        False,
    )
    
    yield (
        (
            balance_base,
            balance_require_multiple_of,
            balance_variance_percentage_lower_threshold,
            balance_variance_percentage_upper_threshold,
        ),
        (
            balance_base,
            balance_require_multiple_of,
            balance_variance_percentage_lower_threshold,
            100,
        ),
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__QuestRewardGeneratorBalance__eq(position_parameters_0, position_parameters_1):
    """
    Tests whether ``QuestRewardGeneratorBalance.__eq__`` works as intended.
    
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
    quest_reward_generator_balance_0 = QuestRewardGeneratorBalance(*position_parameters_0)
    quest_reward_generator_balance_1 = QuestRewardGeneratorBalance(*position_parameters_1)
    
    output = quest_reward_generator_balance_0 == quest_reward_generator_balance_1
    vampytest.assert_instance(output, bool)
    return output


def test__QuestRewardGeneratorBalance__generate_with_diversion():
    """
    Tests whether ``QuestRewardGeneratorBalance.generate_with_diversion`` works as intended.
    """
    balance_base = 3600
    balance_require_multiple_of = 100
    balance_variance_percentage_lower_threshold = 80
    balance_variance_percentage_upper_threshold = 120
    
    quest_reward_generator_balance = QuestRewardGeneratorBalance(
        balance_base,
        balance_require_multiple_of,
        balance_variance_percentage_lower_threshold,
        balance_variance_percentage_upper_threshold,
    )
    
    random_number_generator = Random(5)
    accumulated_diversion = 2.0
    
    generated, diversion = quest_reward_generator_balance.generate_with_diversion(
        random_number_generator, accumulated_diversion
    )
    
    vampytest.assert_eq(
        generated,
        QuestRewardInstantiableBalance(
            7600,
        ),
    )
    
    vampytest.assert_eq(
        diversion,
        0.9473684210526315,
    )
