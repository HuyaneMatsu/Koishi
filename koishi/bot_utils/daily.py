from datetime import datetime, timedelta

from .constants import ROLE__SUPPORT__ELEVATED, ROLE__SUPPORT__BOOSTER, ROLE__SUPPORT__HEART_BOOST

DAILY_INTERVAL          = timedelta(hours = 22)
DAILY_STREAK_BREAK      = timedelta(hours = 26)
DAILY_STREAK_LOSE       = timedelta(hours = 12)

DAILY_BASE              = 100
DAILY_PER_DAY           = 5
DAILY_LIMIT             = 300


DAILY_LIMIT_BONUS_W_E   = 300

DAILY_PER_DAY_BONUS_W_B = 5
DAILY_LIMIT_BONUS_W_B   = 300

DAILY_BASE_BONUS_W_HE   = 514
DAILY_LIMIT_BONUS_W_HE  = 5140

NSFW_ACCESS_COST        = 666
ELEVATED_COST           = 10000
HEART_BOOST_COST        = 514000


VOTE_BASE = 100
VOTE_PER_DAY = 2

VOTE_BASE_BONUS_WEEKEND = 100
VOTE_PER_DAY_BONUS_WEEKEND = 1


TOP_GG_VOTE_DELAY_MIN = timedelta(hours = 12)
TOP_GG_VOTE_DELAY_MAX = timedelta(days = 4)


def calculate_daily_for(user, daily_streak):
    """
    Returns how much daily love the given user gets after the given streak.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The respective user.
    daily_streak : `int`
        The daily streak of the respective user.
    
    Returns
    -------
    received : `int`
    """
    daily_base = DAILY_BASE
    daily_per_day = DAILY_PER_DAY
    daily_limit = DAILY_LIMIT
    
    
    if user.has_role(ROLE__SUPPORT__ELEVATED):
        daily_limit += DAILY_LIMIT_BONUS_W_E
    
    if user.has_role(ROLE__SUPPORT__BOOSTER):
        daily_per_day += DAILY_PER_DAY_BONUS_W_B
        daily_limit += DAILY_LIMIT_BONUS_W_B
    
    if user.has_role(ROLE__SUPPORT__HEART_BOOST):
        daily_base += DAILY_BASE_BONUS_W_HE
        daily_limit += DAILY_LIMIT_BONUS_W_HE
    
    
    daily_extra = daily_streak * daily_per_day
    if (daily_extra > daily_limit):
        daily_extra = daily_limit
    
    received = daily_base + daily_extra + daily_streak
    
    return received

def calculate_daily_new_only(daily_streak, daily_next, now):
    """
    Calculates daily streak loss.
    
    Parameters
    ----------
    daily_streak : `int`
        The user's actual daily streak.
    daily_next : `datetime`
        The time when the user can claim it's next daily reward.
    now : `datetime`
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
    daily_next : `datetime`
        The time when the user can claim it's next daily reward.
    now : `datetime`
        The current utc time.
    
    Returns
    -------
    daily_streak_new : `int`
        The new daily streak value of the user.
    daily_next_new : `datetime`
        The new daily next value of the user.
    """
    daily_next_with_break = daily_next + DAILY_STREAK_BREAK
    if daily_next_with_break < now:
        daily_streak_new = daily_streak - ((now - daily_next_with_break) // DAILY_STREAK_LOSE) - 1
        
        if daily_streak_new < 0:
            daily_streak_new = 0
            daily_next_new = now
        else:
            daily_next_new = daily_next + (DAILY_STREAK_LOSE * (daily_streak - daily_streak_new))
    
    else:
        daily_streak_new = daily_streak
        daily_next_new = daily_next
    
    return daily_streak_new, daily_next_new
