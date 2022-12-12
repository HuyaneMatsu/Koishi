__all__ = ()

from hata import ChannelType, Client, KOKORO, Permission, create_partial_channel_from_id
from scarletio import WaitTillAll

from ..constants import ALLOWED_GUILDS
from ..helpers import check_move_permissions, check_move_permissions_custom

from .constants import (
    CHANNEL_MOVER_BY_STATUS_MESSAGE_ID, CUSTOM_ID_CHANNEL_MOVER_CANCEL, CUSTOM_ID_RP_CHANNEL_MOVER_RESUME
)
from .context import ChannelMoverContext
from .helpers import check_movable, try_initialize_channel_move


SLASH_CLIENT: Client


@SLASH_CLIENT.interactions(
    guild = ALLOWED_GUILDS,
    required_permissions = Permission().update_by_keys(administrator = True),
)
async def move_channel(
    client,
    event,
    target_channel: ('channel_group_messageable', 'Where to move the channel\'s messages.', 'channel'),
    last_message_id : ('int', 'The last message\'s identifier to move from.') = 0,
):
    """Moves channel's all messages | Admin only"""
    check_move_permissions(client, event, target_channel, True)
    source_channel = event.channel
    check_movable(source_channel, target_channel)
    webhook = await try_initialize_channel_move(client, event, source_channel, target_channel)
    await ChannelMoverContext(client, event, source_channel, target_channel, last_message_id, webhook)


@SLASH_CLIENT.interactions(
    custom_id = CUSTOM_ID_CHANNEL_MOVER_CANCEL
)
async def move_channel_cancel(client, event):
    """Cancels the channel move operation."""
    await client.interaction_component_acknowledge(event)
    
    try:
        context = CHANNEL_MOVER_BY_STATUS_MESSAGE_ID[event.message.id]
    except KeyError:
        pass
    else:
        context.set_status_update_waiter_cancelled()
        await client.interaction_followup_message_create(
            event,
            'Cancelling',
            show_for_invoking_user_only = True,
        )


@SLASH_CLIENT.interactions(
    custom_id = CUSTOM_ID_RP_CHANNEL_MOVER_RESUME
)
async def move_channel_resume(client, event, source_channel_id, target_channel_id, last_message_id):
    """Resumes channel movement."""
    last_message_id = int(last_message_id)
    source_channel = create_partial_channel_from_id(int(source_channel_id), ChannelType.unknown, 0)
    target_channel = create_partial_channel_from_id(int(target_channel_id), ChannelType.unknown, 0)
    
    check_move_permissions_custom(
        client, source_channel, target_channel, source_channel.permissions_for(event.user), True
    )
    check_movable(source_channel, target_channel)
    webhook = await try_initialize_channel_move(client, event, source_channel, target_channel)
    await ChannelMoverContext(client, event, source_channel, target_channel, last_message_id, webhook)
    await client.interaction_component_message_edit(event, components = None)


@SLASH_CLIENT.events
async def shutdown(client):
    """
    Called when the client is shutting down.
    
    This function is a coroutine.
    """
    cancel_tasks = []
    
    for context in CHANNEL_MOVER_BY_STATUS_MESSAGE_ID.values():
        cancel_task = context.shutdown()
        if (cancel_task is not None):
            cancel_tasks.append(cancel_task)
    
    cancel_task = None
    
    await WaitTillAll(cancel_tasks, KOKORO)
