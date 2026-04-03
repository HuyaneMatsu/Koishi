from datetime import datetime as DateTime, timedelta as TimeDelta, timezone as TimeZone

import vampytest

from ....bot_utils.daily import TOP_GG_VOTE_DELAY_MAX, TOP_GG_VOTE_DELAY_MIN

from ..helpers import should_top_gg_notify


def _iter_options():
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    yield (
        0,
        now,
        now + TOP_GG_VOTE_DELAY_MIN,
        False,
    )
    
    yield (
        1,
        now,
        now + TOP_GG_VOTE_DELAY_MIN - TimeDelta(seconds = 1),
        False,
    )
    
    yield (
        1,
        now,
        now + TOP_GG_VOTE_DELAY_MAX + TimeDelta(seconds = 1),
        False,
    )
    
    yield (
        1,
        now,
        now + TOP_GG_VOTE_DELAY_MIN,
        True,
    )
    
    yield (
        1,
        now,
        now + TOP_GG_VOTE_DELAY_MIN,
        True,
    )
    
    yield (
        1,
        now,
        now + TOP_GG_VOTE_DELAY_MAX,
        True,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__should_top_gg_notify(count_top_gg_vote, top_gg_voted_at, now):
    """
    Tests whether ``should_top_gg_notify`` works as intended.
    
    Parameters
    ----------
    count_top_gg_vote : `int`
        The amount of times the user voted on top.gg.
    
    top_gg_voted_at : `DateTime`
        When the user voted last time.
    
    now : `DateTime`
        Current time.
    
    Returns
    -------
    output : `bool`
    """
    output = should_top_gg_notify(count_top_gg_vote, top_gg_voted_at, now)
    vampytest.assert_instance(output, bool)
    return output
