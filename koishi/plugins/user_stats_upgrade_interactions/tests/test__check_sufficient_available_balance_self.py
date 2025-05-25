import vampytest
from hata.ext.slash import InteractionAbortedError

from ..checks import check_sufficient_available_balance_self


def _iter_options__passing():
    yield 1000, 1000, 2, 12
    yield 1000, 1001, 2, 12


def _iter_options__failing():
    yield 1000, 999, 2, 12


@vampytest._(vampytest.call_from(_iter_options__passing()))
@vampytest._(vampytest.call_from(_iter_options__failing()).raising(InteractionAbortedError))
def test__check_sufficient_available_balance_self(
    required_balance, available_balance, stat_index, stat_value_after
):
    """
    Tests whether ``check_sufficient_available_balance_self`` works as intended.
    
    Parameters
    ----------
    required_balance : `int`
        The required amount of balance for the purchase.
    
    available_balance : `int`
        Available balance.
    
    stat_index : `int`
        The index of the stat.
    
    stat_value_after : `int`
        The stats value after upgrade.
    
    Raises
    ------
    InteractionAbortedError
    """
    check_sufficient_available_balance_self(
        required_balance, available_balance, stat_index, stat_value_after
    )
