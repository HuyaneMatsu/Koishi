__all__ = ()

from datetime import datetime as DateTime

from hata import ActivityType, DATETIME_FORMAT_CODE, Embed, Status, elapsed_time

from ..rendering_helpers import render_activity_description_into

from .constants import COLOR_UPDATE


MAX_CHUNK_SIZE = 2000
BREAK_AFTER_LINE_COUNT = 1500
OFFLINE = Status.offline.name


def render_presence_update(user, old_attributes):
    """
    Renders a presence update event and returns the rendered parts.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user in context.
    old_attributes : `dict` of (`str`, `object`) items
        The user's modified attributes.
    
    Returns
    -------
    into : `list` of `str`
    """
    into = []
    
    into.append('User: ')
    into.append(user.full_name)
    
    into.append(' (')
    into.append(repr(user.id))
    into.append(')\n')
    
    into.append('At: ')
    into.append(format(DateTime.utcnow(), DATETIME_FORMAT_CODE))
    into.append('\n\n')
    
    try:
        statuses = old_attributes['statuses']
    except KeyError:
        pass
    else:
        try:
            status = old_attributes['status']
        except KeyError:
            pass
        else:
            into.append('**Display status**')
            into.append('\n')
            into.append(status.name)
            into.append(' -> ')
            into.append(user.status.name)
            into.append('\n')
            into.append('\n')
        
        into.append('**Statuses by device**')
        into.append('\n')
        
        for key in ('desktop', 'mobile', 'web'):
            into.append(key)
            into.append(': ')
            into.append(OFFLINE if statuses is None else statuses.get(key, OFFLINE))
            into.append(' -> ')
            
            user_statuses = user.statuses
            if user_statuses is None:
                status_by_platform = OFFLINE
            else:
                status_by_platform = user_statuses.get(key, OFFLINE)
            into.append(status_by_platform)
            into.append('\n')
        
        into.append('\n')
    
    try:
        activities = old_attributes['activities']
    except KeyError:
        pass
    else:
        added, updated, removed = activities
        if (added is not None):
            for activity in added:
                into.append('**Added activity**:')
                render_activity_description_into(into, True, activity)
                into.append('\n')
        
        if (updated is not None):
            for activity_change in updated:
                into.append('**Updated activity**:')
                into.append('\n')
                activity = activity_change.activity
                for key, value in activity_change.old_attributes.items():
                    ACTIVITY_DIFFERENCE_RENDERERS[key](into, value, activity)
                into.append('\n')
        
        if (removed is not None):
            for activity in removed:
                into.append('**Removed activity**:')
                render_activity_description_into(into, True, activity)
                into.append('\n')
    
    return into


def render_date_time_into(into, date_time_value):
    """
    Renders the give date time into the given container.
    
    Parameters
    ----------
    into : `list` of `str`
        The container to render into.
    date_time_value : `DateTime`
        The date time to render.
    
    Returns
    -------
    into : `list` of `str`
    """
    into.append(format(date_time_value, DATETIME_FORMAT_CODE))
    into.append(' [')
    into.append(elapsed_time(date_time_value))
    into.append(' ago]')
    return into



def render_representation_difference_into(into, old_value, new_value):
    """
    Renders the given old and new value with their representation as a difference.
    
    Parameters
    ----------
    into : `list` of `str`
        The container to render into.
    old_value : `object`
        The old value to render.
    new_value : `object`
        The new value to render.
    
    Returns
    -------
    into : `list` of `str`
    """
    into.append('null' if old_value is None else repr(old_value))
    into.append(' -> ')
    into.append('null' if new_value is None else repr(new_value))
    into.append('\n')
    return into


def render_nullable_date_time_into(into, date_time):
    """
    Renders a nullable date-time value into the given container.
    
    Parameters
    ----------
    into : `list` of `str`
        The container to render into.
    date_time : `None`, `DateTime`
        The date-time to render.
    
    Returns
    -------
    into : `list` of `str`
    """
    if date_time is None:
        into.append('null')
    else:
        render_date_time_into(into, date_time)
    return into


