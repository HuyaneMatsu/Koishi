__all__ = ()

import re

from hata import DATETIME_FORMAT_CODE, DiscordException, ERROR_CODES, KOKORO, WebhookBase
from hata.ext.slash import abort
from scarletio import Task, TaskGroup, sleep

DATE_CONNECTOR = ' - '
NAME_WITH_DATE_RP = re.compile(
    f'.*?{re.escape(DATE_CONNECTOR)}\\d{{4}}\\-\\d{{2}}\\-\\d{{2}} \\d{{2}}\\:\\d{{2}}\\:\\d{{2}}'
)
NAME_LENGTH_MAX = 80 - (19 + len(DATE_CONNECTOR))


async def get_message(client, channel, message_id):
    """
    Requests the message for the given identifier.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The respective client.
    channel : ``Channel``
        The channel where the message is.
    message_id : `int`
        The message's id to request.
    
    Returns
    -------
    message : ``Message``
    
    Raises
    ------
    ConnectionError
        No internet connection
    DiscordException
        Client removed.
    """
    try:
        message = await client.message_get((channel.id, message_id))
    except DiscordException as err:
        if err.code == ERROR_CODES.unknown_message:
            return abort(f'Unknown message: {message_id}')
        
        raise
    
    return message


async def get_attachment(client, attachment):
    """
    Requests the given attachment's file.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The respective client.
    attachment : ``Attachment``
        The attachment to request.
    
    Returns
    -------
    attachment : ``Attachment``
        The requested attachment to reproduce their order.
    file : `bytes`
        The requested file.
    """
    file = await client.download_attachment(attachment)
    return attachment, file


async def get_attachments(client, attachments):
    """
    Requests the given attachments.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The respective client.
    attachments : `tuple` of ``Attachment``
        The attachments to request.
    
    Returns
    -------
    attachments : `list` of `tuple` (`str`, `bytes`, (`None`, `str`))
    """
    task_group = TaskGroup(KOKORO, (Task(KOKORO, get_attachment(client, attachment)) for attachment in attachments))
    failed_task = await task_group.wait_exception()
    if (failed_task is not None):
        # Cancel all and propagate the first failing one
        task_group.cancel_all()
        failed_task.get_result()
        return
    
    attachment_map = {}
    for task in task_group.done:
        # This line might raise
        attachment, file = task.get_result()
        
        attachment_map[attachment] = file
    
    return [(attachment.name, attachment_map[attachment], attachment.description) for attachment in attachments]


async def get_message_and_files(client, channel, message_id):
    """
    Gets the given message by their identifier and requests it's attachments too.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The respective client.
    channel : ``Channel``
        The channel where the message is.
    message_id : `int`
        The message's id to request.
    
    
    Returns
    -------
    message : ``Message``
    files : `None`, `list` of `tuple` (`str`, `bytes`, (`None`, `str`))
    
    Raises
    ------
    ConnectionError
        No internet connection
    DiscordException
        Client removed.
    """
    message = await get_message(client, channel, message_id)
    files = await get_files(client, message)
    
    return message, files


async def get_webhook(client, channel_id):
    """
    Gets the optimal webhook to use for the given channel by it's identifier.
    
    This function is a coroutine.
    
    client : ``Client``
        The respective client.
    channel_id : `int`
        The respective channel's identifier.
    
    Returns
    -------
    webhook : ``Webhook``
    """
    executor_webhook = await client.webhook_get_own_channel(channel_id)
    if (executor_webhook is None):
        executor_webhook = await client.webhook_create(channel_id, 'Koishi hook')
    
    return executor_webhook


async def message_delete(client, message):
    """
    Deletes the given message with the client.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The respective client.
    message : ``Message``
        The message to delete.
    """
    try:
        await client.message_delete(message)
    except DiscordException as err:
        if err.code == ERROR_CODES.unknown_message:
            return
        
        raise
    
    except ConnectionError:
        return


async def get_files(client, message):
    """
    Requests the files of the given messages.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The respective client.
    message : ``Message``
        The message to the files of.
    
    Returns
    -------
    files : `None`, `list` of `tuple` (`str`, `bytes`, (`None`, `str`))
        Files of the message.
    """
    attachments = message.attachments
    if (attachments is None):
        files = None
    else:
        files = await get_attachments(client, attachments)
    
    return files


