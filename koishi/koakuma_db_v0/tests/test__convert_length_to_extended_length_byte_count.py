import vampytest

from ..helpers import convert_length_to_extended_length_byte_count


def _iter_options():
    yield 0, 0
    yield 1, 1
    yield 63, 1
    yield 64, 1
    yield 255, 1
    yield 256, 2


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__convert_length_to_extended_length_byte_count(length):
    """
    Tests whether ``convert_length_to_extended_length_byte_count`` works as intended.
    
    Parameters
    ----------
    length : `int`
        The length to convert.
    
    Returns
    -------
    output : `int`
    """
    output = convert_length_to_extended_length_byte_count(length)
    vampytest.assert_instance(output, int)
    return output
