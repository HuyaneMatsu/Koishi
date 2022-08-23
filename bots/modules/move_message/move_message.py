__all__ = ()

from hata import Client, KOKORO, Permission
from scarletio import Task, WaitTillExc

from .constants import ALLOWED_GUILDS
from .helpers import check_move_permissions, get_message_and_files, get_webhook, message_delete


SLASH_CLIENT: Client


@SLASH_CLIENT.interactions(
    guild = ALLOWED_GUILDS,
    required_permissions = Permission().update_by_keys(manage_messages=True),
)
async def move_message(
    client,
    event,
    channel: ('channel_group_messageable', 'Where to move the message.'),
    message_id: ('int', 'The message\'s identifier. The message must be from this channel.')
):
    """Moves a message | Mod only"""
    check_move_permissions(client, event, channel, False)
    
    if channel.is_in_group_thread():
        channel_id = channel.parent_id
        thread_id = channel.id
    else:
        channel_id = channel.id
        thread_id = 0
    
    get_message_and_files_task = Task(get_message_and_files(client, event.channel, message_id), KOKORO)
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
