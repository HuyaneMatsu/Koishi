import vampytest
from hata.ext.slash import InteractionAbortedError

from ..checks import check_sufficient_bet
from ..constants import BET_MIN


def _iter_options__passing():
    yield BET_MIN + 1
    yield BET_MIN


def _iter_options__failing():
    yield BET_MIN - 1


@vampytest._(vampytest.call_from(_iter_options__passing()))
@vampytest._(vampytest.call_from(_iter_options__failing()).raising(InteractionAbortedError))
def test__check_sufficient_bet(bet_amount):
    """
    Tests whether ``check_sufficient_bet`` works as intended.
    
    Parameters
    ----------
    bet_amount : `int`
        The amount the user bet.
    
    Raises
    ------
    InteractionAbortedError
    """
    check_sufficient_bet(bet_amount)
