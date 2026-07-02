import vampytest

from ..helpers import get_length_encoded_byte_count


def _iter_options():
    yield 0, 1
    yield 1, 1
    yield 63, 1
    yield 64, 2
    yield 255, 2
    yield 256, 3


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_length_encoded_byte_count(length):
    """
    Tests whether ``get_length_encoded_byte_count`` works as intended.
    
    Parameters
    ----------
    length : `int`
        The length to convert.
    
    Returns
    -------
    output : `int`
    """
    output = get_length_encoded_byte_count(length)
    vampytest.assert_instance(output, int)
    return output
