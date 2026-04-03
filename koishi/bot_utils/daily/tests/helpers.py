from ..condition import ConditionName
from ..reward import Reward


def _create_dummy_reward_0():
    """
    Creates a dummy reward.
    
    Returns
    -------
    reward : ``Reward``
    """
    reward = object.__new__(Reward)
    reward.base = 100
    reward.extra_limit = 300
    reward.extra_per_streak = 5
    reward.condition = None
    return reward


def _create_dummy_reward_1():
    """
    Creates a dummy reward with condition.
    
    Returns
    -------
    reward : ``Reward``
    """
    reward = object.__new__(Reward)
    reward.base = 0
    reward.extra_limit = 300
    reward.extra_per_streak = 0
    reward.condition = ConditionName('brain')
    return reward
