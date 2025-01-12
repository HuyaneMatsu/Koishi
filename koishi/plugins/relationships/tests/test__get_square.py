import vampytest

from ..helpers import get_square


def _iter_options():
    yield 4, 16
    yield -4, -16


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_square(value):
    """
    Tests whether ``get_square`` works as intended. 
    
    Parameters
    ----------
    value : `int`
        The value to square up.
    
    Returns
    -------
    output : `int`
    """
    output = get_square(value)
    vampytest.assert_instance(output, int)
    return output