def render_date_time_difference_only_into(into, old_date_time, new_date_time):
    """
    Renders date-time difference only into the given container.
    
    The rendered value is nameless.
    
    Parameters
    ----------
    into : `list` of `str`
        The container to render into.
    old_date_time : `None`, `DateTime`
        The old date-time to render.
    new_date_time : `None`, `DateTime`
        The new date-time to render.
    
    Returns
    -------
    into : `list` of `str`
    """
    render_nullable_date_time_into(into, old_date_time)
    into.append(' -> ')
    render_nullable_date_time_into(into, new_date_time)
    into.append('\n')
    return into


def render_name_difference_into(into, old_name, activity):
    """
    Renders name difference into the given containers.
    
    Parameters
    ----------
    into : `list` of `str`
        The container to render into.
    old_name : `str`
        The activity's old name.
    activity : ``Activity``
        The activity in context to pull the new name from.
    
    Returns
    -------
    into : `list` of `str`
    """
    into.append('Name: ')
    render_representation_difference_into(into, old_name, activity.name)
    return into


def render_type_difference_into(into, old_type, activity):
    """
    Renders type difference into the given containers.
    
    Parameters
    ----------
    into : `list` of `str`
        The container to render into.
    old_type : ``ActivityType``
        The activity's old type.
    activity : ``Activity``
        The activity in context to pull the new type from.
    
    Returns
    -------
    into : `list` of `str`
    """
    new_type = activity.type
    into.append('Type: ')
    into.append(old_type.name)
    into.append(' ~ ')
    into.append(repr(old_type.value))
    into.append(' -> ')
    into.append(new_type.name)
    into.append(' ~ ')
    into.append(repr(new_type.value))
    into.append('\n')
    return into


def render_timestamps_difference_into(into, old_timestamps, activity):
    """
    Renders timestamps difference into the given containers.
    
    Parameters
    ----------
    into : `list` of `str`
        The container to render into.
    old_timestamps : `None`, ``ActivityTimeStamps``
        The activity's old timestamps.
    activity : ``Activity``
        The activity in context to pull the new timestamps from.
    
    Returns
    -------
    into : `list` of `str`
    """
    if old_timestamps is None:
        old_timestamp_start = None
        old_timestamp_end = None
    else:
        old_timestamp_start = old_timestamps.start
        old_timestamp_end = old_timestamps.end
        
    new_timestamps = activity.timestamps
    if new_timestamps is None:
        new_timestamp_start = None
        new_timestamp_end = None
    else:
        new_timestamp_start = new_timestamps.start
        new_timestamp_end = new_timestamps.end
    
    if old_timestamp_start != new_timestamp_start:
        into.append('Timestamp start: ')
        render_date_time_difference_only_into(into, old_timestamp_start, new_timestamp_start)
    
    if old_timestamp_end != new_timestamp_end:
        into.append('Timestamp end: ')
        render_date_time_difference_only_into(into, old_timestamp_end, new_timestamp_end)
    
    return into


def render_details_difference_into(into, old_details, activity):
    """
    Renders details difference into the given containers.
    
    Parameters
    ----------
    into : `list` of `str`
        The container to render into.
    old_details : `None`, `str`
        The activity's old details.
    activity : ``Activity``
        The activity in context to pull the new details from.
    
    Returns
    -------
    into : `list` of `str`
    """
    into.append('Details: ')
    render_representation_difference_into(into, old_details, activity.details)
    return into


def render_state_difference(into, old_state, activity):
    """
    Renders state difference into the given containers.
    
    Parameters
    ----------
    into : `list` of `str`
        The container to render into.
    old_state : `None`, `str`
        The activity's old state.
    activity : ``Activity``
        The activity in context to pull the new state from.
    
    Returns
    -------
    into : `list` of `str`
    """
    into.append('State: ')
    render_representation_difference_into(into, old_state, activity.state)
    return into


