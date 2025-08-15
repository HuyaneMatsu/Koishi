import vampytest

from ..utils import parse_duration_suggestion


def _iter_options():
    second = 1
    minute = second * 60
    hour = minute * 60
    day = hour * 24
    
    yield '0d56', 0
    yield '0s', 0
    yield '59s', 59 * second
    yield '1m', 1 * minute
    yield '1m 1s', 1 * minute + 1 * second
    yield '1d 1h 1m 1s', 1 * day + 1 * hour + 1 * minute + 1 * second
    yield '1d 1m', 1 * day + 1 * minute


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_duration_suggestion(duration_string):
    """
    Tests whether ``parse_duration_suggestion`` works as intended.
    
    Parameters
    ----------
    string : `str`
        String to parse.
    
    Returns
    -------
    output : `int`
    """
    output = parse_duration_suggestion(duration_string)
    vampytest.assert_instance(output, int)
    return output
