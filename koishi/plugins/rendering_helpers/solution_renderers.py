__all__ = ('render_activity_description_into',)

from datetime import datetime as DateTime

from hata import ActivityType, Status

from .constants import DATE_TIME_CONDITION_FUTURE, GUILD_PROFILE_MODE_JOIN
from .field_renderers import (
    render_date_time_field_into, render_date_time_with_relative_field_into, render_flags_field_into,
    render_preinstanced_field_into, render_role_mentions_field_into, render_string_field_into
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


def render_activity_description_into(into, field_added, activity):
    """
    Renders activity description.
    
    Parameters
    ----------
    into : `list<str>`
        The container to render into.
    field_added : `bool`
        Whether any fields were added already.
    activity : ``Activity``
        The activity to render.
    
    Returns
    -------
    into : `list<str>`
    field_added : `bool`
    """
    into, field_added = render_string_field_into(into, field_added, activity.name, optional = False, title = 'Name')
    activity_type = activity.type
    into, field_added = render_preinstanced_field_into(into, field_added, activity_type, optional = False)
    
    if activity_type is not ActivityType.custom:
        timestamps = activity.timestamps
        if (timestamps is not None):
            into, field_added = render_date_time_field_into(
                into, field_added, timestamps.start, title = 'Timestamp start'
            )
            into, field_added = render_date_time_field_into(
                into, field_added, timestamps.end, title = 'Timestamp end'
            )
        
        into, field_added = render_string_field_into(into, field_added, activity.details, title = 'Details')
        into, field_added = render_string_field_into(into, field_added, activity.state, title = 'State')
        
        party = activity.party
        if (party is not None):
            into, field_added = render_string_field_into(into, field_added, party.id, title = 'Party id')
            
            party_size = party.size
            party_max = party.max
            if party_size or party_max:
                into, field_added = render_string_field_into(into, field_added, repr(party_size), title = 'Party size')
                into, field_added = render_string_field_into(into, field_added, repr(party_max), title = 'Party max')
        
        assets = activity.assets
        if (assets is not None):
            into, field_added = render_string_field_into(
                into, field_added, assets.image_large, title = 'Assets image large'
            )
            into, field_added = render_string_field_into(
                into, field_added, assets.text_large, title = 'Assets text large'
            )
            into, field_added = render_string_field_into(
                into, field_added, assets.image_small, title = 'Assets image small'
            )
            into, field_added = render_string_field_into(
                into, field_added, assets.text_small, title = 'Assets text small'
            )
        
        secrets = activity.secrets
        if (secrets is not None):
            into, field_added = render_string_field_into(
                into, field_added, secrets.join, title = 'Secrets join'
            )
            into, field_added = render_string_field_into(
                into, field_added, secrets.match, title = 'Secrets match'
            )
            into, field_added = render_string_field_into(
                into, field_added, secrets.spectate, title = 'Secrets spectate'
            )
        
        into, field_added = render_string_field_into(
            into, field_added, activity.spotify_album_cover_url, title = 'Spotify album cover url'
        )
        
        into, field_added = render_string_field_into(into, field_added, activity.url, title = 'Url')
        into, field_added = render_string_field_into(into, field_added, activity.sync_id, title = 'Sync id')
        into, field_added = render_string_field_into(into, field_added, activity.session_id, title = 'Session id')
        into, field_added = render_flags_field_into(into, field_added, activity.flags)
        
        application_id = activity.application_id
        if application_id:
            into, field_added = render_string_field_into(
                into, field_added, repr(application_id), title = 'Application id'
            )
    
    into, field_added = render_date_time_with_relative_field_into(
        into, field_added, activity.created_at, add_ago = True, title = 'Created at'
    )
    
    # This is always false for custom ones, so we can leave it here.
    activity_id = activity.id
    if activity_id:
        into, field_added = render_string_field_into(into, field_added, repr(activity_id), title = 'Id')

    return into, field_added


def render_user_status_description_into(into, field_added, user):
    """
    Renders the user's status.
    
    Parameters
    ----------
    into : `list<str>`
        The container to render into.
    field_added : `bool`
        Whether any fields were added already.
    user : ``ClientUserBase``
        The User to render its status of.
    
    Returns
    -------
    into : `list<str>`
    field_added : `bool`
    """
    status = user.status
    into, field_added = render_string_field_into(into, field_added, status.name, optional = False, title = 'Status')
    if status is not Status.offline:
        into, field_added = render_string_field_into(
            into, field_added, user.get_status_by_platform('desktop').name, optional = False, title = '- Desktop'
        )
        into, field_added = render_string_field_into(
            into, field_added, user.get_status_by_platform('mobile').name, optional = False, title = '- Mobile'
        )
        into, field_added = render_string_field_into(
            into, field_added, user.get_status_by_platform('web').name, optional = False, title = '- Web'
        )
    
    return into, field_added
