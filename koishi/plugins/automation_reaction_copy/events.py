__all__ = ()

from collections import deque
from itertools import chain

from hata import KOKORO, parse_all_emojis
from scarletio import Task, TaskGroup

from ...bots import SLASH_CLIENT

from ..automation_core import get_reaction_copy_enabled
from ..move_message_core import create_webhook_message, get_message_and_files, get_webhook


ACTION_QUEUE = deque(maxlen = 100)


def check_channel_emojis(channel, emoji):
    """
    Returns whether the channel has the given emoji in it.
    
    Parameters
    ----------
    channel : ``Channel``
        The channel to check.
    emoji : ``Emoji``
        The emoji to find.
    
    Returns
    -------
    """
    if not channel.is_in_group_guild_textual():
        return False
    
    if emoji in parse_all_emojis(channel.name):
        return True
    
    topic = channel.topic
    if (topic is not None) and (emoji in parse_all_emojis(topic)):
        return True
    
    return False


@SLASH_CLIENT.events
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
    
    emoji = event.emoji
    if emoji.is_custom_emoji():
        return
    
    if not get_reaction_copy_enabled(guild.id):
        return
    
    source_channel = event.message.channel
    if source_channel is None:
        return
    
    if source_channel.permissions_for(event.user).can_manage_messages:
        pass
    
    else:
        return
    
    target_channels = [
        channel for channel
        in chain(guild.channels.values(), guild.threads.values())
        if check_channel_emojis(channel, emoji)
    ]
    if len(target_channels) != 1:
        return
    
    target_channel = target_channels[0]
    if target_channel is source_channel:
        return
    
    # If the user does not have permissions in the target channel they should not be able to target it.
    if not target_channel.permissions_for(event.user).can_manage_messages:
        return
    
    if not target_channel.cached_permissions_for(client).can_manage_webhooks:
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
