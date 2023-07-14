__all__ = ()

from hata import KOKORO, Permission
from hata.ext.slash import abort
from scarletio import Task, TaskGroup

from ...bots import SLASH_CLIENT

from ..move_message_core.create import create_webhook_message
from ..move_message_core.get import get_message_and_files, get_webhook

from .checks import check_move_permissions
from .constants import ALLOWED_GUILDS
from .helpers import message_delete



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
    
    get_message_and_files_task = Task(KOKORO, get_message_and_files(client, event.channel, message_id))
    get_webhook_task = Task(KOKORO, get_webhook(client, channel_id))
    
    task_group = TaskGroup(
        KOKORO,
        [
            get_message_and_files_task,
            get_webhook_task,
            Task(KOKORO, client.interaction_application_command_acknowledge(event, show_for_invoking_user_only = True))
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
    
    if message is None:
        return abort('Unknown message.')
    
    try:
        await create_webhook_message(client, webhook, message, thread_id, files)
    finally:
        files = None
    
    Task(KOKORO, message_delete(client, message))
    
    await client.interaction_response_message_edit(event, 'Message moved successfully.')
