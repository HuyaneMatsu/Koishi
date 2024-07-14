__all__ = ()

from collections import deque
from itertools import chain

from hata import KOKORO, Permission
from scarletio import Task, TaskGroup

from ...bots import FEATURE_CLIENTS

from ..automation_core import get_reaction_copy_fields
from ..blacklist_core import is_user_id_in_blacklist
from ..move_message_core import create_webhook_message, get_message_and_files, get_webhook

from .constants import MASK_PARSE_ANY_CUSTOM, MAKS_PARSE_ANY_UNICODE
from .list_channels import collect_channel_emojis

ACTION_QUEUE = deque(maxlen = 100)

PERMISSION_MASK_ROLE = Permission().update_by_keys(view_channel = True)
PERMISSION_MASK_DEFAULT = Permission().update_by_keys(manage_messages = True)


def check_is_emoji_allowed(emoji, flags):
    """
    Returns whether the emoji is allowed by the given flags.
    
    Parameters
    ----------
    emoji : ``Emoji``
        The emoji to check for.
    flags : `int`
        Bitwise flags to determine from where and what kind of emojis should we collect.
    
    Returns
    -------
    allowed : `bool`
    """
    if emoji.is_unicode_emoji():
        if flags & MAKS_PARSE_ANY_UNICODE:
            return True
    
    elif emoji.is_custom_emoji():
        if flags & MASK_PARSE_ANY_CUSTOM:
            return True
    
    return False


def check_has_channel_emoji(channel, emoji, flags):
    """
    Returns whether the channel has the given emoji in it.
    
    Parameters
    ----------
    channel : ``Channel``
        The channel to check.
    emoji : ``Emoji``
        The emoji to check for.
    flags : `int`
        Bitwise flags to determine from where and what kind of emojis should we collect.
    
    Returns
    -------
    has_emoji : `bool`
    """
    if not channel.is_in_group_guild_textual():
        return False
    
    if emoji in collect_channel_emojis(channel, flags):
        return True
    
    return False


def try_get_target_channel(guild, emoji, flags):
    """
    Tries to get the target channel from the guild.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild where reaction was added at.
    emoji : ``Emoji``
        The emoji to check for.
    flags : `int`
        Bitwise flags to determine from where and what kind of emojis should we collect.
    
    Returns
    -------
    target_channel : `None | Channel`
    """
    target_channels = [
        channel for channel
        in chain(guild.iter_channels(), guild.iter_threads())
        if check_has_channel_emoji(channel, emoji, flags)
    ]
    
    if len(target_channels) == 1:
        return target_channels[0]


@FEATURE_CLIENTS.events
async def reaction_add(client, event):
    """
    Handles a reaction-add event.
    
    This method is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received event.
    """
    guild = event.message.guild
    if (guild is None):
        return
    
    if event.user.bot or is_user_id_in_blacklist(event.user.id):
        return
    
    emoji = event.emoji
    if emoji.is_custom_emoji() and guild.id != emoji.guild_id:
        return
    
    source_channel = event.message.channel
    if source_channel is None:
        return
    
    reaction_copy_fields = get_reaction_copy_fields(guild.id)
    if reaction_copy_fields is None:
        return
    
    role, flags = reaction_copy_fields
    if not check_is_emoji_allowed(emoji, flags):
        return
    
    if (role is not None) and event.user.has_role(role):
        permission_mask = PERMISSION_MASK_ROLE
    else:
        permission_mask = PERMISSION_MASK_DEFAULT
        
    if source_channel.permissions_for(event.user) & permission_mask != permission_mask:
        return
    
    target_channel = try_get_target_channel(guild, emoji, flags)
    if (target_channel is None) or (target_channel is source_channel):
        return
    
    # If the user does not have permissions in the target channel they should not be able to target it.
    if target_channel.permissions_for(event.user) & permission_mask != permission_mask:
        return
    
    # Get the first client who satisfies the required permission requirements
    for client_to_use in guild.clients:
        if target_channel.cached_permissions_for(client_to_use).can_manage_webhooks:
            if client_to_use is client:
                break
    
    else:
        return
    
    message = event.message
    
    key = (message.id, target_channel.id)
    if key in ACTION_QUEUE:
        return
    
    ACTION_QUEUE.append(key)
    
    try:
        if target_channel.is_in_group_thread():
            channel_id = target_channel.parent_id
            thread_id = target_channel.id
        else:
            channel_id = target_channel.id
            thread_id = 0
        
        get_message_and_files_task = Task(KOKORO, get_message_and_files(client, source_channel, message.id))
        get_webhook_task = Task(KOKORO, get_webhook(client, channel_id))
        
        task_group =  TaskGroup(
            KOKORO,
            [
                get_message_and_files_task,
                get_webhook_task,
            ],
        )
        
        failed_task = await task_group.wait_exception()
        if (failed_task is not None):
            # Cancel all and propagate the first failing.
            task_group.cancel_all()
            failed_task.get_result()
            return
        
        for task in task_group.done:
            result = task.get_result()
            
            if task is get_message_and_files_task:
                message, files = result
                continue
            
            if task is get_webhook_task:
                webhook = result
                continue
        
        try:
            await create_webhook_message(client, webhook, message, thread_id, files)
        finally:
            files = None
    
    except:
        ACTION_QUEUE.remove(key)
        raise
