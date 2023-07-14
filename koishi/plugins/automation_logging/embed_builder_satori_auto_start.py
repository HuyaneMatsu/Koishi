__all__ = ()

from hata import Color, Embed

from .embed_builder_user import (
    render_created_into, render_created_joined_difference_into, render_guild_profile_flags_into, render_id_into,
    render_joined_into, render_profile_into
)


SATORI_COLOR = Color.from_rgb(168, 2, 146)
SATORI_IMAGE = 'https://cdn.discordapp.com/attachments/568837922288173058/1109762751963865200/satori-0015-edit-0000.png'


def build_satori_auto_start_embed(guild, user):
    """
    Builds a satori auto start embed.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild in context.
    user : ``ClientUserBase``
        The user who joined.
    
    Returns
    -------
    embed : ``Embed``
    """
    guild_profile = user.get_guild_profile_for(guild)
    
    description_parts = []
    
    render_profile_into(description_parts, user)
    description_parts.append('\n')
    render_id_into(description_parts, user)
    description_parts.append('\n')
    render_guild_profile_flags_into(description_parts, guild_profile)
    description_parts.append('\n\n')
    render_created_into(description_parts, user)
    description_parts.append('\n')
    render_joined_into(description_parts, guild_profile, True)
    description_parts.append('\n')
    render_created_joined_difference_into(description_parts, user, guild_profile, True)
    
    description = ''.join(description_parts)
    description_parts = None
    
    return Embed(
        None, description, color = SATORI_COLOR,
    ).add_thumbnail(
        user.avatar_url,
    ).add_author(
        f'Started watching {user.full_name}'
    ).add_image(
        SATORI_IMAGE,
    )


def build_satori_user_actioned_embed(user, reason, actioned_name):
    """
    Builds a satori user kick or ban embed
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The actioned user.
    reason : `None`, `str`
        The given reason.
    actioned_name : `str`
        The action's name with `-ed` ending.
    
    Returns
    -------
    embed : ``Embed``
    """
    if (reason is None) or (not reason):
        reason = ' '
    
    return Embed(
        color = SATORI_COLOR,
    ).add_thumbnail(
        user.avatar_url,
    ).add_author(
        f'{actioned_name} {user.full_name}'
    ).add_field(
        'Reason',
        (
            f'```\n'
            f'{reason}\n'
            f'```'
        ),
    )

