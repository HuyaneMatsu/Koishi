import vampytest

from hata.ext.slash import InteractionAbortedError

from ..checks import check_has_enough_balance


def _iter_options():
    yield (
        1000,
        999,
        False,
        True,
    )

    yield (
        1000,
        1000,
        False,
        False,
    )


    yield (
        1000,
        1001,
        False,
        False,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__check_has_enough_balance(expected, available, me):
    """
    Tests whether ``check_has_enough_balance`` works as intended.
    
    Parameters
    ----------
    expected : `int`
        The expected hearts to have.
    
    available : `int`
        The available hearts of a user.
    
    me : `bool`
        Whether the client is checking itself.
    
    Returns
    -------
    aborted : `bool`
    """
    try:
        check_has_enough_balance(expected, available, me)
    except InteractionAbortedError:
        return True
    
    return False
