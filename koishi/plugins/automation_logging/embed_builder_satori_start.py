__all__ = ()

from hata import ActivityType, Color, Embed

from ..rendering_helpers import (
    build_activity_description, build_user_status_description, build_user_with_guild_profile_description
)


SATORI_COLOR = Color.from_rgb(168, 2, 146)
SATORI_IMAGE = 'https://cdn.discordapp.com/attachments/568837922288173058/1109762751963865200/satori-0015-edit-0000.png'


def build_satori_auto_start_header_embed(user, guild_id):
    """
    Builds a satori auto start header embed containing user info.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user who joined.
    guild_id : `int`
        The guild's identifier.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        None,
        build_user_with_guild_profile_description(user, user.get_guild_profile_for(guild_id)),
        color = SATORI_COLOR,
    ).add_thumbnail(
        user.avatar_url,
    ).add_author(
        f'Started watching {user.full_name}'
    )


def build_satori_auto_start_embeds(user, guild_id):
    """
    Builds the satori auto start embeds.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user who joined.
    guild_id : `int`
        The guild's identifier.
    
    Returns
    -------
    embeds : `list` of ``Embed``
    """
    embeds = [
        build_satori_auto_start_header_embed(user, guild_id),
        Embed('Status', build_user_status_description(user), color = SATORI_COLOR),
    ]
    
    custom_activity = user.custom_activity
    if (custom_activity is not None):
        embeds.append(Embed('Custom activity', build_activity_description(custom_activity), color = SATORI_COLOR))
    
    activities_added = 1
    for activity in user.iter_activities():
        # ignore custom
        if activity.type is ActivityType.custom:
            continue
        
        embeds.append(
            Embed(f'Activity ({activities_added})', build_activity_description(activity), color = SATORI_COLOR)
        )
        
        # max 10
        activities_added += 1
        if activities_added > 10:
            break
        
        continue
    
    embeds[-1].add_image(SATORI_IMAGE)
    
    return embeds


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

