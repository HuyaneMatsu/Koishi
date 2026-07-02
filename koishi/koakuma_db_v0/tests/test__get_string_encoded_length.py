import vampytest

from ..helpers import get_string_encoded_length


def _iter_options():
    yield None, 0
    yield 'aya', 3
    yield 'yű', 3
    yield 'y\U0002ffff', 5


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_string_encoded_length(string):
    """
    Tests whether ``get_string_encoded_length`` works as intended.
    
    Parameters
    ----------
    string : `None | str`
        The string to get its encoded length of.
    
    Returns
    -------
    output : `int`
    """
    output = get_string_encoded_length(string)
    vampytest.assert_instance(output, int)
    return output
