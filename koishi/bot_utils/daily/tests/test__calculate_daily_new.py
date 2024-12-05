from datetime import datetime as DateTime, timedelta as TimeDelta, timezone as TimeZone

import vampytest

from ..constants import DAILY_STREAK_BREAK, DAILY_STREAK_LOSE
from ..utils import calculate_daily_new


def _iter_options():
    yield (
        56,
        DateTime(2016, 5, 14, 0, 0, 0, tzinfo = TimeZone.utc),
        DateTime(2016, 5, 14, 0, 0, 0, tzinfo = TimeZone.utc),
        (
            56,
            DateTime(2016, 5, 14, 0, 0, 0, tzinfo = TimeZone.utc),
        ),
    )
    
    yield (
        56,
        DateTime(2016, 5, 14, 0, 0, 0, tzinfo = TimeZone.utc),
        DateTime(2016, 5, 14, 0, 0, 0, tzinfo = TimeZone.utc) + DAILY_STREAK_BREAK + TimeDelta(seconds = 1),
        (
            55,
            DateTime(2016, 5, 14, 0, 0, 0, tzinfo = TimeZone.utc) + DAILY_STREAK_LOSE,
        ),
    )
    
    yield (
        56,
        DateTime(2016, 5, 14, 0, 0, 0, tzinfo = TimeZone.utc),
        DateTime(2016, 5, 14, 0, 0, 0, tzinfo = TimeZone.utc) + DAILY_STREAK_BREAK + DAILY_STREAK_LOSE * 20,
        (
            35,
            DateTime(2016, 5, 14, 0, 0, 0, tzinfo = TimeZone.utc) + DAILY_STREAK_LOSE * 21,
        ),
    )
    
    yield (
        56,
        DateTime(2016, 5, 14, 0, 0, 0, tzinfo = TimeZone.utc),
        DateTime(2016, 5, 14, 0, 0, 0, tzinfo = TimeZone.utc) + DAILY_STREAK_BREAK + DAILY_STREAK_LOSE * 100,
        (
            0,
            DateTime(2016, 5, 14, 0, 0, 0, tzinfo = TimeZone.utc) + DAILY_STREAK_BREAK + DAILY_STREAK_LOSE * 100,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__calculate_daily_new(daily_streak, daily_next, now):
    """
    Tests whether ``calculate_daily_new`` works as intended.
    
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
    output : `(int, DateTime)`
    """
    output = calculate_daily_new(daily_streak, daily_next, now)
    vampytest.assert_instance(output, tuple)
    vampytest.assert_instance(output[0], int)
    vampytest.assert_instance(output[1], DateTime)
    return output
