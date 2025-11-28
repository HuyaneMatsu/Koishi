from datetime import timedelta as TimeDelta

import vampytest

from ..helpers import convert_time_delta


def _iter_options():
    yield (
        TimeDelta(),
        '0 seconds',
    )
    
    yield (
        TimeDelta(days = 3),
        '3 days',
    )
    
    yield (
        TimeDelta(hours = 3),
        '3 hours',
    )
    
    yield (
        TimeDelta(minutes = 3),
        '3 minutes',
    )
    
    yield (
        TimeDelta(seconds = 3),
        '3 seconds',
    )
    
    yield (
        TimeDelta(days = 3, hours = 4, minutes = 4, seconds = 5),
        '3 days, 4 hours, 4 minutes, 5 seconds',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__convert_time_delta(time_delta):
    """
    Tests whether ``convert_time_delta`` works as intended.
    
    Parameters
    ----------
    time_delta : ``TimeDelta``
        The time delta to convert.
    
    Returns
    -------
    output : `str`
    """
    output = convert_time_delta(time_delta)
    vampytest.assert_instance(output, str)
    return output
