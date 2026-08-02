__all__ = ()

from datetime import datetime as DateTime, timedelta as TimeDelta, timezone as TimeZone

from hata import AuditLogEntryType, CLIENTS, Client, KOKORO
from scarletio import TaskGroup

from .constants import (
    ACTION_TYPE_BAN, ACTION_TYPE_KICK, ACTION_TYPE_MUTE, TOP_LIST_SORT_KEYS_BY_TYPE, TOP_LIST_SORT_KEY_ALL
)
from .helpers import get_source_user_from_client_entry
from .top_list_action_counter import TopListActionCounter, top_list_action_counter_increment_with


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
    
    actions : ``set<(int, ClientUserBase, ClientUserBase)>``
        The executed actions to extend.
    """
    async for audit_log_entry in (await client.audit_log_iterator(guild, entry_type = AuditLogEntryType.user_ban_add)):
        if audit_log_entry.created_at < after:
            break
        
        source_user = audit_log_entry.user
        if source_user is None:
            continue
        
        if source_user.id in CLIENTS:
            source_user = await get_source_user_from_client_entry(audit_log_entry)
            if source_user is None:
                continue
        
        elif source_user.bot:
            continue
        
        target_user = audit_log_entry.target
        if source_user is target_user:
            continue
        
        actions.add((ACTION_TYPE_BAN, source_user, target_user))


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
    
    actions : ``set<(int, ClientUserBase, ClientUserBase)>``
        The executed actions to extend.
    """
    async for audit_log_entry in (await client.audit_log_iterator(guild, entry_type = AuditLogEntryType.user_kick)):
        if audit_log_entry.created_at < after:
            break
        
        source_user = audit_log_entry.user
        if source_user is None:
            continue
        
        if source_user.id in CLIENTS:
            source_user = await get_source_user_from_client_entry(audit_log_entry)
            if source_user is None:
                continue
        
        elif source_user.bot:
            continue
        
        target_user = audit_log_entry.target
        if source_user is target_user:
            continue
        
        actions.add((ACTION_TYPE_KICK, source_user, target_user))


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
    
    actions : ``set<(int, ClientUserBase, ClientUserBase)>``
        The executed actions to extend.
    """
    async for audit_log_entry in (await client.audit_log_iterator(guild, entry_type = AuditLogEntryType.user_update)):
        if audit_log_entry.created_at < after:
            break
        
        change = audit_log_entry.get_change('timed_out_until')
        if change is None:
            continue
        
        if change.after is None:
            continue
        
        source_user = audit_log_entry.user
        if source_user is None:
            continue
        
        if source_user.id in CLIENTS:
            source_user = await get_source_user_from_client_entry(audit_log_entry)
            if source_user is None:
                continue
        
        elif source_user.bot:
            continue
        
        target_user = audit_log_entry.target
        if source_user is target_user:
            continue
        
        actions.add((ACTION_TYPE_MUTE, source_user, target_user))


async def request_actions(client, guild, after):
    """
    Requests the actions for the given action type in the given interval.
    
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
    actions : ``set<(int, ClientUserBase, ClientUserBase)>``
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
    top_list : ``list<(ClientUserBase, TopListActionCounter)>
    """
    actions = await request_actions(client, guild, DateTime.now(TimeZone.utc) - TimeDelta(seconds = 86400 * days))
    
    by_user = {}
    for action in actions:
        source_user = action[1]
        
        try:
            counter = by_user[source_user]
        except KeyError:
            counter = TopListActionCounter()
            by_user[source_user] = counter
        
        top_list_action_counter_increment_with(counter, action[0])
    
    return sorted(
        by_user.items(),
        key = TOP_LIST_SORT_KEYS_BY_TYPE.get(sort_by, TOP_LIST_SORT_KEY_ALL),
        reverse = True,
    )
