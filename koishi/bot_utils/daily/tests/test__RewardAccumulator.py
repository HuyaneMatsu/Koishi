import vampytest
from hata import User

from ..reward_accumulator import RewardAccumulator

from .helpers import _create_dummy_reward_0, _create_dummy_reward_1


def _assert_fields_set(reward_accumulator):
    """
    Asserts whether every fields are set of the given reward accumulator.
    
    Parameters
    ----------
    reward_accumulator : ``RewardAccumulator``
        The instance to check.
    """
    vampytest.assert_instance(reward_accumulator, RewardAccumulator)
    vampytest.assert_instance(reward_accumulator.base, int)
    vampytest.assert_instance(reward_accumulator.extra_limit, int)
    vampytest.assert_instance(reward_accumulator.extra_per_streak, int)


def test__RewardAccumulator__new():
    """
    Tests whether ``RewardAccumulator.__new__`` works as intended.
    """
    reward_accumulator = RewardAccumulator()
    _assert_fields_set(reward_accumulator)


def test__RewardAccumulator__repr():
    """
    Tests whether ``RewardAccumulator.__repr__`` works as intended.
    """
    reward_accumulator = RewardAccumulator()
    output = repr(reward_accumulator)
    vampytest.assert_instance(output, str)


def test__RewardAccumulator__add_rewards():
    """
    Tests whether ``RewardAccumulator.add_rewards`` works as intended.
    """
    reward_0 = _create_dummy_reward_0()
    reward_1 = _create_dummy_reward_1()
    
    user = User.precreate(202412010000, name = 'brain')
    
    reward_accumulator = RewardAccumulator()
    reward_accumulator.add_rewards((reward_0, reward_1), user)
    
    vampytest.assert_eq(reward_accumulator.base, reward_0.base + reward_1.base)
    vampytest.assert_eq(reward_accumulator.extra_limit, reward_0.extra_limit + reward_1.extra_limit)
    vampytest.assert_eq(reward_accumulator.extra_per_streak, reward_0.extra_per_streak + reward_1.extra_per_streak)


def test__RewardAccumulator__add_reward__no_condition():
    """
    Tests whether ``RewardAccumulator.add_reward`` works as intended.
    
    Case: no condition.
    """
    reward = _create_dummy_reward_0()
    user = User.precreate(202412010001, name = 'brain')
    
    reward_accumulator = RewardAccumulator()
    output = reward_accumulator.add_reward(reward, user)
    
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)
    
    vampytest.assert_eq(reward_accumulator.base, reward.base)
    vampytest.assert_eq(reward_accumulator.extra_limit, reward.extra_limit)
    vampytest.assert_eq(reward_accumulator.extra_per_streak, reward.extra_per_streak)


def test__RewardAccumulator__add_reward__condition_pass():
    """
    Tests whether ``RewardAccumulator.add_reward`` works as intended.
    
    Case: condition pass.
    """
    reward = _create_dummy_reward_1()
    user = User.precreate(202412010002, name = 'brain')
    
    reward_accumulator = RewardAccumulator()
    output = reward_accumulator.add_reward(reward, user)
    
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)
    
    vampytest.assert_eq(reward_accumulator.base, reward.base)
    vampytest.assert_eq(reward_accumulator.extra_limit, reward.extra_limit)
    vampytest.assert_eq(reward_accumulator.extra_per_streak, reward.extra_per_streak)


def test__RewardAccumulator__add_reward__condition_fail():
    """
    Tests whether ``RewardAccumulator.add_reward`` works as intended.
    
    Case: condition fail.
    """
    reward = _create_dummy_reward_1()
    user = User.precreate(202412010003, name = 'love')
    
    reward_accumulator = RewardAccumulator()
    output = reward_accumulator.add_reward(reward, user)
    
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)
    
    vampytest.assert_eq(reward_accumulator.base, 0)
    vampytest.assert_eq(reward_accumulator.extra_limit, 0)
    vampytest.assert_eq(reward_accumulator.extra_per_streak, 0)


def test__RewardAccumulator__sum_rewards__under_limit():
    """
    Tests whether ``RewardAccumulator.sun_rewards`` works as intended.
    
    Case: under limit.
    """
    reward_accumulator = RewardAccumulator()
    
    reward_accumulator.base = 120
    reward_accumulator.extra_limit = 300
    reward_accumulator.extra_per_streak = 10
    
    output = reward_accumulator.sum_rewards(20)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 340)


def test__RewardAccumulator__sum_rewards__over_limit():
    """
    Tests whether ``RewardAccumulator.sun_rewards`` works as intended.
    
    Case: over limit.
    """
    reward_accumulator = RewardAccumulator()
    
    reward_accumulator.base = 120
    reward_accumulator.extra_limit = 300
    reward_accumulator.extra_per_streak = 10
    
    output = reward_accumulator.sum_rewards(200)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 620)
