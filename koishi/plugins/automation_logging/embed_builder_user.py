__all__ = ()

from hata import Color, Embed

from ..rendering_helpers import build_user_join_or_leave_description


USER_COLOR_JOIN = Color.from_rgb(2, 168, 77)
USER_COLOR_LEAVE = Color.from_rgb(168, 49, 2)


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
        color = (USER_COLOR_JOIN if join else USER_COLOR_LEAVE),
    ).add_thumbnail(
        user.avatar_url,
    ).add_author(
        f'User {"joined" if join else "left"} {guild.name}'
    )

