import vampytest

from ..helpers import build_suggested_time_zone


def _iter_options():
    yield 'KW/orin', 0, 'KW/orin (+00:00)'
    yield 'KW/okuu', +5.5, 'KW/okuu (+05:30)'
    yield 'KW/koishi', -1, 'KW/koishi (-01:00)'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_suggested_time_zone(time_zone_name, time_zone_offset):
    """
    Tests whether ``build_suggested_time_zone`` works as intended.
    
    Parameters
    ----------
    time_zone_name : `str`
        The time zone's name.
    
    time_zone_offset : `float`
        The time zone's offset.
    
    Returns
    -------
    output : `str`
    """
    output = build_suggested_time_zone(time_zone_name, time_zone_offset)
    vampytest.assert_instance(output, str)
    return output
