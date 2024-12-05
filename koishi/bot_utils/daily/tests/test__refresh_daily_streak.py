from datetime import datetime as DateTime, timedelta as TimeDelta, timezone as TimeZone

import vampytest

from ..constants import DAILY_STREAK_BREAK, DAILY_STREAK_LOSE
from ..utils import refresh_daily_streak


def _iter_options():
    yield (
        56,
        DateTime(2016, 5, 14, 0, 0, 0, tzinfo = TimeZone.utc),
        DateTime(2016, 5, 14, 0, 0, 0, tzinfo = TimeZone.utc),
        56,
    )
    
    yield (
        56,
        DateTime(2016, 5, 14, 0, 0, 0, tzinfo = TimeZone.utc),
        DateTime(2016, 5, 14, 0, 0, 0, tzinfo = TimeZone.utc) + DAILY_STREAK_BREAK + TimeDelta(seconds = 1),
        55,
    )
    
    yield (
        56,
        DateTime(2016, 5, 14, 0, 0, 0, tzinfo = TimeZone.utc),
        DateTime(2016, 5, 14, 0, 0, 0, tzinfo = TimeZone.utc) + DAILY_STREAK_BREAK + DAILY_STREAK_LOSE * 20,
        35,
    )
    
    yield (
        56,
        DateTime(2016, 5, 14, 0, 0, 0, tzinfo = TimeZone.utc),
        DateTime(2016, 5, 14, 0, 0, 0, tzinfo = TimeZone.utc) + DAILY_STREAK_BREAK + DAILY_STREAK_LOSE * 100,
        0,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__refresh_daily_streak(daily_streak, daily_next, now):
    """
    Tests whether ``refresh_daily_streak`` works as intended.
    
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
    output : `int`
    """
    output = refresh_daily_streak(daily_streak, daily_next, now)
    vampytest.assert_instance(output, int)
    return output
