__all__ = ('build_user_icon_embed', 'build_user_info_embed')

from hata import Embed

from ..rendering_helpers import build_guild_profile_description, build_user_description

from .constants import ICON_SOURCES_REVERSED, ICON_KINDS_REVERSED
from .icon_helpers import get_icon_of


def build_user_icon_embed(user, guild_id, icon_kind, icon_source):
    """
    Builds an icon embed.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The respective user.
    guild_id : `int`
        The context's guild's identifier.
    icon_kind : `int`
        Which icon should be taken of the user.
    icon_source : `int`
        From which source should be the icon taken from.
    
    Returns
    -------
    embed : ``Embed``
    """
    icon_url = get_icon_of(user, guild_id, icon_kind, icon_source)
    
    icon_source_name = ICON_SOURCES_REVERSED[icon_source]
    icon_kind_name = ICON_KINDS_REVERSED[icon_kind]
    
    color = user.color_at(guild_id)
    
    embed = Embed(
        f'{user.name_at(guild_id)}\'s {icon_source_name!s} {icon_kind_name!s}',
        color = (color if color else None),
        url = icon_url,
    )

    if icon_url is None:
        embed.add_footer(
            f'The user has no {icon_source_name!s} {icon_kind_name!s}.',
        )
    else:
        embed.add_image(
            icon_url,
        )
    
    return embed


def build_user_info_embed(user, guild_id):
    """
    Builds a user info embed.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The respective user.
    guild_id : `int`
        The context's guild's identifier.
    
    Returns
    -------
    embed : ``Embed``
    """
    color = user.color_at(guild_id)
    
    embed = Embed(
        user.full_name,
        color = (color if color else None),
    ).add_thumbnail(
        user.avatar_url_at_as(guild_id),
    ).add_field(
        'User information',
        build_user_description(user),
    )
    
    guild_profile = user.get_guild_profile_for(guild_id)
    if (guild_profile is not None):
        
        embed.add_field(
            'In guild profile',
            build_guild_profile_description(guild_profile),
        )
    
    return embed
