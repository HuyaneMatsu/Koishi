__all__ = ()

from collections import deque
from itertools import chain

from hata import Client, KOKORO, parse_all_emojis
from scarletio import Task, WaitTillExc

from ..constants import ALLOWED_GUILDS, ROLE__MEDIA_SORTER
from ..helpers import create_webhook_message, get_message_and_files, get_webhook


SLASH_CLIENT: Client

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
    guild = event.message.guild
    if (guild is None) or (guild not in ALLOWED_GUILDS):
        return
    
    emoji = event.emoji
    if emoji.is_custom_emoji():
        return
    
    source_channel = event.message.channel
    if source_channel is None:
        return
    
    if source_channel.permissions_for(event.user).can_manage_messages:
        pass
    
    elif (guild.id == ROLE__MEDIA_SORTER.guild_id) and event.user.has_role(ROLE__MEDIA_SORTER):
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
        
        get_message_and_files_task = Task(get_message_and_files(client, source_channel, message.id), KOKORO)
        get_webhook_task = Task(get_webhook(client, channel_id), KOKORO)
        
        done, pending = await WaitTillExc(
            [
                get_message_and_files_task,
                get_webhook_task,
            ],
            KOKORO,
        )
        
        for task in pending:
            task.cancel()
        
        for task in done:
            result = task.result()
            
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
