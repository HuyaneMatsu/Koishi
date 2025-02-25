import vampytest
from hata.ext.slash import InteractionAbortedError

from ..checks import check_is_amount_valid


def _iter_options__passing():
    yield 1


def _iter_options__failing():
    yield 0
    yield -1


@vampytest._(vampytest.call_from(_iter_options__passing()))
@vampytest._(vampytest.call_from(_iter_options__failing()).raising(InteractionAbortedError))
def test__check_is_amount_valid(amount):
    """
    Tests whether ``check_is_amount_valid`` works as intended.
    
    Parameters
    ----------
    amount : `int`
        The amount to check.
    
    Raises
    ------
    InteractionAbortedError
    """
    check_is_amount_valid(amount)
