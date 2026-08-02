import vampytest

from ..helpers import get_integer_length


def _iter_options__get_integer_length():
    yield 0, 1
    yield 1, 1
    yield 9, 1
    yield 10, 2
    yield 11, 2
    yield 99, 2
    yield 100, 3


@vampytest._(vampytest.call_from(_iter_options__get_integer_length()).returning_last())
def test__get_integer_length(input_value):
    """
    Tests whether ``get_integer_length`` works as intended
    
    Parameters
    ----------
    input_value : `int`
        Value to get its length of.
    
    Returns
    -------
    output : `int`
    """
    return get_integer_length(input_value)
