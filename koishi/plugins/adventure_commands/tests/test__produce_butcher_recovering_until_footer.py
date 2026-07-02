from datetime import datetime as DateTime, timedelta as TimeDelta, timezone as TimeZone

import vampytest

from ..content_building import produce_butcher_recovering_until_footer


def _iter_options():
    now = DateTime(2016, 5, 14, 3, 20, 19, tzinfo = TimeZone.utc)
    recovering_until = now + TimeDelta(seconds = 12)
    
    yield (
        now,
        recovering_until,
        (
            f'You are recovering for 12 seconds, until <t:{recovering_until.timestamp():.0f}:T>.'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_butcher_recovering_until_footer(now, recovering_until):
    """
    Tests whether ``produce_butcher_recovering_until_footer`` works as intended.
    
    Parameters
    ----------
    now : `DateTime`
        The current date time.
    
    recovering_until : `DateTime`
        Until when the user is recovering for.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_butcher_recovering_until_footer(now, recovering_until)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
