__all__ = ()

from hata import Embed

from ...bot_utils.constants import COLOR__GAMBLING, EMOJI__HEART_CURRENCY

from ..balance_rendering import add_other_balance_modification_embed_field


def build_success_embed(target_user, guild_id, down_from, amount):
    """
    Builds a success embed.
    
    Parameters
    ----------
    target_user : ``ClientUserBase``
        The targeted user.
    
    guild_id : `int`
        The respective guild's identifier.
    
    down_from : `int`
        From what amount the user is down from.
    
    Returns
    -------
    embed : ``Embed``
    """
    embed = Embed(
        'Amazing, Awesome, Superb!!',
        f'You took away from {target_user.name_at(guild_id)} {amount} {EMOJI__HEART_CURRENCY.as_emoji}.',
        color = COLOR__GAMBLING,
    )
    
    embed = add_other_balance_modification_embed_field(embed, down_from, -amount)
    
    return embed
