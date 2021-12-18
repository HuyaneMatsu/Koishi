from scarletio import Task, WaitTillExc
from hata import Client, Guild, DiscordException, ERROR_CODES, ChannelThread, KOKORO
from hata.ext.slash import abort

SLASH_CLIENT: Client

GUILD__KOISHI_CLAN = Guild.precreate(866746184990720020)

async def get_message(client, channel, message_id):
    try:
        message = await client.message_get(channel, message_id)
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
    
    attachments = message.attachments
    if (attachments is None):
        files = None
    else:
        files = await get_attachments(client, attachments)
    
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


@SLASH_CLIENT.interactions(guild=GUILD__KOISHI_CLAN)
async def move_message(client, event,
    channel: ('channel_group_messageable', 'Where to move the message.'),
    message_id: ('int', 'The message\'s identifier. The message must be from this channel.')
):
    """Moves a message | Mod only"""
    user_permissions = event.user_permissions
    if (not user_permissions.can_manage_messages):
        abort('You need to have manage messages to invoke this command.')
    
    source_channel = event.channel
    if (source_channel is None) or (not source_channel.cached_permissions_for(client).can_manage_messages):
        abort('I require manage messages permission in this channel to execute the command.')
    
    if (not channel.cached_permissions_for(client).can_manage_webhooks):
        abort('I need manage webhook permission in the target channel to execute this this command.')
    
    if isinstance(channel, ChannelThread):
        channel_id = channel.parent_id
        thread_id = channel.id
    else:
        channel_id = channel.id
        thread_id = 0
    
    get_message_and_files_task = Task(get_message_and_files(client, source_channel, message_id), KOKORO)
    get_webhook_task = Task(get_webhook(client, channel_id), KOKORO)
    
    done, pending = await WaitTillExc(
        [
            get_message_and_files_task,
            get_webhook_task,
            Task(client.interaction_application_command_acknowledge(event, show_for_invoking_user_only=True), KOKORO)
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
        name = message.author.name_at(event.guild_id),
        avatar_url = message.author.avatar_url_at(event.guild_id),
        thread = thread_id,
    )
    
    files = None
    
    Task(message_delete(client, message), KOKORO)
    
    await client.interaction_response_message_edit(event, 'Message moved successfully.')
