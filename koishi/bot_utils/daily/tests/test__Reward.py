import vampytest

from ..condition import ConditionBase, ConditionName
from ..reward import Reward


def _assert_fields_set(reward):
    """
    Asserts whether every fields are set of the given reward.
    
    Parameters
    ----------
    reward : ``Reward``
        The instance to check.
    """
    vampytest.assert_instance(reward, Reward)
    vampytest.assert_instance(reward.base, int)
    vampytest.assert_instance(reward.condition, ConditionBase, nullable = True)
    vampytest.assert_instance(reward.extra_limit, int)
    vampytest.assert_instance(reward.extra_per_streak, int)


def test__Reward__construction__no_fields():
    """
    Tests whether ``Reward`` construction works as intended
    
    Case: no fields given.
    """
    class reward(Reward):
        pass
    
    _assert_fields_set(reward)


def test__Reward__construction__all_fields():
    """
    Tests whether ``Reward`` construction works as intended
    
    Case: all fields given.
    """
    value_base = 300
    value_extra_limit = 100
    value_extra_per_streak = 50
    value_condition = ConditionName('brain')
        
    class reward(Reward):
        base = value_base
        extra_limit = value_extra_limit
        extra_per_streak = value_extra_per_streak
        condition = value_condition
    
    _assert_fields_set(reward)
    
    vampytest.assert_eq(reward.base, value_base)
    vampytest.assert_eq(reward.extra_limit, value_extra_limit)
    vampytest.assert_eq(reward.extra_per_streak, value_extra_per_streak)
    vampytest.assert_eq(reward.condition, value_condition)


def test__Reward__repr():
    """
    Tests whether ``Reward.__repr__`` works as intended
    """
    value_base = 300
    value_extra_limit = 100
    value_extra_per_streak = 50
    value_condition = ConditionName('brain')
        
    class reward(Reward):
        base = value_base
        extra_limit = value_extra_limit
        extra_per_streak = value_extra_per_streak
        condition = value_condition
    
    output = repr(reward)
    vampytest.assert_instance(output, str)
