import vampytest

from hata.ext.slash import InteractionAbortedError

from ..checks import check_bet_too_low
from ..constants import BET_MIN


def _iter_options():
    yield (
        BET_MIN - 1,
        True,
    )

    yield (
        BET_MIN,
        False,
    )


    yield (
        BET_MIN + 1,
        False,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__check_bet_too_low(amount):
    """
    Tests whether ``check_bet_too_low`` works as intended.
    
    Parameters
    ----------
    amount : `int`
        Bet amount.
    
    Returns
    -------
    aborted : `bool`
    """
    try:
        check_bet_too_low(amount)
    except InteractionAbortedError:
        return True
    
    return False