def render_party_difference_into(into, old_party, activity):
    """
    Renders party difference into the given containers.
    
    Parameters
    ----------
    into : `list` of `str`
        The container to render into.
    old_party : `None`, ``ActivityParty``
        The activity's old party.
    activity : ``Activity``
        The activity in context to pull the new party from.
    
    Returns
    -------
    into : `list` of `str`
    """
    if old_party is None:
        old_party_id = None
        old_party_size = 0
        old_party_max = 0
    else:
        old_party_id = old_party.id
        old_party_size = old_party.size
        old_party_max = old_party.max
        
    new_party = activity.party
    if new_party is None:
        new_party_id = None
        new_party_size = 0
        new_party_max = 0
    else:
        new_party_id = new_party.id
        new_party_size = new_party.size
        new_party_max = new_party.max
    
    if old_party_id != new_party_id:
        into.append('Party id: ')
        render_representation_difference_into(into, old_party_id, new_party_id)
    
    if old_party_size or old_party_max or new_party_size or new_party_max:
        if (old_party_size or new_party_size) and (old_party_size != new_party_size):
            into.append('Party size: ')
            render_representation_difference_into(into, old_party_size, new_party_size)
        
        if (old_party_max or new_party_max) and (old_party_max != new_party_max):
            into.append('Party max: ')
            render_representation_difference_into(into, old_party_max, new_party_max)
    
    return into


def render_assets_difference_into(into, old_assets, activity):
    """
    Renders assets difference into the given containers.
    
    Parameters
    ----------
    into : `list` of `str`
        The container to render into.
    old_assets : `None`, ``ActivityAssets`˙
        The activity's old assets.
    activity : ``Activity``
        The activity in context to pull the new assets from.
    
    Returns
    -------
    into : `list` of `str`
    """
    if old_assets is None:
        old_asset_image_large = None
        old_asset_text_large = None
        old_asset_image_small = None
        old_asset_text_small = None
    else:
        old_asset_image_large = old_assets.image_large
        old_asset_text_large = old_assets.text_large
        old_asset_image_small = old_assets.image_small
        old_asset_text_small = old_assets.text_small
    
    new_assets = activity.assets
    if new_assets is None:
        mew_asset_image_large = None
        new_asset_text_large = None
        mew_asset_image_small = None
        new_asset_text_small = None
    else:
        mew_asset_image_large = new_assets.image_large
        new_asset_text_large = new_assets.text_large
        mew_asset_image_small = new_assets.image_small
        new_asset_text_small = new_assets.text_small
    
    if old_asset_image_large != mew_asset_image_large:
        into.append('Assets image large: ')
        render_representation_difference_into(into, old_asset_image_large, mew_asset_image_large)
    
    if old_asset_text_large != new_asset_text_large:
        into.append('Assets text large: ')
        render_representation_difference_into(into, old_asset_text_large, new_asset_text_large)
    
    if old_asset_image_small != mew_asset_image_small:
        into.append('Assets image small: ')
        render_representation_difference_into(into, old_asset_image_small, mew_asset_image_small)
    
    if old_asset_text_small != new_asset_text_small:
        into.append('Assets text small: ')
        render_representation_difference_into(into, old_asset_text_small, new_asset_text_small)
    
    return into


def render_album_cover_url_difference_into(into, old_spotify_album_cover_url, activity):
    """
    Renders spotify album cover url difference into the given containers.
    
    Parameters
    ----------
    into : `list` of `str`
        The container to render into.
    old_spotify_album_cover_url : `None`, `str`
        The old spotify album cover url.
    activity : ``Activity``
        The activity in context to pull the new spotify album cover url from.
    
    Returns
    -------
    into : `list` of `str`
    """
    into.append('Spotify album cover url: ')
    render_representation_difference_into(into, old_spotify_album_cover_url, activity.spotify_album_cover_url)
    return into


def render_secrets_difference_into(into, old_secrets, activity):
    """
    Renders activity secrets into the given containers.
    
    Parameters
    ----------
    into : `list` of `str`
        The container to render into.
    old_secrets : `None`, ``ActivitySecret``
        The activity's old secrets.
    activity : ``Activity``
        The activity in context to pull the new secrets from.
    
    Returns
    -------
    into : `list` of `str`
    """
    if old_secrets is None:
        old_secret_join = None
        old_secret_spectate = None
        old_secret_match = None
    else:
        old_secret_join = old_secrets.join
        old_secret_spectate = old_secrets.spectate
        old_secret_match = old_secrets.match
        
    new_secrets = activity.secrets
    if new_secrets is None:
        new_secret_join = None
        new_secret_spectate = None
        new_secret_match = None
    else:
        new_secret_join = new_secrets.join
        new_secret_spectate = new_secrets.spectate
        new_secret_match = new_secrets.match
        
    if old_secret_join != new_secret_join:
        into.append('Secrets join: ')
        render_representation_difference_into(into, old_secret_join, new_secret_join)
    
    if old_secret_spectate != new_secret_spectate:
        into.append('Secrets spectate: ')
        render_representation_difference_into(into, old_secret_spectate, new_secret_spectate)
    
    if old_secret_match != new_secret_match:
        into.append('Secrets spectate: ')
        render_representation_difference_into(into, old_secret_match, new_secret_match)
    
    return into


