__all__ = ()

import re
from datetime import datetime as DateTime, timedelta as TimeDelta

from hata import AuditLogEvent, Color, DiscordException, ERROR_CODES, ID_RP, KOKORO
from scarletio import Task


ORIN_IMAGE_URL = (
    'https://cdn.discordapp.com/attachments/568837922288173058/1043809753681371146/orin-body-collecting-meme-0001.png'
)
ORIN_COLOR = Color(0x9E4D4C)

ALLOWED_INTERVAL = TimeDelta(days = 7)

REASON_RP = re.compile(f'[\\s\\S]*\\[{ID_RP.pattern}\\]', re.M | re.U)


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
    
    task_request_kick = Task(
        client.audit_log_get_chunk(guild, after = after, user = client, event = AuditLogEvent.member_kick),
        KOKORO,
    )
    
    task_request_ban = Task(
        client.audit_log_get_chunk(guild, after = after, user = client, event = AuditLogEvent.member_ban_add),
        KOKORO,
    )
    
    count = 0
    
    try:
        for task in (task_request_kick, task_request_ban):
            audit_log = await task
            for entry in audit_log:
                count += is_entry_from_user(entry, user)
            
    except BaseException as err:
        # Cancel tasks if unexpected exception occurs.
        for task in (task_request_kick, task_request_ban):
            task.cancel()
        
        if isinstance(err, ConnectionError):
            return False
        
        if isinstance(err, DiscordException) and err.code in (
            ERROR_CODES.missing_access, # client removed
            ERROR_CODES.missing_permissions, # permissions changed meanwhile
        ):
            return False
        
        raise
    
    return count == 5
