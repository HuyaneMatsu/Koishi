__all__ = (
    'get_or_create_automation_reaction_role_entry', 'get_automation_reaction_role_entry_and_sync',
    'get_automation_reaction_role_entry_listing_and_sync_page',
)

from scarletio import Future, Task
from hata import DiscordException, ERROR_CODES, KOKORO, ROLES

from .automation_reaction_role_entry import AutomationReactionRoleEntry
from .constants import (
    AUTOMATION_REACTION_ROLE_BY_GUILD_ID, AUTOMATION_REACTION_ROLE_BY_MESSAGE_ID, ENTRIES_MAX, ENTRY_PAGE_SIZE,
    MESSAGE_SYNC_RESULT_DELETED, MESSAGE_SYNC_RESULT_SUCCESS, MESSAGE_SYNC_RESULT_TEMPORARY_FAILURE, MESSAGE_SYNC_TASKS
)
from .queries import query_delete_automation_reaction_role_entry, query_save_automation_reaction_role_entry


async def get_or_create_automation_reaction_role_entry(message):
    """
    Gets the auto react role entry for the given message. If it does not exist, creates it.
    
    This function is a coroutine.
    
    Parameters
    ----------
    message : ``Message``
        Message to get auto react role entry for.
        It is expected that this message is already well cached.
    
    Returns
    -------
    automation_reaction_role_entry_and_page_index : ``(None | AutoreactRoleEntry, int)``
        Returns `automation_reaction_role_entry` as `None` if the auto react role entry cannot be created.
        Also returns the page's identifier to which the auto react role entry belongs to.
    """
    try:
        automation_reaction_role_entry_listing = AUTOMATION_REACTION_ROLE_BY_GUILD_ID[message.guild_id]
    except KeyError:
        page_index = 0
    
    else:
        if len(automation_reaction_role_entry_listing) >= ENTRIES_MAX:
            return (None, 0)
        
        for index, automation_reaction_role_entry in enumerate(automation_reaction_role_entry_listing):
            if automation_reaction_role_entry.message is message:
                automation_reaction_role_entry.message_cached = True
                return automation_reaction_role_entry, index // ENTRY_PAGE_SIZE
        
        page_index = (
            0
            if automation_reaction_role_entry_listing is None else
            max((len(automation_reaction_role_entry_listing) - 1) // ENTRY_PAGE_SIZE, 0)
        )
    
    automation_reaction_role_entry = AutomationReactionRoleEntry(message)
    await query_save_automation_reaction_role_entry(automation_reaction_role_entry)
    return automation_reaction_role_entry, page_index


async def _message_sync_task(automation_reaction_role_entry, futures):
    """
    Internal task to sync sync a message.
    
    Parameters
    ----------
    automation_reaction_role_entry : ``AutomationReactionRoleEntry``
        The auto react role entry to sync.
    
    futures : ``Futures``
        The futures to set result of.
    """
    try:
        # We retry if we hit a permission error.
        last_client = None
        while True:
            for client in automation_reaction_role_entry.message.channel.iter_clients():
                break
            else:
                await query_delete_automation_reaction_role_entry(automation_reaction_role_entry)
                sync_result = MESSAGE_SYNC_RESULT_DELETED
                break
            
            if client is last_client:
                await query_delete_automation_reaction_role_entry(automation_reaction_role_entry)
                sync_result = MESSAGE_SYNC_RESULT_DELETED
                break
            
            try:
                await client.message_get(automation_reaction_role_entry.message)
            except ConnectionError:
                sync_result = MESSAGE_SYNC_RESULT_TEMPORARY_FAILURE
                break
            
            except DiscordException as exception:
                if exception.status >= 500:
                    sync_result = MESSAGE_SYNC_RESULT_TEMPORARY_FAILURE
                    break
                
                # Deleted.
                if exception.code in (
                    ERROR_CODES.unknown_message, # message deleted
                    ERROR_CODES.unknown_channel, # message's channel deleted
                ):
                    await query_delete_automation_reaction_role_entry(automation_reaction_role_entry)
                    sync_result = MESSAGE_SYNC_RESULT_DELETED
                    break
                
                # Retry cases
                if exception.code in (
                    ERROR_CODES.missing_access, # client removed
                    ERROR_CODES.missing_permissions, # permissions changed meanwhile
                ):
                    continue
                
                raise
            
            automation_reaction_role_entry.message_cached = True
            sync_result = MESSAGE_SYNC_RESULT_SUCCESS
            break
    
    except GeneratorExit:
        for future in futures:
            future.cancel()
        raise
    
    except BaseException as exception:
        for future in futures:
            future.set_exception_if_pending(exception)
    
    else:
        for future in futures:
            future.set_result_if_pending(sync_result)
        
    finally:
        try:
            del MESSAGE_SYNC_TASKS[automation_reaction_role_entry.message.id]
        except KeyError:
            pass
    
    for future in futures:
        future.set_result_if_pending(0)


async def _sync_automation_reaction_role_entry_message(automation_reaction_role_entry):
    """
    Syncs a singular auto react role entry.
    
    This function is a coroutine.
    
    Parameters
    ----------
    automation_reaction_role_entry : ``AutomationReactionRoleEntry``
        The entry to sync.
    
    Returns
    -------
    sync_result : `int`
    """
    if automation_reaction_role_entry.message_cached:
        return MESSAGE_SYNC_RESULT_SUCCESS
    
    try:
        item = MESSAGE_SYNC_TASKS[automation_reaction_role_entry.message.id]
    except KeyError:
        futures = []
        MESSAGE_SYNC_TASKS[automation_reaction_role_entry.message.id] = (
            Task(KOKORO, _message_sync_task(automation_reaction_role_entry, futures)),
            futures,
        )
    
    else:
        futures = item[1]
    
    future = Future(KOKORO)
    futures.append(future)
    
    return (await future)


async def get_automation_reaction_role_entry_and_sync(message_id):
    """
    Gets the auto react role entry for the given message identifier and syncs its message.
    
    This function is a coroutine.
    """
    try:
        automation_reaction_role_entry_listing = AUTOMATION_REACTION_ROLE_BY_MESSAGE_ID[message_id]
    except KeyError:
        return None
    
    message_sync_state = await _sync_automation_reaction_role_entry_message(automation_reaction_role_entry_listing)
    if (message_sync_state == MESSAGE_SYNC_RESULT_DELETED):
        return None
    
    return automation_reaction_role_entry_listing


async def get_automation_reaction_role_entry_listing_and_sync_page(guild_id, page_index):
    """
    Gets the auto react role entries for the given guild identifier and syncs the ones that belong to the given
    `page_index`.
    
    This function is a coroutine.
    
    Parameters
    ----------
    guild_id : `int`
        The guild identifier.
    
    page_index : `int`
        Page index.
    
    Returns
    -------
    automation_reaction_role_entry_listing : ``None | list<AutoreactRoleEntry>``
    """
    try:
        automation_reaction_role_entry_listing = AUTOMATION_REACTION_ROLE_BY_GUILD_ID[guild_id]
    except KeyError:
        return None
    
    index = page_index * ENTRY_PAGE_SIZE
    target_end = index + ENTRY_PAGE_SIZE
    
    while index < min(target_end, len(automation_reaction_role_entry_listing)):
        message_sync_state = await _sync_automation_reaction_role_entry_message(
            automation_reaction_role_entry_listing[index]
        )
        if (
            (message_sync_state == MESSAGE_SYNC_RESULT_SUCCESS) or
            (message_sync_state == MESSAGE_SYNC_RESULT_TEMPORARY_FAILURE)
        ):
            index += 1
        continue
    
    if not automation_reaction_role_entry_listing:
        automation_reaction_role_entry_listing = None
    
    return automation_reaction_role_entry_listing


def _iter_user_roles(user, guild_id):
    """
    Iterates over the user's roles.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user to iterate over its roles of.
    
    guild_id : `int`
        The guild's identifier.
    
    Yields
    ------
    role : ``Role``
    """
    try:
        guild_profile = user.guild_profiles[guild_id]
    except KeyError:
        return
    
    try:
        role = ROLES[guild_id]
    except KeyError:
        pass
    else:
        yield role
    
    role_ids = guild_profile.role_ids
    if (role_ids is None):
        return
    
    for role_id in role_ids:
        try:
            role = ROLES[role_id]
        except KeyError:
            pass
        else:
            yield role


def get_highest_client_with_role(guild):
    """
    Gets the highest client in the guild and their top role.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild get the best match for.
    
    Returns
    -------
    highest_client_with_role : ``None | (Client, Role)``
    """
    if guild is None:
        return None
    
    best_client = None
    best_client_role = None
    
    for client in guild.clients:
        manage_roles = 0
        highest_role = None
        
        for role in _iter_user_roles(client, guild.id):
            manage_roles |= role.permissions.manage_roles
            if (highest_role is None) or (role > highest_role):
                highest_role = role
        
        if not manage_roles:
            continue
        
        if (best_client is None) or (highest_role > best_client_role):
            best_client = client
            best_client_role = highest_role
    
    if best_client is None:
        return None
    
    return best_client, best_client_role


def get_automation_reaction_role_item_with_emoji_id(automation_reaction_role_entry, emoji_id):
    """
    Gets the auto react role item with teh given emoji identifier.
    
    Parameters
    ----------
    automation_reaction_role_entry : ``AutomationReactionRoleEntry``
        The auto react role entry to query from.
    
    emoji_id : `int`
        The emoji's identifier.
    
    Returns
    -------
    automation_reaction_role_item : ``None | AutomationReactionRoleItem``
    """
    automation_reaction_role_items = automation_reaction_role_entry.items
    if (automation_reaction_role_items is not None):
        for automation_reaction_role_item in automation_reaction_role_items:
            if automation_reaction_role_item.emoji_id == emoji_id:
                return automation_reaction_role_item


def iter_role_ids_of_roles_nullable(roles):
    """
    Iterates over the given roles' identifiers.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    roles : ``None | tuple<Role>``
        Roles to iterate through their items.
    
    Yields
    ------
    role_id : `int`
    """
    if (roles is not None):
        for role in roles:
            yield role.id


def iter_automation_reaction_role_entry_role_ids(automation_reaction_role_entry, role_ids_slot):
    """
    Iterates over the role ids of the given auto react role entry.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    automation_reaction_role_entry : ``AutomationReactionRoleEntry``
        The auto react role entry to query from.
    
    role_ids_slot : `GetSetDescriptorType | MemberDescriptorType`
        The slot of the entry to get the role identifies for.
    
    Yields
    ------
    role_id : `int`
    """
    automation_reaction_role_items = automation_reaction_role_entry.items
    if (automation_reaction_role_items is not None):
        for automation_reaction_role_item in automation_reaction_role_items:
            role_ids = role_ids_slot.__get__(automation_reaction_role_item, type(automation_reaction_role_item))
            if (role_ids is not None):
                yield from role_ids
    

def iter_automation_reaction_role_entry_role_ids_excluding_item(
    automation_reaction_role_entry, role_ids_slot, excluded_automation_reaction_role_item
):
    """
    Iterates over the role ids of the given auto react role entry.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    automation_reaction_role_entry : ``AutomationReactionRoleEntry``
        The auto react role entry to query from.
    
    role_ids_slot : `GetSetDescriptorType | MemberDescriptorType`
        The slot of the entry to get the role identifies for.
    
    excluded_automation_reaction_role_item : ``AutomationReactionRoleItem``
        The item to exclude.
    
    Yields
    ------
    role_id : `int`
    """
    automation_reaction_role_items = automation_reaction_role_entry.items
    if (automation_reaction_role_items is not None):
        for automation_reaction_role_item in automation_reaction_role_items:
            if automation_reaction_role_item is not excluded_automation_reaction_role_item:
                role_ids = role_ids_slot.__get__(automation_reaction_role_item, type(automation_reaction_role_item))
                if (role_ids is not None):
                    yield from role_ids