def render_url_difference_into(into, old_url, activity):
    """
    Renders url difference into the given containers.
    
    Parameters
    ----------
    into : `list` of `str`
        The container to render into.
    old_url : `None`, `str`
        The activity's old url.
    activity : ``Activity``
        The activity in context to pull the new url from.
    
    Returns
    -------
    into : `list` of `str`
    """
    into.append('Url: ')
    render_representation_difference_into(into, old_url, activity.url)
    return into


def render_sync_id_difference_into(into, old_sync_id, activity):
    """
    Renders sync-id difference into the given containers.
    
    Parameters
    ----------
    into : `list` of `str`
        The container to render into.
    old_sync_id : `None`, `str`
        The activity's old sync-id.
    activity : ``Activity``
        The activity in context to pull the new sync-id from.
    
    Returns
    -------
    into : `list` of `str`
    """
    into.append('Sync id: ')
    render_representation_difference_into(into, old_sync_id, activity.sync_id)
    return into


def render_session_id_difference_into(into, old_session_id, activity):
    """
    Renders session-id difference into the given containers.
    
    Parameters
    ----------
    into : `list` of `str`
        The container to render into.
    old_session_id : `None`, `str`
        The activity's old session-id.
    activity : ``Activity``
        The activity in context to pull the new session-id from.
    
    Returns
    -------
    into : `list` of `str`
    """
    into.append('Session id: ')
    render_representation_difference_into(into, old_session_id, activity.session_id)
    return into


def render_flags_difference_into(into, old_flags, activity):
    """
    Renders flags difference into the given containers.
    
    Parameters
    ----------
    into : `list` of `str`
        The container to render into.
    old_flags : ``ActivityFlag``
        The activity's old flag value.
    activity : ``Activity``
        The activity in context to pull the new flags from.
    
    Returns
    -------
    into : `list` of `str`
    """
    into.append('Flags: ')
    into.append(', '.join(old_flags))
    into.append(' -> ')
    into.append(', '.join(activity.flags))
    into.append('\n')
    return into


def render_application_id_difference_into(into, old_application_id, activity):
    """
    Renders application-id difference into the given containers.
    
    Parameters
    ----------
    into : `list` of `str`
        The container to render into.
    old_application_id : `int`
        The activity's old application-id.
    activity : ``Activity``
        The activity in context to pull the new application-id from.
    
    Returns
    -------
    into : `list` of `str`
    """
    into.append('Application id: ')
    render_representation_difference_into(into, old_application_id, activity.application_id)
    return into


def render_created_at_difference_into(into, old_created_at, activity):
    """
    Renders created-at difference into the given containers.
    
    Parameters
    ----------
    into : `list` of `str`
        The container to render into.
    old_created_at : `DateTime`
        The activity's old created-at.
    activity : ``Activity``
        The activity in context to pull the new created-at from.
    
    Returns
    -------
    into : `list` of `str`
    """
    into.append('Created at: ')
    render_date_time_difference_only_into(into, old_created_at, activity.created_at)
    return into


def render_id_difference_into(into, old_activity_id, activity):
    """
    Renders activity-id difference into the given containers.
    
    Parameters
    ----------
    into : `list` of `str`
        The container to render into.
    old_activity_id : `int`
        The activity's old identifier.
    activity : ``Activity``
        The activity in context to pull the new identifier from.
    
    Returns
    -------
    into : `list` of `str`
    """
    into.append('Id: ')
    render_representation_difference_into(into, old_activity_id, activity.id)
    return into


