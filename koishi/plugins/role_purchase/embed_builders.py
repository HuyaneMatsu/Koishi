__all__ = ()

from hata import Embed

from ...bot_utils.constants import EMOJI__HEART_CURRENCY


def build_failure_embed_has_role_self(role):
    """
    Builds a failure embed for the case when the user already has the given role.
    
    Parameters
    ----------
    role : ``Role``
        The role to be purchased.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        'Suffering from success',
        f'You already have the {role.name} role.',
    )


def build_failure_embed_has_role_other(role, user, guild_id):
    """
    Builds a failure embed for the case when an other user already has the given role.
    
    Parameters
    ----------
    role : ``Role``
        The role to be purchased.
    
    user : `ClientUserBase``
        The targeted user.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        'Suffering from success',
        f'{user.name_at(guild_id)} already has the {role.name} role.',
    )


def build_failure_embed_not_in_guild_self(role):
    """
    Builds a failure embed for the case when the user is not in the guild of the role.
    
    Parameters
    ----------
    role : ``Role``
        The role to be purchased.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        'Not in guild',
        f'You must be in {role.guild.name} to acquire {role.name} role.'
    )


def build_failure_embed_not_in_guild_other(role, user, guild_id):
    """
    Builds a failure embed for the case when the other user is not in the guild of the role.
    
    Parameters
    ----------
    role : ``Role``
        The role to be purchased.
    
    user : `ClientUserBase``
        The targeted user.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        'Not in guild',
        f'{user.name_at(guild_id)} must be in {role.guild.name} to receive the {role.name} role.'
    )


def build_failure_embed_insufficient_available_balance(role, available_balance, required_balance):
    """
    Builds a failure embed for the case when the user' available balance is lower than the cost.
    
    Parameters
    ----------
    role : ``Role``
        The role to be purchased.
    
    available_balance : `int`
        Available balance.
    
    required_balance : `int`
        The required balance to buy the role.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        'Insufficient available balance',
        (
            f'You need to have at least {required_balance!s} available {EMOJI__HEART_CURRENCY} '
            f'to purchase the {role.name!s} role.'
        )
    ).add_field(
        f'Your available {EMOJI__HEART_CURRENCY}',
        (
            f'```\n'
            f'{available_balance}\n'
            f'```'
        ),
    )


def _add_embed_field_user_balance_change(embed, balance, required_balance):
    """
    Adds an embed field showing the balance change of the user.
    
    Parameters
    ----------
    embed : ``Embed``
        The embed to extend.
    
    balance : `int`
        The user's balance.
    
    required_balance : `int`
        Required balance for the role.
    
    Returns
    -------
    embed : ``Embed``
    """
    return embed.add_field(
        f'Your {EMOJI__HEART_CURRENCY}',
        (
            f'```\n'
            f'{balance} -> {balance - required_balance}\n'
            f'```'
        ),
    )


def build_success_embed_self(role, balance, required_balance):
    """
    Builds a success embed for the case when the user successfully purchased a role for themselves.
    
    Parameters
    ----------
    role : ``Role``
        The purchased role.
    
    balance : `int`
        The user's balance.
    
    required_balance : `int`
        Required balance for the role.
    
    Returns
    -------
    embed : ``Embed``
    """
    embed = Embed(
        'Successful purchase',
        f'You successfully purchased the {role.name} role.',
    )
    return _add_embed_field_user_balance_change(embed, balance, required_balance)


def build_success_embed_other(role, balance, required_balance, user, guild_id):
    """
    Builds a success embed for the case when the user successfully purchased a role for someone else.
    
    Parameters
    ----------
    role : ``Role``
        The purchased role.
    
    balance : `int`
        The user's balance.
    
    required_balance : `int`
        Required balance for the role.
    
    user : `ClientUserBase``
        The targeted user.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    embed : ``Embed``
    """
    embed = Embed(
        'Successful purchase',
        f'You successfully purchased the {role.name} role for {user.name_at(guild_id)}.',
    )
    return _add_embed_field_user_balance_change(embed, balance, required_balance)


def build_notification_embed_other(role, source_user, guild_id):
    """
    Builds a notification when a role is purchased for someone else.
    
    Parameters
    ----------
    role : ``Role``
        The purchased role.
    
    source_user : `ClientUserBase``
        The user who bought the role.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        'Love is in the air',
        f'You have been gifted the {role.name} role by {source_user.name_at(guild_id)}.',
    )
