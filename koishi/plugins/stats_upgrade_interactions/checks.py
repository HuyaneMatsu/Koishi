__all__ = ()

from hata.ext.slash import abort

from .embed_builders import (
    build_failure_embed_insufficient_available_balance_other, build_failure_embed_insufficient_available_balance_self
)


def check_sufficient_available_balance_self(
    required_balance, available_balance, stat_index, stat_value_after
):
    """
    Checks whether the user has insufficient amount of available balance for a purchase for themselves.
    
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
    if available_balance >= required_balance:
        return
    
    abort(
        embed = build_failure_embed_insufficient_available_balance_self(
            available_balance, required_balance, stat_index, stat_value_after
        ),
    )


def check_sufficient_available_balance_other(
    required_balance, available_balance, stat_index, stat_value_after, user, guild_id
):
    """
    Checks whether the user has insufficient amount of available balance for a purchase for someone else.
    
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
    
    user : ``ClientUserBase``
        The targeted user.
    
    guild_id : `int`
        The current guild's identifier.
    
    Raises
    ------
    InteractionAbortedError
    """
    if available_balance >= required_balance:
        return
    
    abort(
        embed = build_failure_embed_insufficient_available_balance_other(
            available_balance, required_balance, stat_index, stat_value_after, user, guild_id
        ),
    )
