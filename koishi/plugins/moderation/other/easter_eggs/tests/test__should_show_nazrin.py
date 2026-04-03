from datetime import timedelta as TimeDelta

import vampytest

from ..nazrin import should_show_nazrin


def _iter_options():
    yield TimeDelta(days = 7), False
    yield TimeDelta(days = 8), True


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__should_show_nazrin(duration):
    """
    Tests whether ``should_show_nazrin`` works as intended.
    
    Parameters
    ----------
    duration : `TimeDelta`
        Timeout duration.
    
    Returns
    -------
    output : `bool`
    """
    mocked = vampytest.mock_globals(
        should_show_nazrin,
        random = lambda : 1.0,
    )
    
    output = mocked(duration)
    vampytest.assert_instance(output, bool)
    return output
