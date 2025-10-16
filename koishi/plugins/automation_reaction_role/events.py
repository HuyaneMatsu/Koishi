__all__ = ()

from hata import DiscordException, ERROR_CODES, GUILDS
from ...bots import FEATURE_CLIENTS

from .constants import AUTOMATION_REACTION_ROLE_BY_GUILD_ID, AUTOMATION_REACTION_ROLE_BY_MESSAGE_ID
from .helpers import get_highest_client_with_role
from .queries import (
    query_delete_automation_reaction_role_entry_listing, query_delete_automation_reaction_role_entry,
    query_update_automation_reaction_role_entry
)

async def _handle_reaction_event(client, event, addition):
    """
    Handles a reaction add or remove event.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the message.
    
    event : ``ReactionAddEvent``
        The received interaction action.
    
    addition : `bool`
        Whether the add role should be added and remove roles should be removed, or the other way around.
    """
    if event.user.bot:
        return
    
    # Check whether we are the first client who should be receiving this event.
    for iterated_client in event.message.channel.iter_clients():
        if (iterated_client not in FEATURE_CLIENTS):
            continue
        
        if (iterated_client is iterated_client):
            break
        
        return
    
    else:
        return
    
    while True:
        role_ids_and_to_add_and_to_remove = get_user_new_role_ids(event, addition)
        if role_ids_and_to_add_and_to_remove is None:
            return
        
        role_ids, to_add_role_ids, to_remove_role_ids = role_ids_and_to_add_and_to_remove
        
        highest_client_with_role = get_highest_client_with_role(event.message.guild)
        if (highest_client_with_role is not None):
            client = highest_client_with_role[0]
        
        try:
            # If the role difference count is high, modify the user's profile, if not, either add or delete the roles.
            if (
                (
                    (0 if to_add_role_ids is None else len(to_add_role_ids)) +
                    (0 if to_remove_role_ids is None else len(to_remove_role_ids))
                ) > 2
            ):
                if (to_add_role_ids is not None):
                    role_ids.update(to_add_role_ids)
                
                if (to_remove_role_ids is not None):
                    role_ids.difference_update(to_remove_role_ids)
                
                await client.user_guild_profile_edit(
                    event.message.guild_id,
                    event.user,
                    role_ids = role_ids,
                )
            
            else:
                if (to_add_role_ids is not None):
                    for role_id in to_add_role_ids:
                        await client.user_role_add(event.user, (event.message.guild_id, role_id))
                
                if (to_remove_role_ids is not None):
                    for role_id in to_remove_role_ids:
                        await client.user_role_delete(event.user, (event.message.guild_id, role_id))
        
        except ConnectionError:
            return
        
        except DiscordException as exception:
            if exception.status >= 500:
                return
            
            if exception.code == ERROR_CODES.missing_access:
                await _delete_automation_reaction_role_entry_by_message_id_if_exists(event.message.id)
                return
            
            if exception.code == ERROR_CODES.missing_permissions:
                await _update_or_delete_automation_reaction_role_entries(
                    event.message.guild_id,
                    event.message.id,
                    (None if highest_client_with_role is None else highest_client_with_role[1]),
                )
                continue
            
            raise
        
        return


@FEATURE_CLIENTS.events
async def reaction_add(client, event):
    """
    Called when a reaction added is on a message.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the message.
    
    event : ``ReactionAddEvent``
        The received interaction action.
    """
    await _handle_reaction_event(client, event, True)


@FEATURE_CLIENTS.events
async def reaction_delete(client, event):
    """
    Called when a reaction added is on a message.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the message.
    
    event : ``ReactionDeleteEvent``
        The received interaction action.
    """
    await _handle_reaction_event(client, event, False)


