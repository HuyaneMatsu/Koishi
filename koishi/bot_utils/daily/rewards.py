__all__ = ('REWARDS_DAILY', 'REWARDS_VOTE',)

from ..constants import ROLE__SUPPORT__ELEVATED, ROLE__SUPPORT__BOOSTER, ROLE__SUPPORT__HEART_BOOST

from .condition import ConditionRole, ConditionWeekend
from .reward import Reward


class daily_base(Reward):
    base = 100
    extra_per_streak = 5
    extra_limit = 300


class daily_bonus_with_elevated(Reward):
    extra_limit = 300
    condition = ConditionRole(ROLE__SUPPORT__ELEVATED)


class daily_bonus_with_booster(Reward):
    base = 100
    extra_per_streak = 5
    extra_limit = 300
    condition = ConditionRole(ROLE__SUPPORT__BOOSTER)


class daily_bonus_with_heart_boost(Reward):
    base = 100
    extra_limit = 900
    condition = ConditionRole(ROLE__SUPPORT__HEART_BOOST)


class vote_base(Reward):
    base = 100
    extra_per_streak = 5
    extra_limit = 300


class vote_bonus_with_elevated(Reward):
    extra_limit = 150
    condition = ConditionRole(ROLE__SUPPORT__ELEVATED)


class vote_bonus_with_booster(Reward):
    base = 100
    extra_per_streak = 5
    extra_limit = 300
    condition = ConditionRole(ROLE__SUPPORT__BOOSTER)


class vote_bonus_with_heart_boost(Reward):
    base = 50
    extra_limit = 450
    condition = ConditionRole(ROLE__SUPPORT__HEART_BOOST)


class vote_bonus_with_weekend(Reward):
    base = 100
    extra_per_streak = 5
    extra_limit = 300
    condition = ConditionWeekend()


REWARDS_DAILY = (
    daily_base,
    daily_bonus_with_elevated,
    daily_bonus_with_booster,
    daily_bonus_with_heart_boost,
)

REWARDS_VOTE = (
    vote_base,
    vote_bonus_with_elevated,
    vote_bonus_with_booster,
    vote_bonus_with_heart_boost,
    vote_bonus_with_weekend,
)
