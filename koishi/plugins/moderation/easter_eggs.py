__all__ = ()

from datetime import datetime as DateTime, timedelta as TimeDelta, timezone as TimeZone
from random import random

from hata import AuditLogEntryType, DiscordException, ERROR_CODES, KOKORO
from scarletio import TaskGroup

from .constants import REASON_PATTERN


IMAGE_URL_NAZRIN = (
    'https://cdn.discordapp.com/attachments/568837922288173058/1258766702179782677/kyouko-nazrin-silencing.png'
)
IMAGE_URL_ORIN = (
    'https://cdn.discordapp.com/attachments/568837922288173058/1239516656099790868/orin-body-collecting.png'
)

ENTRY_TYPES_ORIN = (AuditLogEntryType.user_ban_add, AuditLogEntryType.user_kick)
AUDIT_LOG_INTERVAL_ORIN = TimeDelta(days = 7)

TIMEOUT_DURATION_MIN_NAZRIN = 7 * 86400 + 1


def should_show_nazrin(duration):
    """
    Returns whether Nazrin silencing Kyouko image should be shown.
    
    Parameters
    ----------
    duration : `TimeDelta`
        Timeout duration.
    
    Returns
    -------
    should_show_nazrin : `bool`
    """
    return duration >= TIMEOUT_DURATION_MIN_NAZRIN and random() > 0.5


async def should_show_orin(client, guild, user):
    """
    Returns whether the body collect image should be shown.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client with who the actions were executed.
    
    guild : ``Guild``
        The respective guild.
    
    user : ``ClientUserBase``
        The user who is checked.
    
    Returns
    -------
    should_show_orin : `bool`
    """
    count = await count_entries(client, guild, user, AUDIT_LOG_INTERVAL_ORIN, ENTRY_TYPES_ORIN)
    return count == 5


def is_entry_from_user(entry, user):
    """
    Returns whether the given entry was from the given user.
    
    Parameters
    ----------
    entry : ``AuditLogEntry``
        The audit log entry to check.
    
    user : ``ClientUserBase``
        The respective user.
    
    Returns
    -------
    is_entry_from_user : `bool`
    """
    # If the user banned
    if entry.user_id == user.id:
        return True
    
    # If the client banned
    reason = entry.reason
    if (reason is None):
        return False
    
    match = REASON_PATTERN.fullmatch(reason)
    if match is None:
        return False
    
    return int(match.group(2)) == user.id


async def count_entries(client, guild, user, audit_log_interval, entry_types):
    """
    Countries entries which where executed by the given user.
    
    Parameters
    ----------
    client : ``Client``
        The client with who the actions were executed.
    
    guild : ``Guild``
        The respective guild.
    
    user : ``ClientUserBase``
        The user who is checked.
    
    audit_log_interval : `TimeDelta`
        The maximal amount of delta to look backwards.
    
    entry_types : ``tuple<AuditLogEntryType>``
        Audit log entry types to request.
    
    Returns
    -------
    count : `int`
    """
    after = DateTime.now(TimeZone.utc) - audit_log_interval
    
    task_group = TaskGroup(KOKORO)
    for entry_type in entry_types:
        task_group.create_task(
            client.audit_log_get_chunk(guild, after = after, user = client, entry_type = entry_type)
        )
        task_group.create_task(
            client.audit_log_get_chunk(guild, after = after, user = user, entry_type = entry_type)
        )
    
    failed_task = await task_group.wait_exception()
    if (failed_task is not None):
        task_group.cancel_all()
        
        try:
            failed_task.get_result()
        except ConnectionError:
            return False
        
        except DiscordException as err:
            if err.code in (
                ERROR_CODES.missing_access, # client removed
                ERROR_CODES.missing_permissions, # permissions changed meanwhile
            ):
                return 0
            
            raise
    
    count = 0
    
    for task in task_group.done:
        audit_log = task.get_result()
        for entry in audit_log:
            count += is_entry_from_user(entry, user)
    
    return count