def render_emoji_into(into, emoji):
    """
    Renders the emoji into the given container.
    
    Parameters
    ----------
    into : `list` of `str`
        The container to render into.
    emoji : `None`, ``Emoji``
        The emoji to render.
    
    Returns
    -------
    into : `list` of `str`
    """
    if emoji is None:
        into.append('null')
    else:
        into.append(emoji.name)
        into.append(' ~ ')
        into.append(str(emoji.id))
    
    return into


def render_emoji_difference_into(into, old_emoji, new_emoji):
    """
    Renders the given old and new emojis as a difference.
    
    Parameters
    ----------
    into : `list` of `str`
        The container to render into.
    old_emoji : `None`, ``Emoji``
        The old emoji to render.
    new_emoji : `None`, ``Emoji``
        The new emoji to render.
    
    Returns
    -------
    into : `list` of `str`
    """
    render_emoji_into(into, old_emoji)
    into.append(' -> ')
    render_emoji_into(into, new_emoji)
    into.append('\n')
    return into


ACTIVITY_DIFFERENCE_RENDERERS = {
    'name': render_name_difference_into,
    'type': render_type_difference_into,
    'timestamps': render_timestamps_difference_into,
    'details': render_details_difference_into,
    'state': render_state_difference,
    'party': render_party_difference_into,
    'assets': render_assets_difference_into,
    'album_cover_url': render_album_cover_url_difference_into,
    'secrets': render_secrets_difference_into,
    'url': render_url_difference_into,
    'sync_id': render_sync_id_difference_into,
    'session_id': render_session_id_difference_into,
    'flags': render_flags_difference_into,
    'application_id': render_application_id_difference_into,
    'created_at': render_created_at_difference_into,
    'id': render_id_difference_into,
    'emoji': render_emoji_difference_into,
}


def remove_line_break_from_end(chunk_parts):
    """
    Removes the line breaks from the end of the given chunk parts. Returns `True` if all parts were removed.
    
    Parameters
    ----------
    chunk_parts : `list` of `str`
        The chunk parts to check.
    
    Returns
    -------
    all_removed : `bool`
    """
    while chunk_parts:
        if chunk_parts[-1] == '\n':
            del chunk_parts[-1]
            continue
        
        return False
    
    return True


def add_chunk(chunks, chunk_parts):
    """
    Adds a new chunk to the given `chunks`.
    
    Parameters
    ----------
    chunks : `list` of `str`
        The chunks to extend with the new chunk.
    chunk_parts : `list` of `str`
        Parts of the new chunk.
    """
    if not remove_line_break_from_end(chunk_parts):
        chunks.append(''.join(chunk_parts))
        chunk_parts.clear()


def make_chunks(parts):
    """
    Makes chunks from the given parts.
    
    Parameters
    ----------
    parts : `list` of `str`
        Content parts to chunk.
    
    Returns
    -------
    chunks : `str`
    """
    chunks = []
    chunk_parts = []
    chunk_length = 0
    for part in parts:
        if part == '\n':
            if chunk_parts:
                if chunk_length > BREAK_AFTER_LINE_COUNT:
                    add_chunk(chunks, chunk_parts)
                    chunk_length = 0
                else:
                    chunk_parts.append('\n')
                    chunk_length += 1
            else:
                # Do not add linebreak at the start
                continue
        else:
            chunk_length += len(part)
            if chunk_length > MAX_CHUNK_SIZE:
                chunk_length = MAX_CHUNK_SIZE - chunk_length
                chunk_parts.append(part[:chunk_length])
                add_chunk(chunks, chunk_parts)
                chunk_parts.append(part[chunk_length:])
                chunk_length = -chunk_length
            else:
                chunk_parts.append(part)
    
    add_chunk(chunks, chunk_parts)
    return chunks


def build_presence_update_embeds(user, old_attributes):
    """
    Builds presence update embeds.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user in context.
    old_attributes : `dict` of (`str`, `object`) items
        The user's modified attributes.
    
    Returns
    -------
    embeds : `list` of ``Embed``
    """
    return [
        Embed(description = chunk, color = COLOR_UPDATE)
        for chunk in make_chunks(render_presence_update(user, old_attributes))
    ]
