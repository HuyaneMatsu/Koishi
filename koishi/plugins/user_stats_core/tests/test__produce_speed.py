import vampytest

from ..utils import produce_speed


def _iter_options():
    yield 700, '0.7'
    yield 1200, '1.2'
    yield 2000, '2.0'
    yield 749, '0.7'
    yield 750, '0.8'
    yield 950, '1.0'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_speed(speed):
    """
    Tests whether ``produce_speed`` works as intended.
    
    Parameters
    ----------
    speed : `int`
        Speed in millimeters.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_speed(speed)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
