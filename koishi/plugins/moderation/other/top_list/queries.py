__all__ = ()

from datetime import datetime as DateTime

from hata import AuditLogEntryType, Client, KOKORO
from scarletio import TaskGroup

from .action_counter import ActionCounter
from .constants import DELTA_DAY, SORT_KEYS_BY_TYPE, SORT_KEY_ALL, TYPE_BAN, TYPE_KICK, TYPE_MUTE
from .helpers import get_source_user_from_client_entry


async def request_bans(client, guild, after, actions):
    """
    Requests all the bans after the given time.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client to request the audit logs with.
    guild : ``Guild``
        The guild to request the actions at.
    after : `DateTime`
        The date to get the logs after.
    actions : `set` of `tuple` (`int`, ``ClientUserBase``, ``ClientUserBase``)
        The executed actions to extend.
    """
    async for audit_log_entry in (await client.audit_log_iterator(guild, event = AuditLogEntryType.user_ban_add)):
        if audit_log_entry.created_at < after:
            break
        
        source_user = audit_log_entry.user
        if source_user is None:
            continue
        
        if source_user is client:
            source_user = await get_source_user_from_client_entry(audit_log_entry)
            if source_user is None:
                continue
        
        elif source_user.bot:
            continue
        
        target_user = audit_log_entry.target
        if source_user is target_user:
            continue
        
        actions.add((TYPE_BAN, source_user, target_user))


async def request_kicks(client, guild, after, actions):
    """
    Requests all the kicks after the given time.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client to request the audit logs with.
    guild : ``Guild``
        The guild to request the actions at.
    after : `DateTime`
        The date to get the logs after.
    actions : `set` of `tuple` (`int`, ``ClientUserBase``, ``ClientUserBase``)
        The executed actions to extend.
    """
    async for audit_log_entry in (await client.audit_log_iterator(guild, event = AuditLogEntryType.member_kick)):
        if audit_log_entry.created_at < after:
            break
        
        source_user = audit_log_entry.user
        if source_user is None:
            continue
        
        if source_user is client:
            source_user = await get_source_user_from_client_entry(audit_log_entry)
            if source_user is None:
                continue
        
        elif source_user.bot:
            continue
        
        target_user = audit_log_entry.target
        if source_user is target_user:
            continue
        
        actions.add((TYPE_KICK, source_user, target_user))


async def request_mutes(client, guild, after, actions):
    """
    Requests all the mutes after the given time.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client to request the audit logs with.
    guild : ``Guild``
        The guild to request the actions at.
    after : `DateTime`
        The date to get the logs after.
    actions : `set` of `tuple` (`int`, ``ClientUserBase``, ``ClientUserBase``)
        The executed actions to extend.
    """
    async for audit_log_entry in (await client.audit_log_iterator(guild, event = AuditLogEntryType.member_update)):
        if audit_log_entry.created_at < after:
            break
        
        changes = audit_log_entry.changes
        if (changes is None):
            continue
            
        for change in changes:
            if change.attribute_name == 'timed_out_until':
                break
        else:
            continue
        
        if change.after is None:
            continue
        
        source_user = audit_log_entry.user
        if source_user is None:
            continue
        
        if source_user is client:
            source_user = await get_source_user_from_client_entry(audit_log_entry)
            if source_user is None:
                continue
        
        elif source_user.bot:
            continue
        
        target_user = audit_log_entry.target
        if source_user is target_user:
            continue
        
        actions.add((TYPE_MUTE, source_user, target_user))


async def request_actions(client, guild, after):
    """
    Requests the actions for the given action type in the given interva
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client to request the audit logs with.
    guild : ``Guild``
        The guild to request the actions at.
    after : `DateTime`
        The date to get the logs after.
    
    Returns
    -------
    actions : `set` of `tuple` (`int`, ``ClientUserBase``, ``ClientUserBase``)
        A set of `action type` - `source user` - `target user` tuples.
    """
    actions = set()
    
    task_group = TaskGroup(KOKORO)
    task_group.create_task(request_bans(client, guild, after, actions))
    task_group.create_task(request_kicks(client, guild, after, actions))
    task_group.create_task(request_mutes(client, guild, after, actions))
    
    failed_task = await task_group.wait_exception()
    if (failed_task is not None):
        task_group.cancel_all()
        failed_task.get_result()
    
    return actions


async def request_top_list(client, guild, sort_by, days):
    """
    Requests raw moderation top-list for the given guild.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client to request the audit logs with.
    guild : ``Guild``
        The guild to request the actions at.
    sort_by : `int`
        The field's identifier to sort by.
    days : `int`
        The amount of days to request.
    
    Returns
    -------
    top_list : `list` of `tuple` (``ClientUserBase``, ``ActionCounter``)
    """
    actions = await request_actions(client, guild, DateTime.utcnow() - (DELTA_DAY * days))
    
    by_user = {}
    for action in actions:
        source_user = action[1]
        
        try:
            counter = by_user[source_user]
        except KeyError:
            counter = ActionCounter()
            by_user[source_user] = counter
        
        counter.increment_with(action[0])
    
    return sorted(
        by_user.items(),
        key = SORT_KEYS_BY_TYPE.get(sort_by, SORT_KEY_ALL),
        reverse = True,
    )
