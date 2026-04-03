__all__ = ()

from datetime import datetime as DateTime, timezone as TimeZone

from scarletio import TaskGroup
from hata import DiscordException, ERROR_CODES, KOKORO

from ...shared_constants import REASON_RP


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
    
    match = REASON_RP.fullmatch(reason)
    if match is None:
        return False
    
    return int(match.group(1)) == user.id


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
    entry_types : `tuple<AuditLogEntryType>`
        Audit log entry types to request.
    
    Returns
    -------
    count : `int`
    """
    if not guild.cached_permissions_for(client).view_audit_logs:
        return 0
    
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
