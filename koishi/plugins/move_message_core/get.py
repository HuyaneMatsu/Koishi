__all__ = ('get_files', 'get_message', 'get_webhook',)

from hata import ERROR_CODES, DiscordException

from ...bot_utils.response_data_streaming import create_http_stream_resource


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


def get_files(client, message):
    """
    Requests the files of the given messages.
    
    Parameters
    ----------
    client : ``Client``
        The respective client.
    
    message : ``Message``
        The message to the files of.
    
    Returns
    -------
    files : ``None | list<(str, AttachmentStream, None | str)>``
        Files of the message.
    """
    snapshot = message.snapshot
    if snapshot is None:
        attachments = message.attachments
    else:
        attachments = snapshot.attachments
    
    if (attachments is None):
        files = None
    else:
        files = [
            (attachment.name, create_http_stream_resource(client.http, attachment.url), attachment.description)
            for attachment in attachments
        ]
    
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
