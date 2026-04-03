import vampytest

from ...quest_reward_serialisables import QuestRewardSerialisableBase
from ...quest_reward_types import QUEST_REWARD_TYPE_NONE

from ..base import QuestRewardInstantiableBase


def _assert_fields_set(quest_reward_instantiable_base):
    """
    Asserts whether the instance has all of its fields set.
    
    Parameters
    ----------
    quest_reward_instantiable_base : ``QuestRewardInstantiableBase``
        The instance to check.
    """
    vampytest.assert_instance(quest_reward_instantiable_base, QuestRewardInstantiableBase)
    vampytest.assert_eq(quest_reward_instantiable_base.TYPE, QUEST_REWARD_TYPE_NONE)


def test__QuestRewardInstantiableBase__new():
    """
    Tests whether ``QuestRewardInstantiableBase.__new__`` works as intended.
    """
    quest_reward_instantiable_base = QuestRewardInstantiableBase()
    _assert_fields_set(quest_reward_instantiable_base)


def test__QuestRewardInstantiableBase__repr():
    """
    Tests whether ``QuestRewardInstantiableBase.__repr__`` works as intended.
    """
    quest_reward_instantiable_base = QuestRewardInstantiableBase()
    
    output = repr(quest_reward_instantiable_base)
    vampytest.assert_instance(output, str)


def _iter_options__eq():
    yield (
        (),
        (),
        True,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__QuestRewardInstantiableBase__eq(position_parameters_0, position_parameters_1):
    """
    Tests whether ``QuestRewardInstantiableBase.__eq__`` works as intended.
    
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
    quest_reward_instantiable_base_0 = QuestRewardInstantiableBase(*position_parameters_0)
    quest_reward_instantiable_base_1 = QuestRewardInstantiableBase(*position_parameters_1)
    
    output = quest_reward_instantiable_base_0 == quest_reward_instantiable_base_1
    vampytest.assert_instance(output, bool)
    return output


def test__QuestRewardInstantiableBase__instantiate():
    """
    Tests whether ``QuestRewardInstantiableBase.instantiate`` works as intended.
    """
    quest_reward_instantiable_base = QuestRewardInstantiableBase()
    
    output = quest_reward_instantiable_base.instantiate()
    
    vampytest.assert_eq(
        output,
        QuestRewardSerialisableBase(),
    )