def check_move_permissions(client, event, target_channel, require_admin_permissions):
    """
    Checks the user's permissions whether the user can move messages.
    
    Parameters
    ----------
    client : ``Client``
        The respective client who is moving the messages.
    event : ``InteractionEvent``
        The received interaction event.
    target_channel : ``Channel``
        The target channel of moving.
    require_admin_permissions : `bool`
        Whether we should require admin permission and not manage messages.
    """
    return check_move_permissions_custom(
        client, event.channel, target_channel, event.user_permissions, require_admin_permissions
    )


def check_move_permissions_custom(client, source_channel, target_channel, user_permissions, require_admin_permissions):
    """
    Checks the user's permissions whether the user can move messages. This is a more customizable checker than 
    ``.check_move_permissions``, since it directly accepts context parameters.
    
    Parameters
    ----------
    client : ``Client``
        The respective client who is moving the messages.
    source_channel : ``Channel``
        Source channel to move from.
    target_channel : ``Channel``
        The target channel of moving.
    user_permissions : ``Permission``
        The user's permissions.
    require_admin_permissions : `bool`
        Whether we should require admin permission and not manage messages.
    """
    if require_admin_permissions:
        if (not user_permissions.can_administrator):
            return abort('You need to have administrator permission to invoke this command.')
    
    else:
        if (not user_permissions.can_manage_messages):
            return abort('You need to have manage messages permission to invoke this command.')
        
        if (source_channel is None) or (not source_channel.cached_permissions_for(client).can_manage_messages):
            return abort('I require manage messages permission in this channel to execute the command.')
        
    if (not target_channel.cached_permissions_for(client).can_manage_webhooks):
        return abort('I need manage webhook permission in the target channel to execute this this command.')


async def create_webhook_message(client, webhook, message, thread_id, files):
    """
    Sends the given message with the given webhook.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client to send the message with.
    webhook : ``Webhook``
        The webhook to send the message with.
    message : ``Message``
        The message to send.
    thread_id : `int`
        Thread identifier to send if sending to a thread if applicable.
    files : `None`, `list` of `tuple` (`str`, `bytes`, (`None`, `str`))
        Files of the message.
    """
    name = _get_user_name(message)
    avatar_url = message.author.avatar_url_at(message.guild_id)
    
    content = message.content
    if (content is not None):
        while len(content) > 2000:
            await _repeat_create_webhook_message(
                client, webhook, content[:2000], None, None, name, avatar_url, thread_id,
            )
            
            content = content[2000:]
    
    try:
        await _repeat_create_webhook_message(
            client, webhook, content, message.clean_embeds, files, name, avatar_url, thread_id,
        )
    except:
        # Unallocate files if any exception occurs.
        files = None
        raise


def _get_user_name(message):
    """
    Gets the message's author's name.
    
    Parameters
    ----------
    message : ``Message``
        The respective message.
    
    Returns
    -------
    name : `str`
    """
    user = message.author
    name = user.name_at(message.guild_id)
    
    if isinstance(user, WebhookBase) and (NAME_WITH_DATE_RP.fullmatch(name) is not None):
        return name
    
    if len(name) > NAME_LENGTH_MAX:
        name = name[: NAME_LENGTH_MAX - len(' ...')] + ' ...'
    
    return f'{name}{DATE_CONNECTOR}{message.created_at:{DATETIME_FORMAT_CODE}}'


async def _repeat_create_webhook_message(client, webhook, content, embeds, files, name, avatar_url, thread_id):
    """
    Sends a webhook message. If encounters unique rate limits then repeats.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client to send the message with.
    webhook : ``Webhook``
        The webhook to send the message with.
    content : `None`, `str`
        The message's content.
    embeds : `None`, `list` of ``Embed``
        Embeds to send the message with.
    files : `None`, `list` of `tuple` (`str`, `bytes`, (`None`, `str`))
        Attachments of the message.
    name : `str`
        The user's name to use.
    avatar_url : `None`, `str`
        User avatar url to use.
    thread_id : `int`
        Thread identifier to send if sending to a thread if applicable.
    """
    while True:
        try:    
            await client.webhook_message_create(
                webhook,
                content,
                embed = embeds,
                file = files,
                allowed_mentions = None,
                name = name,
                avatar_url = avatar_url,
                thread = thread_id,
            )
        except DiscordException as err:
            if err.code == ERROR_CODES.rate_limit_resource:
                await sleep(err.retry_after, KOKORO)
                continue
            
            raise
        
        break
