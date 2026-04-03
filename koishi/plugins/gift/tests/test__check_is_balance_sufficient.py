import vampytest
from hata.ext.slash import InteractionAbortedError

from ..checks import check_is_balance_sufficient


def _iter_options__passing():
    yield 5, 0


def _iter_options__failing():
    yield 0, 0
    yield 0, 5
    yield 5, 5


@vampytest._(vampytest.call_from(_iter_options__passing()))
@vampytest._(vampytest.call_from(_iter_options__failing()).raising(InteractionAbortedError))
def test__check_is_balance_sufficient(source_balance, source_allocated):
    """
    Tests whether ``check_is_balance_sufficient`` works as intended.
    
    Parameters
    ----------
    source_balance : `int`
        The source user's balance.
    
    source_allocated : `int`
        The source user's allocated balance.
    
    Raises
    ------
    InteractionAbortedError
    """
    check_is_balance_sufficient(source_balance, source_allocated)
