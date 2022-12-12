__all__ = ()

from hata import Client, DiscordException, ERROR_CODES, Permission, is_id
from hata.ext.slash import abort

from ..constants import ALLOWED_GUILDS
from ..helpers import check_move_permissions

from .constants import (
    CUSTOM_ID_MESSAGE_MOVER_ADD_BY_ID, CUSTOM_ID_MESSAGE_MOVER_CANCEL, CUSTOM_ID_MESSAGE_MOVER_CLOSE,
    CUSTOM_ID_MESSAGE_MOVER_SUBMIT, MESSAGE_MOVER_ADD_BY_ID_FORM, MESSAGE_MOVER_CONTEXTS
)
from .context import MessageMoverContext


SLASH_CLIENT: Client


@SLASH_CLIENT.interactions(custom_id = CUSTOM_ID_MESSAGE_MOVER_SUBMIT)
async def submit_message_mover(event):
    await maybe_call_message_mover_method(event, MessageMoverContext.submit)


@SLASH_CLIENT.interactions(custom_id = CUSTOM_ID_MESSAGE_MOVER_CANCEL)
async def cancel_message_mover(event):
    await maybe_call_message_mover_method(event, MessageMoverContext.cancel)


@SLASH_CLIENT.interactions(custom_id = CUSTOM_ID_MESSAGE_MOVER_CLOSE)
async def close_message_mover(client, event):
    if event.user_permissions.can_manage_messages:
        await client.interaction_component_acknowledge(event)
        await client.interaction_response_message_delete(event)


async def maybe_call_message_mover_method(event, function):
    if not event.user_permissions.can_manage_messages:
        return
    
    try:
        message_mover_context = MESSAGE_MOVER_CONTEXTS[(event.user.id, event.channel_id)]
    except KeyError:
        pass
    else:
        await function(message_mover_context, event)


@SLASH_CLIENT.interactions(
    guild = ALLOWED_GUILDS,
    required_permissions = Permission().update_by_keys(manage_messages=True),
)
async def move_messages(
    client,
    event,
    channel: ('channel_group_messageable', 'Where to move the message.'),
):
    """Moves messages | Mod only"""
    check_move_permissions(client, event, channel, False)
    
    if channel.is_in_group_thread():
        channel_id = channel.parent_id
        thread_id = channel.id
    else:
        channel_id = channel.id
        thread_id = 0
    
    context = MessageMoverContext(client, event, event.channel_id, channel_id, thread_id)
    await context.start()


@SLASH_CLIENT.interactions(
    guild = ALLOWED_GUILDS,
    required_permissions = Permission().update_by_keys(manage_messages=True),
    target = 'message',
)
async def add_to_move_group(
    event,
    message,
):
    """Adds a message to message move context."""
    await add_message_to_move_group(event, message)


@SLASH_CLIENT.interactions(custom_id = CUSTOM_ID_MESSAGE_MOVER_ADD_BY_ID)
async def add_message_by_id_button_click(event):
    if event.user_permissions.can_manage_messages:
        return MESSAGE_MOVER_ADD_BY_ID_FORM


@SLASH_CLIENT.interactions(custom_id = CUSTOM_ID_MESSAGE_MOVER_ADD_BY_ID, target = 'form')
async def add_message_by_id_form_submit(client, event, *, message_id):
    if not is_id(message_id):
        abort(f'Please submit a message\'s id.')
    
    try:
        message = await client.message_get((event.channel_id, int(message_id)))
    except DiscordException as err:
        if err.code == ERROR_CODES.unknown_message:
            abort('The given id refers to a non-existing message.')
        
        raise
    
    await add_message_to_move_group(event, message)
    

async def add_message_to_move_group(event, message):
    key = (event.user.id, event.channel_id)
    
    try:
        context = MESSAGE_MOVER_CONTEXTS[key]
    except KeyError:
        abort('There is no message mover context in the channel.')
    else:
        await context.add_message(event, message)
