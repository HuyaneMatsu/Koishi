__all__ = ('calculate_daily_for', 'calculate_daily_new', 'calculate_vote_for', 'refresh_daily_streak')

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


def refresh_daily_streak(daily_streak, daily_next, now):
    """
    Calculates daily streak loss.
    
    Parameters
    ----------
    daily_streak : `int`
        The user's actual daily streak.
    
    daily_next : `DateTime`
        The time when the user can claim it's next daily reward.
    
    now : `DateTime`
        The current utc time.
    
    Returns
    -------
    daily_streak_new : `int`
        The new daily streak value of the user.
    """
    daily_next_with_break = daily_next + DAILY_STREAK_BREAK
    if daily_next_with_break < now:
        daily_streak_new = daily_streak - ((now - daily_next_with_break) // DAILY_STREAK_LOSE) - 1
        
        if daily_streak_new < 0:
            daily_streak_new = 0
    
    else:
        daily_streak_new = daily_streak
    
    return daily_streak_new


def calculate_daily_new(daily_streak, daily_next, now):
    """
    Calculates daily streak loss and the new next claim time.
    
    Parameters
    ----------
    daily_streak : `int`
        The user's actual daily streak.
    
    daily_next : `DateTime`
        The time when the user can claim it's next daily reward.
    
    now : `DateTime`
        The current utc time.
    
    Returns
    -------
    daily_streak_new : `int`
        The new daily streak value of the user.
    
    daily_next_new : `DateTime`
        The new daily next value of the user.
    """
    daily_next_with_break = daily_next + DAILY_STREAK_BREAK
    if daily_next_with_break >= now:
        daily_streak_new = daily_streak
        daily_next_new = daily_next
    
    else:
        daily_streak_new = daily_streak - ((now - daily_next_with_break) // DAILY_STREAK_LOSE) - 1
        if daily_streak_new <= 0:
            daily_streak_new = 0
            daily_next_new = now
        
        else:
            daily_next_new = daily_next + (DAILY_STREAK_LOSE * (daily_streak - daily_streak_new))
    
    return daily_streak_new, daily_next_new
