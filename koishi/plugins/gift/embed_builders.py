__all__ = ()

from hata import Embed

from ...bot_utils.constants import COLOR__GAMBLING, EMOJI__HEART_CURRENCY

from ..balance_rendering import add_other_balance_modification_embed_field, add_self_balance_modification_embed_field


def build_failure_embed_no_target_user():
    """
    Builds a failure embed for the case when no target user was selected.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        'Cannot gift to user',
        'Please select a target user to gift to.',
        color = COLOR__GAMBLING,
    )


def build_failure_embed_self_target():
    """
    Builds a failure embed for the case when the user is targeting themselves.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        'Cannot gift to user',
        'You cannot gift hearts to yourself, my little lonely potato.',
        color = COLOR__GAMBLING,
    )


def build_failure_embed_invalid_amount():
    """
    Builds a failure embed for the case when the user trying to gift an invalid amount.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        'Invalid gift amount',
        'Cannot gift non-positive amount of hearts. >:3',
        color = COLOR__GAMBLING,
    )


def build_failure_embed_no_balance(with_allocated):
    """
    Builds a failure embed for the case when the user does not have any balance.
    
    Parameters
    ----------
    with_allocated : `bool`
        Whether the allocated balance amount is already calculated in.
    
    Returns
    -------
    embed : ``Embed``
    """
    if with_allocated:
        description = 'Like a flower...\nWhithering to the dust.'
    else:
        description = 'You do not have any hearts to gift.'
    
    return Embed(
        'Not enough hearts',
        description,
        color = COLOR__GAMBLING,
    )


def build_success_embed(source_balance, target_balance, amount, target_user, guild_id, message):
    """
    Builds a success embed when the hearts are being gifted.
    
    Parameters
    ----------
    source_balance : `int`
        The source user's balance.
    
    target_balance : `int`
        The target user's balance.
    
    amount : `int`
        The amount of balance gifted.
    
    target_user : ``ClientUserBase``
        The targeted user.
    
    guild_id : `int`
        The respective guild's identifier.
    
    message : `None | str`
        Additional message from the gifter.
    
    Returns
    -------
    embed : ``Embed``
    """
    embed = Embed(
        'Aww, so lovely',
        f'You gifted {amount} {EMOJI__HEART_CURRENCY} to {target_user.name_at(guild_id)}.',
        color = COLOR__GAMBLING,
    )
    
    embed = add_self_balance_modification_embed_field(embed, source_balance, -amount)
    embed = add_other_balance_modification_embed_field(embed, target_balance, amount)
    
    if (message is not None):
        embed.add_field('Message', message)
    
    return embed


def build_notification_embed(target_balance, amount, source_user, guild_id, message):
    """
    Builds a notification embed when hearts were gifted.
    
    Parameters
    ----------
    target_balance : `int`
        The target user's balance.
    
    amount : `int`
        The amount of balance gifted.
    
    source_user : ``ClientUserBase``
        The source user.
    
    guild_id : `int`
        The respective guild's identifier.
    
    message : `None | str`
        Additional message from the gifter.
    
    Returns
    -------
    embed : ``Embed``
    """
    embed = Embed(
        'Aww, love is in the air',
        f'You have been gifted {amount} {EMOJI__HEART_CURRENCY} by {source_user.name_at(guild_id)}.',
        color = COLOR__GAMBLING,
    )
    
    embed = add_self_balance_modification_embed_field(embed, target_balance, amount)
    
    if (message is not None):
        embed.add_field('Message', message)
    
    return embed
