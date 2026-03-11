import vampytest

from ..content_building import produce_meter_per_second


def _iter_options():
    yield 700, '0.7 m/s'
    yield 1200, '1.2 m/s'
    yield 2000, '2.0 m/s'
    yield 749, '0.7 m/s'
    yield 750, '0.8 m/s'
    yield 950, '1.0 m/s'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_meter_per_second(speed):
    """
    Tests whether ``produce_meter_per_second`` works as intended.
    
    Parameters
    ----------
    speed : `int`
        Speed in millimeters.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_meter_per_second(speed)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
