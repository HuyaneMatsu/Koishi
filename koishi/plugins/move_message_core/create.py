__all__ = ('create_webhook_message',)

from hata import DiscordException, ERROR_CODES, KOKORO
from scarletio import sleep

from .helpers import _get_user_name


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
    if not message.has_any_content_field():
        return
    
    name = _get_user_name(message)
    avatar_url = message.author.avatar_url_at(message.guild_id)
    
    poll = message.poll
    if (poll is not None):
        poll = poll.copy_with(duration = 3600)
    
    content = message.content
    if (content is not None):
        while len(content) > 2000:
            try:
                await _repeat_create_webhook_message(
                    client, webhook, content[:2000], None, None, name, None, avatar_url, thread_id,
                )
            except:
                files = None
                raise
            
            content = content[2000:]
    
    try:
        await _repeat_create_webhook_message(
            client, webhook, content, message.clean_embeds, files, name, poll, avatar_url, thread_id
        )
    except:
        # Unallocate files if any exception occurs.
        files = None
        raise


async def _repeat_create_webhook_message(client, webhook, content, embeds, files, name, poll, avatar_url, thread_id):
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
    embeds : ``None | list<Embed>``
        Embeds to send the message with.
    files : `None`, `list` of `tuple` (`str`, `bytes`, (`None`, `str`))
        Attachments of the message.
    name : `str`
        The user's name to use.
    poll : `None | Poll`
        The message's poll.
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
                poll = poll,
                avatar_url = avatar_url,
                thread = thread_id,
            )
        except DiscordException as err:
            if err.code == ERROR_CODES.rate_limit_resource:
                await sleep(err.retry_after, KOKORO)
                continue
            
            if err.code == ERROR_CODES.cannot_create_empty_message:
                break
            
            raise
        
        break
