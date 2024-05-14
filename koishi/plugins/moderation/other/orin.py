__all__ = ()

from datetime import datetime as DateTime, timedelta as TimeDelta

from hata import AuditLogEntryType, Color, DiscordException, ERROR_CODES, KOKORO
from scarletio import TaskGroup

from ..shared_constants import REASON_RP


ORIN_IMAGE_URL = (
    'https://cdn.discordapp.com/attachments/568837922288173058/1239516656099790868/orin-body-collecting.png'
)
ORIN_COLOR = Color(0x9E4D4C)

ALLOWED_INTERVAL = TimeDelta(days = 7)


def apply_orin_mode(embed):
    """
    Applies orin mode to the given embed.
    
    Parameters
    ----------
    embed : ``Embed``
        The embed to orinify.
    """
    embed.add_image(ORIN_IMAGE_URL)
    embed.color = ORIN_COLOR


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


async def should_show_orin(client, guild, user):
    """
    Returns whether the body collect image should be shown at the given guild.
    
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
    if not guild.cached_permissions_for(client).can_view_audit_logs:
        return False
    
    after = DateTime.utcnow() - ALLOWED_INTERVAL
    
    task_group = TaskGroup(KOKORO)
    task_group.create_task(
        client.audit_log_get_chunk(guild, after = after, user = client, entry_type = AuditLogEntryType.user_kick)
    )
    task_group.create_task(
        client.audit_log_get_chunk(guild, after = after, user = client, entry_type = AuditLogEntryType.user_ban_add)
    )
    task_group.create_task(
        client.audit_log_get_chunk(guild, after = after, user = user, entry_type = AuditLogEntryType.user_kick)
    )
    task_group.create_task(
        client.audit_log_get_chunk(guild, after = after, user = user, entry_type = AuditLogEntryType.user_ban_add)
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
                return False
            
            raise
    
    count = 0
    
    for task in task_group.done:
        audit_log = task.get_result()
        for entry in audit_log:
            count += is_entry_from_user(entry, user)
    
    return count == 5
