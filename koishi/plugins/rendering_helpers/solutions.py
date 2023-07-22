__all__ = ('build_guild_profile_description', 'build_user_description')

from .field_renderers import (
    render_date_time_field_into, render_flags_field_into, render_role_mentions_field_into, render_string_field_into
)


def build_user_description(user):
    """
    Builds user description.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The respective user.
    
    Returns
    -------
    description : `str`
    """
    into_parts = []
    field_added = False
    
    into_parts, field_added = render_date_time_field_into(
        into_parts, field_added, user.created_at, title = 'Created'
    )
    into_parts, field_added = render_string_field_into(
        into_parts, field_added, user.mention, title = 'Profile'
    )
    into_parts, field_added = render_string_field_into(
        into_parts, field_added, str(user.id), title = 'ID'
    )
    into_parts, field_added = render_string_field_into(
        into_parts, field_added, user.display_name, title = 'Display name'
    )
    into_parts, field_added = render_flags_field_into(
        into_parts, field_added, user.flags
    )
    
    return ''.join(into_parts)


def build_guild_profile_description(guild_profile):
    """
    Builds guild profile description.
    
    Parameters
    ----------
    guild_profile : ``GuildProfile``
        The user's guild profile.
    
    Returns
    -------
    description : `str`
    """
    into_parts = []
    field_added = False
    
    into_parts, field_added = render_date_time_field_into(
        into_parts, field_added, guild_profile.joined_at, optional = False, title = 'Joined'
    )
    into_parts, field_added = render_role_mentions_field_into(
        into_parts, field_added, guild_profile.roles, optional = False
    )
    into_parts, field_added = render_string_field_into(
        into_parts, field_added, guild_profile.nick, title = 'Nick'
    )
    into_parts, field_added = render_date_time_field_into(
        into_parts, field_added, guild_profile.boosts_since, add_ago = False, title = 'Booster since'
    )
    into_parts, field_added = render_date_time_field_into(
        into_parts, field_added, guild_profile.timed_out_until, add_ago = False, title = 'Timed out until',when = 1
    )
    into_parts, field_added = render_flags_field_into(
        into_parts, field_added, guild_profile.flags
    )
    
    return ''.join(into_parts)
