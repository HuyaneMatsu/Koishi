import vampytest

from ...quest_reward_serialisables import QuestRewardSerialisableCredibility
from ...quest_reward_types import QUEST_REWARD_TYPE_CREDIBILITY

from ..credibility import QuestRewardInstantiableCredibility


def _assert_fields_set(quest_reward_instantiable_credibility):
    """
    Asserts whether the instance has all of its fields set.
    
    Parameters
    ----------
    quest_reward_instantiable_credibility : ``QuestRewardInstantiableCredibility``
        The instance to check.
    """
    vampytest.assert_instance(quest_reward_instantiable_credibility, QuestRewardInstantiableCredibility)
    vampytest.assert_eq(quest_reward_instantiable_credibility.TYPE, QUEST_REWARD_TYPE_CREDIBILITY)
    vampytest.assert_instance(quest_reward_instantiable_credibility.credibility, int)


def test__QuestRewardInstantiableCredibility__new():
    """
    Tests whether ``QuestRewardInstantiableCredibility.__new__`` works as intended.
    """
    credibility = 3600
    
    quest_reward_instantiable_credibility = QuestRewardInstantiableCredibility(
        credibility,
    )
    _assert_fields_set(quest_reward_instantiable_credibility)
    vampytest.assert_eq(quest_reward_instantiable_credibility.credibility, credibility)


def test__QuestRewardInstantiableCredibility__repr():
    """
    Tests whether ``QuestRewardInstantiableCredibility.__repr__`` works as intended.
    """
    credibility = 3600
    
    quest_reward_instantiable_credibility = QuestRewardInstantiableCredibility(
        credibility,
    )
    
    output = repr(quest_reward_instantiable_credibility)
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
def test__QuestRewardInstantiableCredibility__eq(position_parameters_0, position_parameters_1):
    """
    Tests whether ``QuestRewardInstantiableCredibility.__eq__`` works as intended.
    
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
    quest_reward_instantiable_credibility_0 = QuestRewardInstantiableCredibility(*position_parameters_0)
    quest_reward_instantiable_credibility_1 = QuestRewardInstantiableCredibility(*position_parameters_1)
    
    output = quest_reward_instantiable_credibility_0 == quest_reward_instantiable_credibility_1
    vampytest.assert_instance(output, bool)
    return output


def test__QuestRewardInstantiableCredibility__instantiate():
    """
    Tests whether ``QuestRewardInstantiableCredibility.instantiate`` works as intended.
    """
    credibility = 3600
    
    quest_reward_instantiable_credibility = QuestRewardInstantiableCredibility(
        credibility,
    )
    
    output = quest_reward_instantiable_credibility.instantiate()
    
    vampytest.assert_instance(output, QuestRewardSerialisableCredibility)
    vampytest.assert_eq(output.credibility, credibility)
