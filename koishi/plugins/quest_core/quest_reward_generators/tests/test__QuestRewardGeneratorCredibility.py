from random import Random

import vampytest

from ...quest_reward_instantiables import QuestRewardInstantiableCredibility
from ...quest_reward_types import QUEST_REWARD_TYPE_CREDIBILITY

from ..credibility import QuestRewardGeneratorCredibility


def _assert_fields_set(quest_reward_generator_credibility):
    """
    Asserts whether the instance has all of its fields set.
    
    Parameters
    ----------
    quest_reward_generator_credibility : ``QuestRewardGeneratorCredibility``
        The instance to check.
    """
    vampytest.assert_instance(quest_reward_generator_credibility, QuestRewardGeneratorCredibility)
    vampytest.assert_eq(quest_reward_generator_credibility.TYPE, QUEST_REWARD_TYPE_CREDIBILITY)
    vampytest.assert_instance(quest_reward_generator_credibility.credibility_base, int)


def test__QuestRewardGeneratorCredibility__new():
    """
    Tests whether ``QuestRewardGeneratorCredibility.__new__`` works as intended.
    """
    credibility_base = 3600
    
    quest_reward_generator_credibility = QuestRewardGeneratorCredibility(
        credibility_base,
    )
    _assert_fields_set(quest_reward_generator_credibility)
    
    vampytest.assert_eq(quest_reward_generator_credibility.credibility_base, credibility_base)


def test__QuestRewardGeneratorCredibility__repr():
    """
    Tests whether ``QuestRewardGeneratorCredibility.__repr__`` works as intended.
    """
    credibility_base = 3600
    
    quest_reward_generator_credibility = QuestRewardGeneratorCredibility(
        credibility_base,
    )
    
    output = repr(quest_reward_generator_credibility)
    vampytest.assert_instance(output, str)


def _iter_options__eq():
    credibility_base = 3600
    
    yield (
        (
            credibility_base,
        ),
        (
            credibility_base,
        ),
        True,
    )
    
    yield (
        (
            credibility_base,
        ),
        (
            7200,
        ),
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__QuestRewardGeneratorCredibility__eq(position_parameters_0, position_parameters_1):
    """
    Tests whether ``QuestRewardGeneratorCredibility.__eq__`` works as intended.
    
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
    quest_reward_generator_credibility_0 = QuestRewardGeneratorCredibility(*position_parameters_0)
    quest_reward_generator_credibility_1 = QuestRewardGeneratorCredibility(*position_parameters_1)
    
    output = quest_reward_generator_credibility_0 == quest_reward_generator_credibility_1
    vampytest.assert_instance(output, bool)
    return output


def test__QuestRewardGeneratorCredibility__generate_with_diversion():
    """
    Tests whether ``QuestRewardGeneratorCredibility.generate_with_diversion`` works as intended.
    """
    credibility_base = 3600
    
    quest_reward_generator_credibility = QuestRewardGeneratorCredibility(
        credibility_base,
    )
    
    random_number_generator = Random(5)
    accumulated_diversion = 2.0
    
    generated, diversion = quest_reward_generator_credibility.generate_with_diversion(
        random_number_generator, accumulated_diversion
    )
    
    vampytest.assert_eq(
        generated,
        QuestRewardInstantiableCredibility(
            7200,
        ),
    )
    
    vampytest.assert_eq(
        diversion,
        1.0,
    )
