__all__ = (
    'build_activity_description', 'build_guild_profile_description', 'build_user_description',
    'build_user_join_or_leave_description', 'build_user_status_description', 'build_user_with_guild_profile_description'
)

from datetime import datetime as DateTime

from .constants import GUILD_PROFILE_MODE_GENERAL, GUILD_PROFILE_MODE_JOIN, GUILD_PROFILE_MODE_LEAVE
from .field_renderers import render_date_time_difference_field_into, render_date_time_field_into
from .solution_renderers import (
    render_activity_description_into, render_guild_profile_description_into,
    render_nullable_guild_profile_description_into, render_user_description_into, render_user_status_description_into
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
    into, field_added = render_user_description_into([], False, user)
    return ''.join(into)


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
    into, field_added = render_guild_profile_description_into([], False, guild_profile, GUILD_PROFILE_MODE_GENERAL)
    return ''.join(into)


def build_user_with_guild_profile_description(user, guild_profile):
    """
    Builds a user description with its guild profile's
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user who joined or left.
    guild_profile : `None`, ``GuildProfile``
        The user's guild profile.
    
    Returns
    -------
    description : `str`
    """
    into = []
    field_added = False
    
    into, field_added = render_user_description_into(into, field_added, user)
    
    if field_added:
        into.append('\n')
    
    into, field_added = render_nullable_guild_profile_description_into(
        into, field_added, guild_profile, GUILD_PROFILE_MODE_GENERAL
    )
    
    return ''.join(into)


def build_user_join_or_leave_description(user, guild_profile, join):
    """
    Builds a user join / leave description.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user who joined or left.
    guild_profile : `None`, ``GuildProfile``
        The user's guild profile.
    join : `bool`
        Whether the user joined or left.
    
    Returns
    -------
    description : `str`
    """
    into = []
    field_added = False
    
    into, field_added = render_user_description_into(into, field_added, user)
    
    if field_added:
        into.append('\n')
    
    into, field_added = render_nullable_guild_profile_description_into(
        into, field_added, guild_profile, GUILD_PROFILE_MODE_JOIN if join else GUILD_PROFILE_MODE_LEAVE
    )
    
    if not join:
        if field_added:
            into.append('\n')
        
        into, field_added = render_date_time_field_into(
            into,
            field_added,
            DateTime.utcnow(),
            optional = False,
            title = 'Left',
        )
        into, field_added = render_date_time_difference_field_into(
            into,
            field_added,
            user.created_at,
            (None if guild_profile is None else guild_profile.created_at),
            optional = False,
            title = 'Created - joined',
        )
    
    return ''.join(into)


def build_activity_description(activity):
    """
    Builds the activity's description.
    
    Parameters
    ----------
    activity : ``Activity``
        The activity to render.
    
    Returns
    -------
    description : `str`
    """
    into, field_added = render_activity_description_into([], False, activity)
    return ''.join(into)


def build_user_status_description(user):
    """
    Builds the user's status' description
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The User to render its status of.
   
    Returns
    -------
    description : `str`
    """
    into, field_added = render_user_status_description_into([], False, user)
    return ''.join(into)
