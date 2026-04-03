import vampytest

from ..parsers_description import limit_string_length


def _iter_options():
    yield None, 20, None
    yield 'ayaya', 20, 'ayaya'
    yield 'a' * 20, 20, 'a' * 20
    yield 'ayayaya', 6, 'ay ...'
    yield 'a' * 25, 20, 'a' * 16 + ' ...'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__limit_string_length(string, max_length):
    """
    Tests whether ``limit_string_length`` works as intended.
    
    Parameters
    ----------
    string : `None`, `str`
        String to limit.
    max_length : `int`
        The maximal allowed length.
    
    Returns
    -------
    output : `None`, `str`
    """
    return limit_string_length(string, max_length)
