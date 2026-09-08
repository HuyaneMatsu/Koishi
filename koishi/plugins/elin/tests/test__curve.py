import vampytest

from ..calculate_piety_bonuses import curve


def _iter_options():
    yield 10, 20, 10, 75, 10
    yield 20, 20, 10, 75, 20
    yield 30, 20, 10, 75, 27
    yield 40, 20, 10, 75, 33
    yield 50, 20, 10, 75, 39
    yield 60, 20, 10, 75, 43
    yield 70, 20, 10, 75, 47


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__curve(value, start, step, rate):
    """
    Tests whether ``curve`` works as intended.
    
    Parameters
    ----------
    value : `int`
        The value to curve.
    
    start : `int`
        Where curving starts.
    
    step : `int`
        Step between each curving level.
    
    rate : `int`
        Rate of curving.
    
    Returns
    -------
    value : `int`
    """
    output = curve(value, start, step, rate)
    vampytest.assert_instance(output, int)
    return output
