__all__ = ()

from ...bot_utils.constants import EMOJI__HEART_CURRENCY

from ..balance_rendering import produce_modification_description


def produce_buy_role_confirmation_description(
    role,
    required_balance,
    target_user,
    guild_id,
):
    """
    Produces buy role confirmation description.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    role : ``Role``
        The role to be purchased.
    
    required_balance : `int`
        The required balance for upgrading.
    
    target_user : ``None | ClientUserBase``
        The targeted user if any.
    
    guild_id : `int`
        The local guild's identifier.
    
    Yields
    ------
    part : `str`
    """
    yield 'Are you sure to buy '
    yield role.name
    yield ' role'
    
    if (target_user is not None):
        yield ' for '
        yield target_user.name_at(guild_id)
    
    yield '?\n\nIt will cost you '
    yield str(required_balance)
    yield ' '
    yield EMOJI__HEART_CURRENCY.as_emoji
    yield '.'


def produce_buy_role_success_description(
    role,
    current_balance,
    required_balance,
    target_user,
    guild_id,
):
    """
    Produces buy roles notification.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    role : ``Role``
        The role to be purchased.
    
    current_balance : `int`
        The user's current balance.
    
    required_balance : `int`
        The required balance for upgrading.
    
    target_user : ``None | ClientUserBase``
        The targeted user if any.
    
    guild_id : `int`
        The local guild's identifier.
    
    Yields
    ------
    part : `str`
    """
    yield 'You purchased '
    
    yield role.name
    yield ' role'
    
    if (target_user is not None):
        yield ' for '
        yield target_user.name_at(guild_id)
   
    yield '.\n\nYour '
    yield EMOJI__HEART_CURRENCY.as_emoji
    yield ':\n'
    yield from produce_modification_description(current_balance, -required_balance)


def produce_buy_role_notification_description(
    role,
    source_user,
    guild_id,
):
    """
    Produces buy roles notification.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    role : ``Role``
        The role to be purchased.
    
    source_user : `ClientUserBase``
        The purchasing user.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Yields
    ------
    part : `str`
    """
    yield source_user.name_at(guild_id)
    yield ' gifted you '
    yield role.name
    yield ' role.'