def get_user_new_role_ids(event, addition):
    """
    Gets the user's new role ids.
    
    Parameters
    ----------
    event : ``ReactionAddEvent``
        Received event.
    
    addition : `bool`
        Whether the add role should be added and remove roles should be removed, or the other way around.
    
    Returns
    -------
    role_ids_and_to_add_and_to_remove : `None | (set<int>, None | list<int>, None | list<int>)`
    """
    try:
        automation_reaction_role_entry = AUTOMATION_REACTION_ROLE_BY_MESSAGE_ID[event.message.id]
    except KeyError:
        return
    
    try:
        guild_profile = event.user.guild_profiles[event.message.guild_id]
    except KeyError:
        return
    
    automation_reaction_role_items = automation_reaction_role_entry.items
    if automation_reaction_role_items is None:
        return
    
    emoji_id = event.emoji.id
    
    for automation_reaction_role_item in automation_reaction_role_items:
        if automation_reaction_role_item.emoji_id == emoji_id:
            break
    else:
        return
    
    add_role_ids = automation_reaction_role_item.add_role_ids
    remove_role_ids = automation_reaction_role_item.remove_role_ids
    if (add_role_ids is None) and (remove_role_ids is None):
        return
    
    role_ids = {*guild_profile.iter_role_ids()}
    to_add_role_ids = None
    to_remove_role_ids = None
    
    if not addition:
        add_role_ids, remove_role_ids = remove_role_ids, add_role_ids
    
    if (add_role_ids is not None):
        for role_id in add_role_ids:
            if (role_id in role_ids):
                continue
            
            if to_add_role_ids is None:
                to_add_role_ids = []
            
            to_add_role_ids.append(role_id)
            continue
    
    if (remove_role_ids is not None):
        for role_id in remove_role_ids:
            if (role_id not in role_ids):
                continue
            
            if to_remove_role_ids is None:
                to_remove_role_ids = []
            
            to_remove_role_ids.append(role_id)
            continue
    
    if (to_add_role_ids is None) and (to_remove_role_ids is None):
        return
    
    return role_ids, to_add_role_ids, to_remove_role_ids


async def _update_automation_reaction_role_entries_by_excluding_role_ids(guild_id, role_ids_to_exclude):
    """
    Updates auto react role entries by excluding role identifiers.
    
    This function is a coroutine.
    
    Parameters
    ----------
    guild_id : `int`
        Guild identifier.
    
    role_ids_to_exclude : `set<int>`
        The roles' identifier to exclude.
    
    Returns
    -------
    success : `bool`
    """
    try:
        automation_reaction_role_entries = AUTOMATION_REACTION_ROLE_BY_GUILD_ID[guild_id]
    except KeyError:
        return False
    
    for automation_reaction_role_entry in automation_reaction_role_entries.copy():
        if exclude_roles_from_automation_reaction_role_entry(automation_reaction_role_entry, role_ids_to_exclude):
            await query_update_automation_reaction_role_entry(automation_reaction_role_entry)
    
    return True


async def _update_or_delete_automation_reaction_role_entries(guild_id, message_id, highest_role):
    """
    Updates or deletes the auto react role entries with the given configuration.
    
    This function is a coroutine.
    
    Parameters
    ----------
    guild_id : `int`
        Guild identifier.
    
    guild_id : `int`
        Message identifier.
    
    highest_role : ``None | Role``
        The higher role a competent client holds.
    
    Returns
    -------
    success : `bool`
    """
    guild = GUILDS.get(guild_id, None)
    if (guild is None) or (highest_role is None):
        if await _delete_automation_reaction_role_entry_by_guild_id_if_exists(guild_id):
            return True
        
        if message_id and (await _delete_automation_reaction_role_entry_by_message_id_if_exists(message_id)):
            return True
        
    else: 
        if await _update_automation_reaction_role_entries_by_excluding_role_ids(
            guild_id,
            {role.id for role in guild.iter_roles() if role >= highest_role},
        ):
            return True
            
        if message_id and (await _delete_automation_reaction_role_entry_by_message_id_if_exists(message_id)):
            return True
    
    return False


