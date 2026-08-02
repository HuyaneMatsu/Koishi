__all__ = ()

from math import floor, log10

from hata import DiscordException, ERROR_CODES

from ...bot_utils.user_getter import get_user

from .constants import (
    NOTIFICATION_RESULT_STATE_FAILURE_CONNECTION_OR_SERVER_ISSUE, NOTIFICATION_RESULT_STATE_FAILURE_DMS_CLOSED,
    NOTIFICATION_RESULT_STATE_SUCCESS, REASON_ALLOWED_LENGTH_THRESHOLD, REASON_PATTERN
)


def select_client_with_permission(client, guild, required_permission):
    """
    Selects a client in the guild with permissions. If there is no such guild, returns an error message.
    
    Parameters
    ----------
    client : ``Client``
        Default client.
    
    guild : ``Guild``
        Local guild.
    
    required_permission : ``Permission``
        The required permissions to execute the action.
    
    Returns
    -------
    selected_client : ``None | Client``
    """
    highest_client = None
    highest_role = None
    
    clients = guild.clients
    if (
        (client in clients) and
        ((guild.cached_permissions_for(client) & required_permission) == required_permission)
    ):
        highest_client = client
        highest_role = client.top_role_at(guild)
    
    for client_iterated in clients:
        if (
            (client_iterated is client) or
            ((guild.cached_permissions_for(client_iterated) & required_permission) != required_permission)
        ):
            continue
        
        highest_role_iterated = client_iterated.top_role_at(guild)
        if (highest_role is None) or ((highest_role_iterated is not None) and (highest_role_iterated > highest_role)):
            highest_client = client_iterated
            highest_role = highest_role_iterated
    
    return highest_client


def iter_select_client_with_shared_guild(user):
    """
    Iterate selects clients which share guild with the given user.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        User to select shared clients of.
    
    Yields
    ------
    client : ``Client``
    """
    produced_clients = None
    
    for guild in user.iter_guilds():
        for client in guild.clients:
            if (produced_clients is None) or (client not in produced_clients):
                yield client
            
            if (produced_clients is None):
                produced_clients = []
            
            produced_clients.append(client)
            continue


def parse_boolean_select_values(values, default):
    """
    Converts boolean select values to a boolean.
    
    Parameters
    ----------
    values : `None | tuple<str>`
        The selected value(s).
    
    default : `bool`
        Default value to return if none is received.
    
    Returns
    -------
    value : `bool`
    """
    if values is None:
        value = default
    else:
        value = values[0] == '1'
    
    return value


def process_reason(reason):
    """
    Cuts the end down of a reason if too long.
    
    Parameters
    ----------
    reason : `None | str`
        The reason to validate.
    
    Returns
    -------
    reason : `None | str`
    """
    if (reason is not None) and (len(reason) > REASON_ALLOWED_LENGTH_THRESHOLD):
        reason = reason[:REASON_ALLOWED_LENGTH_THRESHOLD] + ' ...'
    
    return reason


def build_reason(user, guild_id, reason):
    """
    Auto creates action reason if not given.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The invoking user.
    
    guild_id : `int`
        The local guild's identifier.
    
    reason : `None | str`
        Reason given.
    
    Returns
    -------
    reason : `str`
    """
    reason_parts = []
    if (reason is not None):
        reason_parts.append(reason)
        reason_parts.append('\n')
    
    reason_parts.append('Requested by: ')
    reason_parts.append(user.name_at(guild_id))
    reason_parts.append(' [')
    reason_parts.append(str(user.id))
    reason_parts.append(']')
    
    return ''.join(reason_parts)


async def try_notify_user(client, user, components):
    """
    Notifies the user about the action in context.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    user : ``User``
        The user in context.
    
    components : ``list<Component>``
        Components to send.
    
    Returns
    -------
    notification_result_state : `int`
    """
    if user.bot:
        return NOTIFICATION_RESULT_STATE_SUCCESS
    
    try:
        channel = await client.channel_private_create(user)
    except ConnectionError:
        return NOTIFICATION_RESULT_STATE_FAILURE_CONNECTION_OR_SERVER_ISSUE
    
    except DiscordException as exception:
        if exception.code >= 500:
            return NOTIFICATION_RESULT_STATE_FAILURE_CONNECTION_OR_SERVER_ISSUE
        
        raise
    
    try:
        await client.message_create(
            channel,
            allowed_mentions = None,
            components = components,
        )
    except ConnectionError:
        return NOTIFICATION_RESULT_STATE_FAILURE_CONNECTION_OR_SERVER_ISSUE
    
    except DiscordException as exception:
        if exception.code >= 500:
            return NOTIFICATION_RESULT_STATE_FAILURE_CONNECTION_OR_SERVER_ISSUE
        
        if exception.code in (
            ERROR_CODES.cannot_message_user_0, # user has dm-s disallowed
            ERROR_CODES.cannot_message_user_1, # user has dm-s disallowed
        ):
            return NOTIFICATION_RESULT_STATE_FAILURE_DMS_CLOSED
        
        raise
    
    return NOTIFICATION_RESULT_STATE_SUCCESS


async def get_source_user_from_client_entry(entry):
    """
    Gets the source invoker user if the client executed an action.
    
    This function is a coroutine.
    
    Parameters
    ----------
    entry : ``AuditLogEntry``
        The entry to inspect.
    
    Returns
    -------
    source_user : ``None | ClientUserBase``
    """
    reason = entry.reason
    if (reason is None):
        return None
    
    match = REASON_PATTERN.fullmatch(reason)
    if match is None:
        return None
    
    user_id = int(match.group(2))
    return await get_user(user_id)


def get_integer_length(value):
    """
    Gets an integer's length.
    
    Parameters
    ----------
    value : `int`
        The value to get its length of.
    
    Returns
    -------
    length : `int`
    """
    if not value:
        return 1
    
    return floor(log10(value)) + 1
