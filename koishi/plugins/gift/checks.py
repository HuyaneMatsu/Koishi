__all__ = ()

from hata.ext.slash import abort

from .embed_builders import (
    build_failure_embed_invalid_amount, build_failure_embed_no_balance, build_failure_embed_no_target_user,
    build_failure_embed_self_target
)


def check_is_amount_valid(amount):
    """
    Checks whether the given amount is valid for gifting.
    
    Parameters
    ----------
    amount : `int`
        The amount to check.
    
    Raises
    ------
    InteractionAbortedError
    """
    if amount > 0:
        return
    
    abort(
        embed = build_failure_embed_invalid_amount(),
    )


def check_is_target_valid(source_user, target_user):
    """
    Checks whether the targeted user can be gifted.
    
    Parameters
    ----------
    source_user : ``ClientUserBase``
        The user who is gifting.
    
    target_user : `None | ClientUserBase`
        The targeted user if any.
    
    relationship : `None | Relationship`
        The relationship connecting the two users (can be extend).
    
    Raises
    ------
    InteractionAbortedError
    """
    while True:
        if target_user is None:
            embed = build_failure_embed_no_target_user()
            break
        
        if source_user is target_user:
            embed = build_failure_embed_self_target()
            break
        
        return
    
    abort(embed = embed)


def check_is_balance_sufficient(source_balance, source_allocated):
    """
    Checks whether the balance is sufficient to gift anything.
    
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
    if source_balance - source_allocated > 0:
        return
    
    abort(
        embed = build_failure_embed_no_balance(source_balance > 0),
    )
