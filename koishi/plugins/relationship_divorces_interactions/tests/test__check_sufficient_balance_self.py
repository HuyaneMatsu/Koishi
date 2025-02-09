import vampytest
from hata.ext.slash import InteractionAbortedError

from ..checks import check_sufficient_balance_self


def _iter_options__passing():
    yield 1000, 1000, 2
    yield 1000, 1001, 2


def _iter_options__failing():
    yield 1000, 999, 2


@vampytest._(vampytest.call_from(_iter_options__passing()))
@vampytest._(vampytest.call_from(_iter_options__failing()).raising(InteractionAbortedError))
def test__check_sufficient_balance_self(required_balance, available_balance, new_relationship_slot_count):
    """
    Tests whether ``check_sufficient_balance_self`` works as intended.
    
    Parameters
    ----------
    required_balance : `int`
        The required balance to buy the relationship slot.
    
    available_balance : `int`
        The available balance of the user.
    
    new_relationship_slot_count : `int`
        The new relationship slot count.
    
    Raises
    ------
    InteractionAbortedError
    """
    check_sufficient_balance_self(required_balance, available_balance, new_relationship_slot_count)
