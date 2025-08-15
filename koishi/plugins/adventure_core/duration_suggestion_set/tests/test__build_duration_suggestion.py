import vampytest

from ..utils import build_duration_suggestion


def _iter_options():
    second = 1
    minute = second * 60
    hour = minute * 60
    day = hour * 24
    
    yield 0, '0s'
    yield 59 * second, '59s'
    yield 1 * minute, '1m'
    yield 1 * minute + 1 * second, '1m 1s'
    yield 1 * day + 1 * hour + 1 * minute + 1 * second, '1d 1h 1m 1s'
    yield 1 * day + 1 * minute, '1d 1m'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_duration_suggestion(duration):
    """
    Tests whether ``build_duration__suggestion`` works as intended.

    Parameters
    ----------
    duration : `int`
        Duration to build suggestion for.

    Returns
    -------
    output : `str`
    """
    output = build_duration_suggestion(duration)
    vampytest.assert_instance(output, str)
    return output
