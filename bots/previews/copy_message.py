__all__ = ()


from scarletio import Task, WaitTillExc
from hata import Client, DiscordException, ERROR_CODES, KOKORO
from hata.ext.slash import abort
from bot_utils.constants import ROLE__SUPPORT__TESTER, GUILD__SUPPORT

SLASH_CLIENT: Client

async def get_message(client, channel, message_id):
    try:
        message = await client.message_get((channel.id, message_id))
    except DiscordException as err:
        if err.code == ERROR_CODES.unknown_message:
            abort(f'Unknown message: {message_id}')
        
        raise
    
    return message


async def get_attachment(client, attachment):
    file = await client.download_attachment(attachment)
    return attachment, file


async def get_attachments(client, attachments):
    tasks = []
    for attachment in attachments:
        tasks.append(Task(get_attachment(client, attachment), KOKORO))
    
    done, pending = await WaitTillExc(tasks, KOKORO)
    
    # We do not care about the pending ones
    for task in pending:
        task.cancel()
    
    attachment_map = {}
    for task in done:
        # This line might raise
        attachment, file = task.result()
        
        attachment_map[attachment] = file
    
    return [(attachment.name, attachment_map[attachment], attachment.description) for attachment in attachments]


async def get_message_and_files(client, channel, message_id):
    message = await get_message(client, channel, message_id)
    files = await get_files(client, message)
    
    return message, files


async def get_webhook(client, channel_id):
    executor_webhook = await client.webhook_get_own_channel(channel_id)
    if (executor_webhook is None):
        executor_webhook = await client.webhook_create(channel_id, 'Koishi hook')
    
    return executor_webhook


async def message_delete(client, message):
    try:
        await client.message_delete(message)
    except DiscordException as err:
        if err.code == ERROR_CODES.unknown_message:
            return
        
        raise
    
    except ConnectionError:
        return


async def get_files(client, message):
    attachments = message.attachments
    if (attachments is None):
        files = None
    else:
        files = await get_attachments(client, attachments)
    
    return files


@SLASH_CLIENT.events
async def reaction_add(client, event):
    guild = event.message.guild
    if guild is None:
        return
    
    emoji = event.emoji
    if emoji.is_custom_emoji():
        return
    
    source_channel = event.message.channel
    if source_channel is None:
        return
    
    if (
        (not event.user.has_role(ROLE__SUPPORT__TESTER)) and
        (not source_channel.permissions_for(event.user).can_manage_messages)
    ):
        return

    if not source_channel.cached_permissions_for(client).can_manage_messages:
        return
    
    unicode = emoji.unicode
    target_channels = [channel for channel in guild.channels.values() if unicode in channel.name]
    if len(target_channels) != 1:
        return
    
    target_channel = target_channels[0]
    if target_channel is source_channel:
        return
    
    if not target_channel.cached_permissions_for(client).can_manage_webhooks:
        return
    
    
    if target_channel.is_in_group_thread():
        channel_id = target_channel.parent_id
        thread_id = target_channel.id
    else:
        channel_id = target_channel.id
        thread_id = 0
    
    message = event.message
    
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
    
    await client.webhook_message_create(
        webhook,
        message.content,
        embed = message.clean_embeds,
        file = files,
        allowed_mentions = None,
        name = message.author.name_at(guild.id),
        avatar_url = message.author.avatar_url_at(guild.id),
        thread = thread_id,
    )
    
    files = None
