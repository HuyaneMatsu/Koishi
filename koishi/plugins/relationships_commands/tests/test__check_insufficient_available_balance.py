import vampytest
from hata.ext.slash import InteractionAbortedError

from ..checks import check_insufficient_available_balance


def _iter_options__passing():
    yield 200, 199
    yield 200, 200


def _iter_options__failing():
    yield 200, 201


@vampytest._(vampytest.call_from(_iter_options__passing()))
@vampytest._(vampytest.call_from(_iter_options__failing()).raising(InteractionAbortedError))
def test__check_insufficient_available_balance(available_balance, investment):
    """
    Tests whether ``check_insufficient_available_balance`` works as intended.
    
    Parameters
    ----------
    available_balance : `int`
        The user' available balance.
    
    investment : `int`
        Investment to propose with.
    
    Raises
    ------
    InteractionAbortedError
    """
    check_insufficient_available_balance(available_balance, investment)
