__all__ = ()

from ...bot_utils.daily import (
    DAILY_INTERVAL, DAILY_STREAK_BREAK, TOP_GG_VOTE_DELAY_MAX, TOP_GG_VOTE_DELAY_MIN, calculate_daily_for,
    refresh_streak
)

def should_top_gg_notify(count_top_gg_vote, top_gg_voted_at, now):
    if count_top_gg_vote <= 0:
        return False
        
    vote_difference = now - top_gg_voted_at
    if vote_difference < TOP_GG_VOTE_DELAY_MIN:
        return False
    
    if vote_difference > TOP_GG_VOTE_DELAY_MAX:
        return False
    
    return False
