import vampytest

from ..calculate_piety_bonuses import clamp


def _iter_options():
    yield 199, 200, 1000, 200
    yield 200, 200, 1000, 200
    yield 201, 200, 1000, 201
    yield 999, 200, 1000, 999
    yield 1000, 200, 1000, 1000
    yield 1001, 200, 1000, 1000


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__clamp(value, threshold_lower, threshold_upper):
    """
    Tests whether ``clamp`` works as intended.
    
    Parameters
    ----------
    value : `int`
        Value to clamp.
    
    threshold_lower : `int`
        The lower threshold to clamp to.
    
    threshold_upper : `int`
        The upper threshold to clamp to.
    
    Returns
    -------
    output : `int`
    """
    output = clamp(value, threshold_lower, threshold_upper)
    vampytest.assert_instance(output, int)
    return output
