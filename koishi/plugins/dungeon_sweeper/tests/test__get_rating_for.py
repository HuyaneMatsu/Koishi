import vampytest

from ..helpers import get_rating_for


def _iter_options():
    yield 40, 33, 'S'
    yield 40, 40, 'S'
    yield 40, 47, 'A'
    yield 40, 54, 'B'
    yield 40, 61, 'C'
    yield 40, 68, 'D'
    yield 40, 75, 'E'
    yield 40, 82, 'E'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_rating_for(best, steps):
    """
    Tests whether ``get_rating_for`` works as intended.
    
    Parameters
    ----------
    best : `int`
        The minimal amount of steps required to defeat the stage.
    
    steps : `int`
        The user's step count.
    
    Returns
    -------
    output : `str`
    """
    output = get_rating_for(best, steps)
    vampytest.assert_instance(output, str)
    return output
