__all__ = (
    'BOOST_INTERVAL', 'DAILY_INTERVAL', 'DAILY_REMINDER_AFTER', 'DAILY_STREAK_BREAK', 'DAILY_STREAK_LOSE',
    'TOP_GG_VOTE_DELAY_MAX', 'TOP_GG_VOTE_DELAY_MIN', 'TOP_GG_VOTE_INTERVAL'
)

from datetime import timedelta as TimeDelta


DAILY_INTERVAL          = TimeDelta(hours = 22)
DAILY_STREAK_BREAK      = TimeDelta(hours = 26)
DAILY_STREAK_LOSE       = TimeDelta(hours = 12)
DAILY_REMINDER_AFTER    = TimeDelta(hours = 22)
TOP_GG_VOTE_INTERVAL    = TimeDelta(hours = 12)
TOP_GG_VOTE_DELAY_MIN   = TOP_GG_VOTE_INTERVAL
TOP_GG_VOTE_DELAY_MAX   = TimeDelta(days  =  4)
BOOST_INTERVAL          = TimeDelta(hours = 22)
