__all__ = ()

from hata import DiscordException, ERROR_CODES, KOKORO
from hata.ext.slash import abort
from scarletio import Task, WaitTillExc


async def get_message(client, channel, message_id):
    try:
        message = await client.message_get((channel.id, message_id))
    except DiscordException as err:
        if err.code == ERROR_CODES.unknown_message:
            return abort(f'Unknown message: {message_id}')
        
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


def check_move_permissions(client, event, channel, require_admin_permissions):
    user_permissions = event.user_permissions
    if require_admin_permissions:
        if (not user_permissions.can_administrator):
            return abort('You need to have administrator permission to invoke this command.')
    
    else:
        if (not user_permissions.can_manage_messages):
            return abort('You need to have manage messages permission to invoke this command.')
        
        source_channel = event.channel
        if (source_channel is None) or (not source_channel.cached_permissions_for(client).can_manage_messages):
            return abort('I require manage messages permission in this channel to execute the command.')
        
    if (not channel.cached_permissions_for(client).can_manage_webhooks):
        return abort('I need manage webhook permission in the target channel to execute this this command.')
