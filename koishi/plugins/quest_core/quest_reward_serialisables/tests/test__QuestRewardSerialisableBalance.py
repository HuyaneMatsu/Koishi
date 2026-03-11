import vampytest

from ...quest_reward_types import QUEST_REWARD_TYPE_BALANCE

from ..balance import QuestRewardSerialisableBalance


def _assert_fields_set(quest_reward_serialisable_balance):
    """
    Asserts whether the instance has all of its fields set.
    
    Parameters
    ----------
    quest_reward_serialisable_balance : ``QuestRewardSerialisableBalance``
        The instance to check.
    """
    vampytest.assert_instance(quest_reward_serialisable_balance, QuestRewardSerialisableBalance)
    vampytest.assert_eq(quest_reward_serialisable_balance.TYPE, QUEST_REWARD_TYPE_BALANCE)
    vampytest.assert_instance(quest_reward_serialisable_balance.balance, int)


def test__QuestRewardSerialisableBalance__new():
    """
    Tests whether ``QuestRewardSerialisableBalance.__new__`` works as intended.
    """
    balance = 3600
    
    quest_reward_serialisable_balance = QuestRewardSerialisableBalance(
        balance,
    )
    _assert_fields_set(quest_reward_serialisable_balance)


def test__QuestRewardSerialisableBalance__repr():
    """
    Tests whether ``QuestRewardSerialisableBalance.__repr__`` works as intended.
    """
    balance = 3600
    
    quest_reward_serialisable_balance = QuestRewardSerialisableBalance(
        balance,
    )
    
    output = repr(quest_reward_serialisable_balance)
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
def test__QuestRewardSerialisableBalance__eq(position_parameters_0, position_parameters_1):
    """
    Tests whether ``QuestRewardSerialisableBalance.__eq__`` works as intended.
    
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
    quest_reward_serialisable_balance_0 = QuestRewardSerialisableBalance(*position_parameters_0)
    quest_reward_serialisable_balance_1 = QuestRewardSerialisableBalance(*position_parameters_1)
    
    output = quest_reward_serialisable_balance_0 == quest_reward_serialisable_balance_1
    vampytest.assert_instance(output, bool)
    return output


def test__QuestRewardSerialisableBalance__deserialise():
    """
    Tests whether ``QuestRewardSerialisableBalance.deserialise`` works as as intended.
    """
    balance = 3600
    
    data = b''.join([
        balance.to_bytes(8, 'little'),
    ])
    start_index = 0
    
    quest_reward_serialisable_balance, end_index = QuestRewardSerialisableBalance.deserialise(
        data, start_index
    )
    
    _assert_fields_set(quest_reward_serialisable_balance)
    vampytest.assert_eq(end_index, 8)
    
    vampytest.assert_eq(quest_reward_serialisable_balance.balance, balance)


def test__QuestRewardSerialisableBalance__serialise():
    """
    Tests whether ``QuestRewardSerialisableBalance.serialise`` works as intended.
    """
    balance = 3600
    
    quest_reward_serialisable_balance = QuestRewardSerialisableBalance(
        balance,
    )
    
    output = [*quest_reward_serialisable_balance.serialise()]
    
    for element in output:
        vampytest.assert_instance(element, bytes)
    
    vampytest.assert_eq(
        b''.join(output),
        b''.join([
            balance.to_bytes(8, 'little'),
        ]),
    )
