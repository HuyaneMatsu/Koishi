__all__ = ()

from hata.ext.slash import abort

from .embed_builders import (
    build_failure_embed_insufficient_balance_self, build_failure_embed_no_relationship_divorces_other,
    build_failure_embed_insufficient_balance_other, build_failure_embed_no_relationship_divorces_self
)


def check_no_relationship_divorces_self(relationship_divorces):
    """
    Checks whether there are no relationship divorces.
    
    Parameters
    ----------
    relationship_divorces : `int`
        The current relationship divorce count.
    
    Raises
    ------
    InteractionAbortedError
    """
    if relationship_divorces > 0:
        return
    
    abort(
        embed = build_failure_embed_no_relationship_divorces_self(),
        components = None,
    )


def check_no_relationship_divorces_other(relationship_divorces, user, guild_id):
    """
    Checks whether there are no relationship divorces.
    
    Parameters
    ----------
    relationship_divorces : `int`
        The current relationship divorce count.
    
    user : `ClientUserBase``
        The targeted user.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Raises
    ------
    InteractionAbortedError
    """
    if relationship_divorces > 0:
        return
    
    abort(
        embed = build_failure_embed_no_relationship_divorces_other(user, guild_id),
        components = None,
    )


def check_sufficient_balance_self(required_balance, available_balance, relationship_divorces):
    """
    Checks whether the user has sufficient balance.
    
    Parameters
    ----------
    required_balance : `int`
        The required balance to locate and burn the divorce papers.
    
    available_balance : `int`
        The available balance of the user.
    
    relationship_divorces : `int`
        The current relationship divorce count.
    
    Raises
    ------
    InteractionAbortedError
    """
    if available_balance >= required_balance:
        return
    
    abort(
        embed = build_failure_embed_insufficient_balance_self(required_balance, relationship_divorces),
        components = None,
    )


def check_sufficient_balance_other(required_balance, available_balance, relationship_divorces, user, guild_id):
    """
    Checks whether the user has sufficient balance.
    
    Parameters
    ----------
    required_balance : `int`
        The required balance to locate and burn the divorce papers.
    
    available_balance : `int`
        The available balance of the user.
    
    relationship_divorces : `int`
        The current relationship divorce count.
    
    user : `ClientUserBase``
        The targeted user.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Raises
    ------
    InteractionAbortedError
    """
    if available_balance >= required_balance:
        return
    
    abort(
        embed = build_failure_embed_insufficient_balance_other(
            required_balance, relationship_divorces, user, guild_id
        ),
        components = None,
    )
