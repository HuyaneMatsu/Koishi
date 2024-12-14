__all__ = ()

from hata import Embed, elapsed_time

from ...bot_utils.constants import COLOR__GAMBLING, EMOJI__HEART_CURRENCY, URL__KOISHI_TOP_GG


def build_embed_already_claimed_self(daily_can_claim_at):
    """
    Builds an already claimed embed targeting yourself.
    
    Parameters
    ----------
    daily_can_claim_at : `DateTime`
        When the user can claim their daily.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        'You already claimed your daily hearts for today~',
        f'Come back in {elapsed_time(daily_can_claim_at)}.',
        color = COLOR__GAMBLING,
    )


def build_embed_already_claimed_other(daily_can_claim_at, target_user, guild_id):
    """
    Builds an already claimed embed targeting someone else.
    
    Parameters
    ----------
    daily_can_claim_at : `DateTime`
        When the user can claim their daily.
    
    target_user : ``ClientUserBase``
        The targeted user.
    
    guild_id : `int`
        Respective guild's identifier.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        f'{target_user.name_at(guild_id)} already claimed their daily hearts for today~',
        f'Come back in {elapsed_time(daily_can_claim_at)}.',
        color = COLOR__GAMBLING,
    )


def build_embed_daily_claimed_self(received, balance_new, streak_old, streak_new, top_gg_notify):
    """
    Builds a daily-self claim embed.
    
    Parameters
    ----------
    received : `int`
        The amount of received balance.
    
    balance_new : `int`
        The user's new balance.
    
    streak_old : `int`
        The user's previous streak.
    
    streak_new : `int`
        The user's new streak.
    
    top_gg_notify : `bool`
        Whether the user should be encouraged to vote on top.gg.
    
    Returns
    -------
    embed : ``Embed``
    """
    description_parts = []
    
    description_parts.append('You received ')
    description_parts.append(str(received))
    description_parts.append(' ')
    description_parts.append(EMOJI__HEART_CURRENCY.as_emoji)
    description_parts.append(' and now have ')
    description_parts.append(str(balance_new))
    description_parts.append(' ')
    description_parts.append(EMOJI__HEART_CURRENCY.as_emoji)
    description_parts.append('\n')
    
    
    if streak_new > streak_old:
        description_parts.append('You are on a ')
        description_parts.append(str(streak_new))
        description_parts.append(' day streak! Keep up the good work!')
        
    elif streak_new < streak_old:
        description_parts.append('You did not claim daily for more than 1 day, you lost ')
        description_parts.append(str(streak_old - streak_new))
        description_parts.append(' streak, and now you are at ')
        description_parts.append(str(streak_new))
        description_parts.append('.')
        
    else:
        description_parts.append('You did not claim daily for 1 day, your daily stands at ')
        description_parts.append(str(streak_old))
        description_parts.append('.')
    
    if top_gg_notify:
        description_parts.append('\n\nPlease vote for me on [top.gg](')
        description_parts.append(URL__KOISHI_TOP_GG)
        description_parts.append(') for extra ')
        description_parts.append(EMOJI__HEART_CURRENCY.as_emoji)
        description_parts.append(' <3')
    
    
    return Embed(
        'Here, some hearts for you~\nCome back tomorrow !',
        ''.join(description_parts),
        color = COLOR__GAMBLING,
    )


def build_embed_not_related(target_user, guild_id):
    """
    Builds not related embed.
    
    Parameters
    ----------
    target_user : ``ClientUserBase``
        The targeted user.
    
    guild_id : `int`
        Respective guild's identifier.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        'Savage',
        f'{target_user.name_at(guild_id)} is not related to you.',
        color = COLOR__GAMBLING,
    )


def build_embed_daily_claimed_other(received, balance_new, streak_old, streak_new, target_user, guild_id):
    """
    Builds a daily-other claim embed.
    
    Parameters
    ----------
    received : `int`
        The amount of received balance.
    
    balance_new : `int`
        The user's new balance.
    
    streak_old : `int`
        The user's previous streak.
    
    streak_new : `int`
        The user's new streak.
    
    target_user : ``ClientUserBase``
        The targeted user.
    
    guild_id : `int`
        Respective guild's identifier.
    
    Returns
    -------
    embed : ``Embed``
    """
    description_parts = []
    
    description_parts.append(target_user.name_at(guild_id))
    description_parts.append(' received ')
    description_parts.append(str(received))
    description_parts.append(' ')
    description_parts.append(EMOJI__HEART_CURRENCY.as_emoji)
    description_parts.append(' and now they have ')
    description_parts.append(str(balance_new))
    description_parts.append(' ')
    description_parts.append(EMOJI__HEART_CURRENCY.as_emoji)
    description_parts.append('\n')
    
    
    if streak_new > streak_old:
        description_parts.append('They are on a ')
        description_parts.append(str(streak_new))
        description_parts.append(' day streak! Keep up the good work for them!')
        
    elif streak_new < streak_old:
        description_parts.append('They did not claim daily for more than 1 day, they lost ')
        description_parts.append(str(streak_old - streak_new))
        description_parts.append(' streak, and now they have ')
        description_parts.append(str(streak_new))
        description_parts.append('.')
        
    else:
        description_parts.append('They did not claim daily for 1 day, their daily stands at ')
        description_parts.append(str(streak_old))
        description_parts.append('.')
    
    
    return Embed(
        'How sweet, you claimed my hearts for your chosen one !',
        ''.join(description_parts),
        color = COLOR__GAMBLING,
    )


def build_embed_daily_claimed_other_notification(received, balance_new, streak_new, source_user, guild_id):
    """
    Builds a daily claimed by other notification embed.
    
    Parameters
    ----------
    received : `int`
        The amount of received balance.
    
    balance_new : `int`
        The user's new balance.
    
    streak_new : `int`
        The user's new streak.
    
    source_user : ``ClientUserBase``
        The source user.
    
    guild_id : `int`
        Respective guild's identifier.
    
    Returns
    -------
    embed : ``Embed``
    """
    description_parts = []
    
    description_parts.append('You received ')
    description_parts.append(str(received))
    description_parts.append(' ')
    description_parts.append(EMOJI__HEART_CURRENCY.as_emoji)
    description_parts.append(' and now you have ')
    description_parts.append(str(balance_new))
    description_parts.append(' ')
    description_parts.append(EMOJI__HEART_CURRENCY.as_emoji)
    description_parts.append('\nYou are on a ')
    description_parts.append(str(streak_new))
    description_parts.append(' day streak.')
    
    
    return Embed(
        f'{source_user.name_at(guild_id)} claimed daily hearts for you.',
        ''.join(description_parts),
        color = COLOR__GAMBLING,
    )
