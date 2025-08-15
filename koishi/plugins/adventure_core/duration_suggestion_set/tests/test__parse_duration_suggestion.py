import vampytest

from ..utils import parse_duration_hexadecimal


def _iter_options():
    yield '56d', 0
    yield '56d1', 0x56d1
    yield '4566', 0x4566
    yield '6d 2m', 0


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_duration_hexadecimal(duration_string):
    """
    Tests whether ``parse_duration_hexadecimal`` works as intended.
    
    Parameters
    ----------
    string : `str`
        String to parse.
    
    Returns
    -------
    output : `int`
    """
    output = parse_duration_hexadecimal(duration_string)
    vampytest.assert_instance(output, int)
    return output
