from datetime import timedelta as TimeDelta

import vampytest

from ..shared_helpers_mute import build_duration_string


def _iter_options():
    yield TimeDelta(days = 28), '28 days'
    yield TimeDelta(hours = 6, seconds = 7), '6 hours, 7 seconds'
    yield TimeDelta(days = 2, hours = 3, minutes = 4, seconds = 5), '2 days, 3 hours, 4 minutes, 5 seconds' 


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__create_auto_reason(input_value):
    """
    Tests whether ``create_auto_reason`` works as intended.
    
    Parameters
    ----------
    input_value : `TimeDelta`
        Value to test with.
    
    Returns
    -------
    output : `str`
    """
    return build_duration_string(input_value)
