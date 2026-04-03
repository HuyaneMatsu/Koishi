__all__ = ('calculate_daily_for', 'calculate_daily_new', 'calculate_vote_for', 'refresh_streak')

from .constants import DAILY_STREAK_BREAK, DAILY_STREAK_LOSE
from .reward_accumulator import RewardAccumulator
from .rewards import REWARDS_DAILY, REWARDS_VOTE


def calculate_daily_for(user, streak):
    """
    Returns how much daily love the given user gets after the given streak.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The respective user.
    
    streak : `int`
        The streak of the respective user.
    
    Returns
    -------
    received : `int`
    """
    accumulator = RewardAccumulator()
    accumulator.add_rewards(REWARDS_DAILY, user)
    return accumulator.sum_rewards(streak)


def calculate_vote_for(user, streak):
    """
    Returns how much love the given user gets after the given streak after a vote.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The respective user.
    
    streak : `int`
        The streak of the respective user.
    
    Returns
    -------
    received : `int`
    """
    accumulator = RewardAccumulator()
    accumulator.add_rewards(REWARDS_VOTE, user)
    return accumulator.sum_rewards(streak)


def refresh_streak(streak, daily_can_claim_at, now):
    """
    Calculates daily streak loss.
    
    Parameters
    ----------
    streak : `int`
        The user's actual daily streak.
    
    daily_can_claim_at : `DateTime`
        The time when the user can claim it's next daily reward.
    
    now : `DateTime`
        The current utc time.
    
    Returns
    -------
    streak_new : `int`
        The new daily streak value of the user.
    """
    daily_can_claim_at_with_break = daily_can_claim_at + DAILY_STREAK_BREAK
    if daily_can_claim_at_with_break < now:
        streak_new = streak - ((now - daily_can_claim_at_with_break) // DAILY_STREAK_LOSE) - 1
        
        if streak_new < 0:
            streak_new = 0
    
    else:
        streak_new = streak
    
    return streak_new


def calculate_daily_new(streak, daily_can_claim_at, now):
    """
    Calculates daily streak loss and the new next claim time.
    
    Parameters
    ----------
    streak : `int`
        The user's actual daily streak.
    
    daily_can_claim_at : `DateTime`
        The time when the user can claim it's next daily reward.
    
    now : `DateTime`
        The current utc time.
    
    Returns
    -------
    streak_new : `int`
        The new daily streak value of the user.
    
    daily_can_claim_at_new : `DateTime`
        The new daily next value of the user.
    """
    daily_can_claim_at_with_break = daily_can_claim_at + DAILY_STREAK_BREAK
    if daily_can_claim_at_with_break >= now:
        streak_new = streak
        daily_can_claim_at_new = daily_can_claim_at
    
    else:
        streak_new = streak - ((now - daily_can_claim_at_with_break) // DAILY_STREAK_LOSE) - 1
        if streak_new <= 0:
            streak_new = 0
            daily_can_claim_at_new = now
        
        else:
            daily_can_claim_at_new = daily_can_claim_at + (DAILY_STREAK_LOSE * (streak - streak_new))
    
    return streak_new, daily_can_claim_at_new
