__all__ = ()

from hata import Embed

from ...bot_utils.constants import COLOR__GAMBLING, EMOJI__HEART_CURRENCY

from ..balance_rendering import add_modification_embed_field


def build_success_embed(target_user, guild_id, up_from, amount, message):
    """
    Builds a success embed.
    
    Parameters
    ----------
    target_user : ``ClientUserBase``
        The targeted user.
    
    guild_id : `int`
        The respective guild's identifier.
    
    up_from : `int`
        From what amount the user is up from.
    
    amount : `int`
        The amount teh user was awarded with.
    
    awarded_with : `str`
        With what the user is awarded with.
    
    message : `None | str`
        Additional message.
    
    Returns
    -------
    embed : ``Embed``
    """
    embed = Embed(
        'Amazing, Awesome, Superb!!',
        f'You awarded {target_user.name_at(guild_id)} with {amount} {EMOJI__HEART_CURRENCY}.',
        color = COLOR__GAMBLING,
    )
    
    embed = add_modification_embed_field(embed, f'Their {EMOJI__HEART_CURRENCY}', up_from, amount)
    
    if (message is not None):
        embed.add_field('Message:', message)
    
    return embed


def build_notification_embed(source_user, guild_id, up_from, amount, message):
    """
    Builds notification embed.
    
    Parameters
    ----------
    source_user : ``ClientUserBase``
        The source user.
    
    guild_id : `int`
        The respective guild's identifier.
    
    up_from : `int`
        From what amount the user is up from.
    
    message : `None | str`
        Additional message.
    
    Returns
    -------
    embed : ``Embed``
    """
    embed = Embed(
        'Amazing, Awesome, Superb!!',
        f'You have been awarded by {source_user.name_at(guild_id)} with {amount} {EMOJI__HEART_CURRENCY}.',
        color = COLOR__GAMBLING,
    )
    
    embed = add_modification_embed_field(embed, f'Your {EMOJI__HEART_CURRENCY}', up_from, amount)
    
    if (message is not None):
        embed.add_field('Message:', message)
    
    return embed
