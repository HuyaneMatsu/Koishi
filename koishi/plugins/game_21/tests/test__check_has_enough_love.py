import vampytest

from hata.ext.slash import InteractionAbortedError

from ..checks import check_has_enough_love


def _iter_options():
    yield (
        1000,
        999,
        True,
    )

    yield (
        1000,
        1000,
        False,
    )


    yield (
        1000,
        1001,
        False,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__check_has_enough_love(expected_love, available_love):
    """
    Tests whether ``check_has_enough_love`` works as intended.
    
    Parameters
    ----------
    expected_love : `int`
        The expected hearts to have.
    available_love : `int`
        The available hearts of a user.
    
    Returns
    -------
    aborted : `bool`
    """
    try:
        check_has_enough_love(expected_love, available_love)
    except InteractionAbortedError:
        return True
    
    return False