@FEATURE_CLIENTS.events
async def role_delete(client, role):
    """
    Handles a role delete event.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received this event.
    
    role : ``Role``
        The deleted role.
    """
    # Check whether we are teh first client who should be receiving this event.
    guild = role.guild
    if (guild is not None):
        clients = guild.clients
        if clients and (client is not clients[0]):
            return
    
    highest_client_with_role = get_highest_client_with_role(role.guild)
    await _update_or_delete_automation_reaction_role_entries(
        role.guild_id,
        0,
        (None if highest_client_with_role is None else highest_client_with_role[1]),
    )


def _exclude_roles(role_ids, role_ids_to_exclude):
    """
    Helper function to exclude specific role identifiers.
    
    Parameters
    ----------
    role_ids : `None | tuple<int>`
        Role identifiers.
    
    role_ids_to_exclude : `set<int>`
        The roles' identifier to exclude.
    
    Returns
    -------
    new_role_ids : `None | tuple<int>`
    """
    if (role_ids is None):
        return None
    
    new_role_ids = [role_id for role_id in role_ids if role_id not in role_ids_to_exclude]
    if not new_role_ids:
        new_role_ids = None
    else:
        new_role_ids.sort()
        new_role_ids = tuple(new_role_ids)
    
    return new_role_ids


def exclude_roles_from_automation_reaction_role_entry(automation_reaction_role_entry, role_ids_to_exclude):
    """
    Applies ro deletion to the auto react role entry.
    
    Parameters
    ----------
    automation_reaction_role_entry : ``AutoreactRoleEntry``
        The auto react orle entry to update.
    
    role_ids_to_exclude : `set<int>`
        The roles' identifier to exclude.
    
    Returns
    -------
    updated : `bool`
    """
    automation_reaction_role_items = automation_reaction_role_entry.items
    if automation_reaction_role_items is None:
        return False
    
    modified = False
    
    for automation_reaction_role_item in automation_reaction_role_items:
        add_role_ids = automation_reaction_role_item.add_role_ids
        new_add_role_ids = _exclude_roles(add_role_ids, role_ids_to_exclude)
        if add_role_ids != new_add_role_ids:
            automation_reaction_role_item.add_role_ids = new_add_role_ids
            modified = True
        
        remove_role_ids = automation_reaction_role_item.remove_role_ids
        new_remove_role_ids = _exclude_roles(remove_role_ids, role_ids_to_exclude)
        if remove_role_ids != new_remove_role_ids:
            automation_reaction_role_item.remove_role_ids = new_remove_role_ids
            modified = True
    
    return modified


async def _delete_automation_reaction_role_entry_by_guild_id_if_exists(guild_id):
    """
    Deletes the auto react role entry by guild if it exists in cache.
    
    This function is a coroutine.
    
    Parameters
    ----------
    guild_id : `int`
        Guild identifier.
    
    Returns
    -------
    success : `bool`
    """
    try:
        automation_reaction_role_entries = AUTOMATION_REACTION_ROLE_BY_GUILD_ID[guild_id]
    except KeyError:
        return False
    
    await query_delete_automation_reaction_role_entry_listing(automation_reaction_role_entries.copy())
    return True


@FEATURE_CLIENTS.events
async def guild_delete(client, guild, client_guild_profile):
    """
    Handles a guild delete event.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received this event.
    
    guild : ``Guild``
        The deleted guild.
    
    client_guild_profile : ``None | GuildProfile``
        The client's guild profile that it had in the guild.
    """
    if guild.clients:
        return
    
    await _delete_automation_reaction_role_entry_by_guild_id_if_exists(guild.id)


