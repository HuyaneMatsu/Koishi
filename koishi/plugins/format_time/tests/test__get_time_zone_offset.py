import vampytest

from ..helpers import get_time_zone_offset


def _iter_options():
    yield 'car', 2.0
    yield 'darwin', 9.5


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_time_zone_offset(name):
    """
    Tests whether ``get_time_zone_offset`` works as intended.
    
    Parameters
    ----------
    name : `str`
        The name to get time zone offset for.
    
    Returns
    -------
    output : `float`
    """
    output = get_time_zone_offset(name)
    vampytest.assert_instance(output, float)
    return output
