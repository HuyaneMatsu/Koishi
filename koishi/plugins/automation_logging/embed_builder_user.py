__all__ = ()

from hata import Embed

from ..rendering_helpers import build_user_join_or_leave_description
from .constants import COLOR_ADD, COLOR_DELETE


def build_user_embed(guild, user, guild_profile, join):
    """
    Builds a user join or leave embed.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild in context.
    user : ``ClientUserBase``
        The user who joined or left.
    guild_profile : `None`, ``GuildProfile``
        The user's guild profile in the guild.
    join : `bool`
        Whether the user joined or left.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        user.full_name,
        build_user_join_or_leave_description(user, guild_profile, join),
        color = (COLOR_ADD if join else COLOR_DELETE),
    ).add_thumbnail(
        user.avatar_url,
    ).add_author(
        f'User {"joined" if join else "left"} {guild.name}'
    ).add_footer(
        f'We are now {guild.user_count} shrimps{"!!!" if join else "..."}'
    )
