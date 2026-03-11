from random import Random

import vampytest

from ...quest_reward_instantiables import QuestRewardInstantiableCredibility
from ...quest_reward_types import QUEST_REWARD_TYPE_CREDIBILITY

from ..credibility_fix import QuestRewardGeneratorCredibilityFix


def _assert_fields_set(quest_reward_generator_credibility_fix):
    """
    Asserts whether the instance has all of its fields set.
    
    Parameters
    ----------
    quest_reward_generator_credibility_fix : ``QuestRewardGeneratorCredibilityFix``
        The instance to check.
    """
    vampytest.assert_instance(quest_reward_generator_credibility_fix, QuestRewardGeneratorCredibilityFix)
    vampytest.assert_eq(quest_reward_generator_credibility_fix.TYPE, QUEST_REWARD_TYPE_CREDIBILITY)
    vampytest.assert_instance(quest_reward_generator_credibility_fix.credibility_base, int)


def test__QuestRewardGeneratorCredibilityFix__new():
    """
    Tests whether ``QuestRewardGeneratorCredibilityFix.__new__`` works as intended.
    """
    credibility_base = 3600
    
    quest_reward_generator_credibility_fix = QuestRewardGeneratorCredibilityFix(
        credibility_base,
    )
    _assert_fields_set(quest_reward_generator_credibility_fix)
    
    vampytest.assert_eq(quest_reward_generator_credibility_fix.credibility_base, credibility_base)


def test__QuestRewardGeneratorCredibilityFix__repr():
    """
    Tests whether ``QuestRewardGeneratorCredibilityFix.__repr__`` works as intended.
    """
    credibility_base = 3600
    
    quest_reward_generator_credibility_fix = QuestRewardGeneratorCredibilityFix(
        credibility_base,
    )
    
    output = repr(quest_reward_generator_credibility_fix)
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
def test__QuestRewardGeneratorCredibilityFix__eq(position_parameters_0, position_parameters_1):
    """
    Tests whether ``QuestRewardGeneratorCredibilityFix.__eq__`` works as intended.
    
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
    quest_reward_generator_credibility_fix_0 = QuestRewardGeneratorCredibilityFix(*position_parameters_0)
    quest_reward_generator_credibility_fix_1 = QuestRewardGeneratorCredibilityFix(*position_parameters_1)
    
    output = quest_reward_generator_credibility_fix_0 == quest_reward_generator_credibility_fix_1
    vampytest.assert_instance(output, bool)
    return output


def test__QuestRewardGeneratorCredibilityFix__generate_with_diversion():
    """
    Tests whether ``QuestRewardGeneratorCredibilityFix.generate_with_diversion`` works as intended.
    """
    credibility_base = 3600
    
    quest_reward_generator_credibility_fix = QuestRewardGeneratorCredibilityFix(
        credibility_base,
    )
    
    random_number_generator = Random(5)
    accumulated_diversion = 2.0
    
    generated, diversion = quest_reward_generator_credibility_fix.generate_with_diversion(
        random_number_generator, accumulated_diversion
    )
    
    vampytest.assert_eq(
        generated,
        QuestRewardInstantiableCredibility(
            3600,
        ),
    )
    
    vampytest.assert_eq(
        diversion,
        1.0,
    )
