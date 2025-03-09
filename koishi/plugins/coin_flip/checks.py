__all__ = ()

from hata.ext.slash import abort

from .constants import BET_MIN
from .embed_builders import build_failure_embed_insufficient_available_balance, build_failure_embed_insufficient_bet


def check_sufficient_bet(bet_amount):
    """
    Checks whether the bet is sufficient.
    
    Parameters
    ----------
    bet_amount : `int`
        The amount the user bet.
    
    Raises
    ------
    InteractionAbortedError
    """
    if bet_amount >= BET_MIN:
        return
    
    abort(
        embed = build_failure_embed_insufficient_bet(),
    )


def check_sufficient_available_balance(available_balance, bet_amount):
    """
    Checks whether the bet is sufficient.
    
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
    if available_balance >= bet_amount:
        return
    
    abort(
        embed = build_failure_embed_insufficient_available_balance(available_balance, bet_amount),
    )
