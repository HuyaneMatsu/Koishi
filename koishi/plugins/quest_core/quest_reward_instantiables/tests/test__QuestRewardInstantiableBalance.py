import vampytest

from ...quest_reward_serialisables import QuestRewardSerialisableBalance
from ...quest_reward_types import QUEST_REWARD_TYPE_BALANCE

from ..balance import QuestRewardInstantiableBalance


def _assert_fields_set(quest_reward_instantiable_balance):
    """
    Asserts whether the instance has all of its fields set.
    
    Parameters
    ----------
    quest_reward_instantiable_balance : ``QuestRewardInstantiableBalance``
        The instance to check.
    """
    vampytest.assert_instance(quest_reward_instantiable_balance, QuestRewardInstantiableBalance)
    vampytest.assert_eq(quest_reward_instantiable_balance.TYPE, QUEST_REWARD_TYPE_BALANCE)
    vampytest.assert_instance(quest_reward_instantiable_balance.balance, int)


def test__QuestRewardInstantiableBalance__new():
    """
    Tests whether ``QuestRewardInstantiableBalance.__new__`` works as intended.
    """
    balance = 3600
    
    quest_reward_instantiable_balance = QuestRewardInstantiableBalance(
        balance,
    )
    _assert_fields_set(quest_reward_instantiable_balance)
    vampytest.assert_eq(quest_reward_instantiable_balance.balance, balance)


def test__QuestRewardInstantiableBalance__repr():
    """
    Tests whether ``QuestRewardInstantiableBalance.__repr__`` works as intended.
    """
    balance = 3600
    
    quest_reward_instantiable_balance = QuestRewardInstantiableBalance(
        balance,
    )
    
    output = repr(quest_reward_instantiable_balance)
    vampytest.assert_instance(output, str)


def _iter_options__eq():
    balance = 3600
    
    yield (
        (
            balance,
        ),
        (
            balance,
        ),
        True,
    )
    
    yield (
        (
            balance,
        ),
        (
            7200,
        ),
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__QuestRewardInstantiableBalance__eq(position_parameters_0, position_parameters_1):
    """
    Tests whether ``QuestRewardInstantiableBalance.__eq__`` works as intended.
    
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
    quest_reward_instantiable_balance_0 = QuestRewardInstantiableBalance(*position_parameters_0)
    quest_reward_instantiable_balance_1 = QuestRewardInstantiableBalance(*position_parameters_1)
    
    output = quest_reward_instantiable_balance_0 == quest_reward_instantiable_balance_1
    vampytest.assert_instance(output, bool)
    return output


def test__QuestRewardInstantiableBalance__instantiate():
    """
    Tests whether ``QuestRewardInstantiableBalance.instantiate`` works as intended.
    """
    balance = 3600
    
    quest_reward_instantiable_balance = QuestRewardInstantiableBalance(
        balance,
    )
    
    output = quest_reward_instantiable_balance.instantiate()
    
    vampytest.assert_instance(output, QuestRewardSerialisableBalance)
    vampytest.assert_eq(output.balance, balance)
