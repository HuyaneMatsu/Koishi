__all__ = ('render_activity_description_into',)

from datetime import datetime as DateTime, timezone as TimeZone

from hata import Status, ActivityMetadataCustom, ActivityMetadataHanging, ActivityMetadataRich

from .constants import DATE_TIME_CONDITION_FUTURE, GUILD_PROFILE_RENDER_MODE_JOIN, MESSAGE_RENDER_MODE_CREATE
from .field_renderers import (
    render_attachments_field_into, render_channel_field_into, render_date_time_field_into,
    render_date_time_with_relative_field_into, render_emoji_field_into, render_flags_field_into,
    render_preinstanced_field_into, render_role_mentions_field_into, render_string_field_into,
    render_string_tuple_field_into, render_user_field_into
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
        (DateTime.now(TimeZone.utc) if mode == GUILD_PROFILE_RENDER_MODE_JOIN else None),
        optional = False,
        title = 'Joined',
    )
    
    if mode != GUILD_PROFILE_RENDER_MODE_JOIN:
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
    if mode == GUILD_PROFILE_RENDER_MODE_JOIN:
        joined_at = guild_profile.joined_at
        if (joined_at is None):
            joined_at = DateTime.now(TimeZone.utc)
        
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
        optional = (mode == GUILD_PROFILE_RENDER_MODE_JOIN),
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
    activity_type = activity.type
    into, field_added = render_preinstanced_field_into(into, field_added, activity_type, optional = False)
    metadata_type = activity_type.metadata_type
    
    if metadata_type is ActivityMetadataRich:
        into, field_added = render_string_field_into(into, field_added, activity.name, optional = False, title = 'Name')
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
        into, field_added = render_string_tuple_field_into(into, field_added, activity.buttons, title = 'Buttons')
        into, field_added = render_string_field_into(into, field_added, activity.sync_id, title = 'Sync id')
        into, field_added = render_string_field_into(into, field_added, activity.session_id, title = 'Session id')
        into, field_added = render_flags_field_into(into, field_added, activity.flags)
        
        application_id = activity.application_id
        if application_id:
            into, field_added = render_string_field_into(
                into, field_added, repr(application_id), title = 'Application id'
            )
    
        # This is always false for custom ones, so we can leave it here.
        activity_id = activity.id
        if activity_id:
            into, field_added = render_string_field_into(into, field_added, repr(activity_id), title = 'Id')
    
    elif metadata_type is ActivityMetadataCustom:
        into, field_added = render_emoji_field_into(into, field_added, activity.emoji)
        into, field_added = render_string_field_into(into, field_added, activity.state, title = 'State')
    
    elif metadata_type is ActivityMetadataHanging:
        into, field_added = render_preinstanced_field_into(
            into, field_added, activity.hang_type, optional = False, title = 'Hang type'
        )
        into, field_added = render_emoji_field_into(into, field_added, activity.emoji)
        into, field_added = render_string_field_into(into, field_added, activity.details, title = 'Details')
    
    
    into, field_added = render_date_time_with_relative_field_into(
        into, field_added, activity.created_at, add_ago = True, title = 'Created at'
    )
    

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
        The user to render its status of.
    
    Returns
    -------
    into : `list<str>`
    field_added : `bool`
    """
    status = user.status
    into, field_added = render_string_field_into(into, field_added, status.name, optional = False, title = 'Status')
    status_by_platform = user.status_by_platform
    if (status_by_platform is not None):
        for platform, status in status_by_platform.iter_status_by_platform():
            into, field_added = render_string_field_into(
                into, field_added, status.name, optional = False, title = f'- {platform.name.capitalize()}'
            )
    
    return into, field_added


def render_message_common_description_into(into, field_added, message, mode, title):
    """
    Renders the message's common description.
    
    Parameters
    ----------
    into : `list<str>`
        The container to render into.
    field_added : `bool`
        Whether any fields were added already.
    message : ``Message``
        The message to render.
    mode : `int`
        Whether the message was created or deleted.
    title : `None | str`
        Description title to add.
    
    Returns
    -------
    into : `list<str>`
    field_added : `bool`
    """
    if (title is not None):
        into.append('### ')
        into.append(title)
        into.append('\n')
        field_added = True
    
    content_parts, field_added = render_string_field_into(
        into, field_added, str(message.id), title = 'Id'
    )
    into, field_added = render_preinstanced_field_into(
        into, field_added, message.type
    )
    if mode == MESSAGE_RENDER_MODE_CREATE:
        into, field_added = render_date_time_field_into(
            into, field_added, message.created_at, title = 'Created'
        )
        
    else:
        into, field_added = render_date_time_with_relative_field_into(
            into, field_added, message.created_at, title = 'Created'
        )
        
        into, field_added = render_date_time_field_into(
            into,
            field_added,
            DateTime.now(TimeZone.utc),
            optional = False,
            title = 'Deleted',
        )
    
    content_parts, field_added = render_string_field_into(
        into, field_added, str(len(message)), title = 'Length'
    )
    into, field_added = render_user_field_into(
        into, field_added, message.author, guild = message.guild, title = 'Author'
    )
    into, field_added = render_channel_field_into(into, field_added, message.channel)
    into, field_added = render_attachments_field_into(into, field_added, message.attachments)
    return into, field_added
