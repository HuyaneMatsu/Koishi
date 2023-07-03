__all__ = ('get_files', 'get_message_and_files', 'get_webhook',)

from hata import ERROR_CODES, DiscordException, KOKORO
from scarletio import Task, TaskGroup


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
            message = None
        
        else:
            raise
    
    return message


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
    message : `None`, ``Message``
    files : `None`, `list` of `tuple` (`str`, `bytes`, (`None`, `str`))
    
    Raises
    ------
    ConnectionError
        No internet connection
    DiscordException
        Client removed.
    """
    message = await get_message(client, channel, message_id)
    if message is None:
        files = None
    else:
        files = await get_files(client, message)
    
    return message, files
