import vampytest
from hata.ext.slash import InteractionAbortedError

from ..checks import check_sufficient_available_balance


def _iter_options__passing():
    yield 10, 10
    yield 11, 10


def _iter_options__failing():
    yield 9, 10


@vampytest._(vampytest.call_from(_iter_options__passing()))
@vampytest._(vampytest.call_from(_iter_options__failing()).raising(InteractionAbortedError))
def test__check_sufficient_available_balance(available_balance, bet_amount):
    """
    Tests whether ``check_sufficient_available_balance`` works as intended.
    
    Parameters
    ----------
    available_balance : `int`
        The available balance of the user.
    
    bet_amount : `int`
        The amount the user bet.
    
    Raises
    ------
    InteractionAbortedError
    """
    check_sufficient_available_balance(available_balance, bet_amount)
