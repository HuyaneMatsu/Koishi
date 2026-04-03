import vampytest

from ...quest_reward_types import QUEST_REWARD_TYPE_CREDIBILITY

from ..credibility import QuestRewardSerialisableCredibility


def _assert_fields_set(quest_reward_serialisable_credibility):
    """
    Asserts whether the instance has all of its fields set.
    
    Parameters
    ----------
    quest_reward_serialisable_credibility : ``QuestRewardSerialisableCredibility``
        The instance to check.
    """
    vampytest.assert_instance(quest_reward_serialisable_credibility, QuestRewardSerialisableCredibility)
    vampytest.assert_eq(quest_reward_serialisable_credibility.TYPE, QUEST_REWARD_TYPE_CREDIBILITY)
    vampytest.assert_instance(quest_reward_serialisable_credibility.credibility, int)


def test__QuestRewardSerialisableCredibility__new():
    """
    Tests whether ``QuestRewardSerialisableCredibility.__new__`` works as intended.
    """
    credibility = 3600
    
    quest_reward_serialisable_credibility = QuestRewardSerialisableCredibility(
        credibility,
    )
    _assert_fields_set(quest_reward_serialisable_credibility)


def test__QuestRewardSerialisableCredibility__repr():
    """
    Tests whether ``QuestRewardSerialisableCredibility.__repr__`` works as intended.
    """
    credibility = 3600
    
    quest_reward_serialisable_credibility = QuestRewardSerialisableCredibility(
        credibility,
    )
    
    output = repr(quest_reward_serialisable_credibility)
    vampytest.assert_instance(output, str)


def _iter_options__eq():
    credibility = 3600
    
    yield (
        (
            credibility,
        ),
        (
            credibility,
        ),
        True,
    )
    
    yield (
        (
            credibility,
        ),
        (
            7200,
        ),
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__QuestRewardSerialisableCredibility__eq(position_parameters_0, position_parameters_1):
    """
    Tests whether ``QuestRewardSerialisableCredibility.__eq__`` works as intended.
    
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
    quest_reward_serialisable_credibility_0 = QuestRewardSerialisableCredibility(*position_parameters_0)
    quest_reward_serialisable_credibility_1 = QuestRewardSerialisableCredibility(*position_parameters_1)
    
    output = quest_reward_serialisable_credibility_0 == quest_reward_serialisable_credibility_1
    vampytest.assert_instance(output, bool)
    return output


def test__QuestRewardSerialisableCredibility__deserialise():
    """
    Tests whether ``QuestRewardSerialisableCredibility.deserialise`` works as as intended.
    """
    credibility = 3600
    
    data = b''.join([
        credibility.to_bytes(8, 'little'),
    ])
    start_index = 0
    
    quest_reward_serialisable_credibility, end_index = QuestRewardSerialisableCredibility.deserialise(
        data, start_index
    )
    
    _assert_fields_set(quest_reward_serialisable_credibility)
    vampytest.assert_eq(end_index, 8)
    
    vampytest.assert_eq(quest_reward_serialisable_credibility.credibility, credibility)


def test__QuestRewardSerialisableCredibility__serialise():
    """
    Tests whether ``QuestRewardSerialisableCredibility.serialise`` works as intended.
    """
    credibility = 3600
    
    quest_reward_serialisable_credibility = QuestRewardSerialisableCredibility(
        credibility,
    )
    
    output = [*quest_reward_serialisable_credibility.serialise()]
    
    for element in output:
        vampytest.assert_instance(element, bytes)
    
    vampytest.assert_eq(
        b''.join(output),
        b''.join([
            credibility.to_bytes(8, 'little'),
        ]),
    )
