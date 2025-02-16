__all__ = ()

from hata.ext.slash import abort

from .embed_builders import (
    build_failure_embed_has_role_other, build_failure_embed_has_role_self,
    build_failure_embed_insufficient_available_balance, build_failure_embed_not_in_guild_other,
    build_failure_embed_not_in_guild_self
)


def check_has_role_self(role, user):
    """
    Checks whether the user already has the role
    
    Parameters
    ----------
    role : ``Role``
        The role to be purchased.
    
    user : ``ClientUserBase``
        The user the who is purchasing the role.
    
    Raises
    ------
    InteractionAbortedError
    """
    if not user.has_role(role):
        return
    
    abort(
        embed = build_failure_embed_has_role_self(role),
    )


def check_has_role_other(role, user, guild_id):
    """
    Checks whether the other user already has the role.
    
    Parameters
    ----------
    role : ``Role``
        The role to be purchased.
    
    user : ``ClientUserBase``
        The user the for who the role is purchased for.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Raises
    ------
    InteractionAbortedError
    """
    if not user.has_role(role):
        return
    
    abort(
        embed = build_failure_embed_has_role_other(role, user, guild_id),
    )


def check_not_in_guild_self(role, user):
    """
    Checks whether the user is in the role's guild.
    
    Parameters
    ----------
    role : ``Role``
        The role to be purchased.
    
    user : ``ClientUserBase``
        The user the who is purchasing the role.
    
    Raises
    ------
    InteractionAbortedError
    """
    if user.get_guild_profile_for(role.guild_id) is not None:
        return
    
    abort(
        embed = build_failure_embed_not_in_guild_self(role),
    )


def check_not_in_guild_other(role, user, guild_id):
    """
    Checks whether the other user is in the role's guild.
    
    Parameters
    ----------
    role : ``Role``
        The role to be purchased.
    
    user : ``ClientUserBase``
        The user the for who the role is purchased for.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Raises
    ------
    InteractionAbortedError
    """
    if user.get_guild_profile_for(role.guild_id) is not None:
        return
    
    abort(
        embed = build_failure_embed_not_in_guild_other(role, user, guild_id),
    )


def check_insufficient_available_balance(role, available_balance, required_balance):
    """
    Checks whether the user has sufficient balance.
    
    Parameters
    ----------
    role : ``Role``
        The role to be purchased.
    
    available_balance : `int`
        Available balance.
    
    required_balance : `int`
        The required balance to buy the role.
    
    Raises
    ------
    InteractionAbortedError
    """
    if available_balance >= required_balance:
        return
    
    abort(
        embed = build_failure_embed_insufficient_available_balance(role, available_balance, required_balance),
    )
