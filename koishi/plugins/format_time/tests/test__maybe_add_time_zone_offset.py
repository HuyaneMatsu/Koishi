from datetime import datetime as DateTime

import vampytest

from ..helpers import maybe_add_time_zone_offset


def _iter_options():
    yield DateTime(2016, 5, 14), +0.0, DateTime(2016, 5, 14)
    yield DateTime(2016, 5, 14), +1.0, DateTime(2016, 5, 13, 23)
    yield DateTime(2016, 5, 14), -13.0, DateTime(2016, 5, 14, 13)


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__maybe_add_time_zone_offset(date_time, time_zone_offset):
    """
    Tests whether ``maybe_add_time_zone_offset`` works as intended.
    
    Parameters
    ----------
    date_time : `DateTime`
        Date time to apply time zone offset.
    
    time_zone_offset : `float`
        Time zone offset to apply.
    
    Returns
    -------
    output : `DateTime`
    """
    output = maybe_add_time_zone_offset(date_time, time_zone_offset)
    vampytest.assert_instance(output, DateTime)
    return output
