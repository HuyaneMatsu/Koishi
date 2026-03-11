import vampytest

from ...quest_reward_types import QUEST_REWARD_TYPE_NONE

from ..base import QuestRewardSerialisableBase


def _assert_fields_set(quest_reward_serialisable_base):
    """
    Asserts whether the instance has all of its fields set.
    
    Parameters
    ----------
    quest_reward_serialisable_base : ``QuestRewardSerialisableBase``
        The instance to check.
    """
    vampytest.assert_instance(quest_reward_serialisable_base, QuestRewardSerialisableBase)
    vampytest.assert_eq(quest_reward_serialisable_base.TYPE, QUEST_REWARD_TYPE_NONE)


def test__QuestRewardSerialisableBase__new():
    """
    Tests whether ``QuestRewardSerialisableBase.__new__`` works as intended.
    """
    quest_reward_serialisable_base = QuestRewardSerialisableBase()
    _assert_fields_set(quest_reward_serialisable_base)


def test__QuestRewardSerialisableBase__repr():
    """
    Tests whether ``QuestRewardSerialisableBase.__repr__`` works as intended.
    """
    quest_reward_serialisable_base = QuestRewardSerialisableBase()
    
    output = repr(quest_reward_serialisable_base)
    vampytest.assert_instance(output, str)


def _iter_options__eq():
    yield (
        (),
        (),
        True,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__QuestRewardSerialisableBase__eq(position_parameters_0, position_parameters_1):
    """
    Tests whether ``QuestRewardSerialisableBase.__eq__`` works as intended.
    
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
    quest_reward_serialisable_base_0 = QuestRewardSerialisableBase(*position_parameters_0)
    quest_reward_serialisable_base_1 = QuestRewardSerialisableBase(*position_parameters_1)
    
    output = quest_reward_serialisable_base_0 == quest_reward_serialisable_base_1
    vampytest.assert_instance(output, bool)
    return output


def test__QuestRewardSerialisableBase__deserialise():
    """
    Tests whether ``QuestRewardSerialisableBase.deserialise`` works as as intended.
    """
    data = b''
    start_index = 0
    
    quest_reward_serialisable_base, end_index = QuestRewardSerialisableBase.deserialise(
        data, start_index
    )
    
    _assert_fields_set(quest_reward_serialisable_base)
    vampytest.assert_eq(end_index, 0)


def test__QuestRewardSerialisableBase__serialise():
    """
    Tests whether ``QuestRewardSerialisableBase.serialise`` works as intended.
    """
    quest_reward_serialisable_base = QuestRewardSerialisableBase()
    
    output = [*quest_reward_serialisable_base.serialise()]
    
    for element in output:
        vampytest.assert_instance(element, bytes)
    
    vampytest.assert_eq(
        b''.join(output),
        b'',
    )
