import vampytest

from ..helpers import get_root


def _iter_options():
    yield 16, 4
    yield -16, -4


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_root(value):
    """
    Tests whether ``get_root`` works as intended. 
    
    Parameters
    ----------
    value : `int`
        The value to root up.
    
    Returns
    -------
    output : `int`
    """
    output = get_root(value)
    vampytest.assert_instance(output, int)
    return output
