from random import Random

import vampytest

from ...quest_reward_instantiables import QuestRewardInstantiableBase
from ...quest_reward_types import QUEST_REWARD_TYPE_NONE

from ..base import QuestRewardGeneratorBase


def _assert_fields_set(quest_reward_generator_base):
    """
    Asserts whether the instance has all of its fields set.
    
    Parameters
    ----------
    quest_reward_generator_base : ``QuestRewardGeneratorBase``
        The instance to check.
    """
    vampytest.assert_instance(quest_reward_generator_base, QuestRewardGeneratorBase)
    vampytest.assert_eq(quest_reward_generator_base.TYPE, QUEST_REWARD_TYPE_NONE)


def test__QuestRewardGeneratorBase__new():
    """
    Tests whether ``QuestRewardGeneratorBase.__new__`` works as intended.
    """
    quest_reward_generator_base = QuestRewardGeneratorBase()
    _assert_fields_set(quest_reward_generator_base)


def test__QuestRewardGeneratorBase__repr():
    """
    Tests whether ``QuestRewardGeneratorBase.__repr__`` works as intended.
    """
    quest_reward_generator_base = QuestRewardGeneratorBase()
    
    output = repr(quest_reward_generator_base)
    vampytest.assert_instance(output, str)


def _iter_options__eq():
    yield (
        (),
        (),
        True,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__QuestRewardGeneratorBase__eq(position_parameters_0, position_parameters_1):
    """
    Tests whether ``QuestRewardGeneratorBase.__eq__`` works as intended.
    
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
    quest_reward_generator_base_0 = QuestRewardGeneratorBase(*position_parameters_0)
    quest_reward_generator_base_1 = QuestRewardGeneratorBase(*position_parameters_1)
    
    output = quest_reward_generator_base_0 == quest_reward_generator_base_1
    vampytest.assert_instance(output, bool)
    return output


def test__QuestRewardGeneratorBase__generate_with_diversion():
    """
    Tests whether ``QuestRewardGeneratorBase.generate_with_diversion`` works as intended.
    """
    quest_reward_generator_base = QuestRewardGeneratorBase()
    
    random_number_generator = Random(5)
    accumulated_diversion = 2.0
    
    generated, diversion = quest_reward_generator_base.generate_with_diversion(
        random_number_generator, accumulated_diversion
    )
    
    vampytest.assert_eq(
        generated,
        QuestRewardInstantiableBase(),
    )
    
    vampytest.assert_eq(
        diversion,
        1.0,
    )
