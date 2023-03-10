__all__ = ()

from hata import Client, KOKORO, Permission
from scarletio import Task, TaskGroup

from .constants import ALLOWED_GUILDS
from .helpers import (
    check_move_permissions, create_webhook_message, get_message, get_message_and_files, get_webhook, message_delete
)


SLASH_CLIENT: Client


@SLASH_CLIENT.interactions(
    guild = ALLOWED_GUILDS,
    required_permissions = Permission().update_by_keys(manage_messages = True),
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
    
    message = await get_message(client, channel, message_id)
    
    get_message_and_files_task = Task(get_message_and_files(client, event.channel, message_id), KOKORO)
    get_webhook_task = Task(get_webhook(client, channel_id), KOKORO)
    
    task_group = TaskGroup(
        KOKORO,
        [
            get_message_and_files_task,
            get_webhook_task,
            Task(client.interaction_application_command_acknowledge(event, show_for_invoking_user_only = True), KOKORO)
        ],
    )
    
    failed_tasks = await task_group.wait_exception()
    if (failed_tasks is not None):
        # Cancel all and propagate the exception of the first failed task
        task_group.cancel_all()
        failed_tasks.get_result()
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
    
    Task(message_delete(client, message), KOKORO)
    
    await client.interaction_response_message_edit(event, 'Message moved successfully.')