@FEATURE_CLIENTS.events
async def channel_delete(client, channel):
    """
    Handles a channel delete event.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received this event.
    
    channel : ``Channel``
        The deleted channel.
    """
    channel_id = channel.id
    guild_id = channel.guild_id
    
    try:
        automation_reaction_role_entries = AUTOMATION_REACTION_ROLE_BY_GUILD_ID[guild_id]
    except KeyError:
        return
    
    to_delete = None
    
    for automation_reaction_role_entry in automation_reaction_role_entries:
        if automation_reaction_role_entry.message.channel_id != channel_id:
            continue
        
        if to_delete is None:
            to_delete = []
        
        to_delete.append(automation_reaction_role_entry)
        continue
    
    if to_delete is None:
        return
    
    await query_delete_automation_reaction_role_entry_listing(to_delete)


async def _delete_automation_reaction_role_entry_by_message_id_if_exists(message_id):
    """
    Deletes the auto react role entry by message if it exists in cache.
    
    This function is a coroutine.
    
    Parameters
    ----------
    message_id : `int`
        Message identifier.
    
    Returns
    -------
    success : `bool`
    """
    try:
        automation_reaction_role_entry = AUTOMATION_REACTION_ROLE_BY_MESSAGE_ID[message_id]
    except KeyError:
        return False
    
    await query_delete_automation_reaction_role_entry(automation_reaction_role_entry)
    return True


@FEATURE_CLIENTS.events
async def message_delete(client, message):
    """
    Handles a message delete event.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received this event.
    
    message : ``Message``
        The deleted message.
    """
    await _delete_automation_reaction_role_entry_by_message_id_if_exists(message.id)


@FEATURE_CLIENTS.events
async def guild_user_update(client, guild, user, old_attributes):
    """
    Handles a user guild profile update event.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    guild : ``Guild``
        The guild where the user was updated at.
    
    user : ``ClientUserBase``
        The updated user.
    
    old_attributes : `None | dict<str, object>`
        The user's guild profile's old attributes.
    """
    if client is not user:
        return
    
    if (old_attributes is not None) and (old_attributes.get('role_ids', None) is None):
        return
    
    highest_client_with_role = get_highest_client_with_role(guild)
    await _update_or_delete_automation_reaction_role_entries(
        guild.id,
        0,
        (None if highest_client_with_role is None else highest_client_with_role[1]),
    )


@FEATURE_CLIENTS.events
async def reaction_delete_emoji(client, message, emoji, removed_reactions):
    """
    Handles a reaction delete emoji.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    message : ``Message``
        The message that had a reaction emoji removed of it.
    
    emoji : ``Emoji``
        The removed emoji.
    
    removed_reactions : ``None | dict<Reaction, ReactionMappingLine>``
        The removed reactions.
    """
    try:
        automation_reaction_role_entry = AUTOMATION_REACTION_ROLE_BY_MESSAGE_ID[message.id]
    except KeyError:
        return
    
    automation_reaction_role_items = automation_reaction_role_entry.items
    if automation_reaction_role_items is None:
        return
    
    emoji_id = emoji.id
    
    for index, automation_reaction_role_item in enumerate(automation_reaction_role_items):
        if automation_reaction_role_item.emoji_id == emoji_id:
            break
    else:
        return
    
    del automation_reaction_role_items[index]
    if not automation_reaction_role_items:
        automation_reaction_role_entry.items = None
    
    await query_update_automation_reaction_role_entry(automation_reaction_role_entry)


@FEATURE_CLIENTS.events
async def reaction_clear(client, message, reactions):
    """
    Handles a reaction delete emoji.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    message : ``Message``
        The message that had reactions removed from it.
    
    reactions : ``None | ReactionMapping``
        The removed reactions.
    """
    try:
        automation_reaction_role_entry = AUTOMATION_REACTION_ROLE_BY_MESSAGE_ID[message.id]
    except KeyError:
        return
    
    automation_reaction_role_items = automation_reaction_role_entry.items
    if automation_reaction_role_items is None:
        return
    
    automation_reaction_role_entry.items = None
    await query_update_automation_reaction_role_entry(automation_reaction_role_entry)
