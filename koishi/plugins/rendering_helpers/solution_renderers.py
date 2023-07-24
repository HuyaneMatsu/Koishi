__all__ = ()

from datetime import datetime as DateTime

from .constants import DATE_TIME_CONDITION_FUTURE, GUILD_PROFILE_MODE_JOIN
from .field_renderers import (
    render_date_time_field_into, render_date_time_with_relative_field_into, render_flags_field_into,
    render_role_mentions_field_into, render_string_field_into
)


def render_user_description_into(into, field_added, user):
    """
    Renders user description.
    
    Parameters
    ----------
    into : `list<str>`
        The container to render into.
    field_added : `bool`
        Whether any fields were added already.
    user : ``ClientUserBase``
        The respective user.
    
    Returns
    -------
    into : `list<str>`
    field_added : `bool`
    """
    into, field_added = render_date_time_with_relative_field_into(
        into, field_added, user.created_at, title = 'Created'
    )
    into, field_added = render_string_field_into(
        into, field_added, user.mention, title = 'Profile'
    )
    into, field_added = render_string_field_into(
        into, field_added, str(user.id), title = 'ID'
    )
    into, field_added = render_string_field_into(
        into, field_added, user.display_name, title = 'Display name'
    )
    into, field_added = render_flags_field_into(
        into, field_added, user.flags
    )
    
    return into, field_added


def render_nullable_guild_profile_description_into(into, field_added, guild_profile, mode):
    """
    Renders a nullable guild profile's description.
    
    Parameters
    ----------
    into : `list<str>`
        The container to render into.
    field_added : `bool`
        Whether any fields were added already.
    guild_profile : `None`, ``GuildProfile``
        The user's guild profile.
    mode : `int`
        How the guild profile should be rendered.
    
    Returns
    -------
    into : `list<str>`
    field_added : `bool`
    """
    if guild_profile is None:
        return render_nulled_guild_profile_description_into(into, field_added, mode)
    
    return render_guild_profile_description_into(into, field_added, guild_profile, mode)


def render_nulled_guild_profile_description_into(into, field_added, mode):
    """
    Pair function of ``render_guild_profile_description_into``. Just for the case when `guild_profile` is `None`.
    
    Parameters
    ----------
    into : `list<str>`
        The container to render into.
    field_added : `bool`
        Whether any fields were added already.
    mode : `int`
        How the guild profile should be rendered.
    
    Returns
    -------
    into : `list<str>`
    field_added : `bool`
    """
    into, field_added = render_date_time_field_into(
        into,
        field_added,
        (DateTime.utcnow() if mode == GUILD_PROFILE_MODE_JOIN else None),
        optional = False,
        title = 'Joined',
    )
    
    if mode != GUILD_PROFILE_MODE_JOIN:
        into.append('\nRoles: *none*')
    
    return into, field_added


def render_guild_profile_description_into(into, field_added, guild_profile, mode):
    """
    Renders guild profile description.
    
    Parameters
    ----------
    into : `list<str>`
        The container to render into.
    field_added : `bool`
        Whether any fields were added already.
    guild_profile : ``GuildProfile``
        The user's guild profile.
    mode : `int`
        How the guild profile should be rendered.
    
    Returns
    -------
    into : `list<str>`
    field_added : `bool`
    """
    if mode == GUILD_PROFILE_MODE_JOIN:
        joined_at = guild_profile.joined_at
        if (joined_at is None):
            joined_at = DateTime.utcnow()
        
        into, field_added = render_date_time_field_into(
            into, field_added, joined_at, title = 'Joined'
        )
    else:
        into, field_added = render_date_time_with_relative_field_into(
            into, field_added, guild_profile.joined_at, optional = False, title = 'Joined'
        )
    
    into, field_added = render_role_mentions_field_into(
        into,
        field_added,
        guild_profile.roles,
        optional = (mode == GUILD_PROFILE_MODE_JOIN),
    )
    into, field_added = render_string_field_into(
        into, field_added, guild_profile.nick, title = 'Nick'
    )
    into, field_added = render_date_time_with_relative_field_into(
        into, field_added, guild_profile.boosts_since, add_ago = False, title = 'Booster since'
    )
    into, field_added = render_date_time_with_relative_field_into(
        into,
        field_added,
        guild_profile.timed_out_until,
        add_ago = False,
        title = 'Timed out until',
        condition = DATE_TIME_CONDITION_FUTURE,
    )
    into, field_added = render_flags_field_into(
        into, field_added, guild_profile.flags
    )
    
    return into, field_added
