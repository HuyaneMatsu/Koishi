__all__ = ()

from hata import Client, Permission

from .constants import ALLOWED_GUILDS
from .helpers import check_move_permissions, create_webhook_message, get_files, get_webhook


SLASH_CLIENT : Client


@SLASH_CLIENT.interactions(
    guild = ALLOWED_GUILDS,
    show_for_invoking_user_only = True,
    required_permissions = Permission().update_by_keys(administrator = True),
)
async def move_channel(
    client,
    event,
    channel: ('channel_group_messageable', 'Where to move the channel\'s messages.'),
):
    """Moves channel's all messages | Mod only"""
    check_move_permissions(client, event, channel, True)
    
    yield f'Starting to move messages to {channel.name}'
    
    if channel.is_in_group_thread():
        channel_id = channel.parent_id
        thread_id = channel.id
    else:
        channel_id = channel.id
        thread_id = 0
    
    source_channel_id = event.channel_id
    guild_id = event.guild_id
    
    request_more = True
    after_id = 0
    webhook = await get_webhook(client, channel_id)
    
    while request_more:
        messages = await client.message_get_chunk(source_channel_id, after=after_id)
        
        if len(messages) < 100:
            request_more = False
        else:
            after_id = messages[0].id
        
        for message in reversed(messages):
            files = await get_files(client, message)
            try:
                await create_webhook_message(client, webhook, message, thread_id, files)
            except:
                # Unallocate files if exception occurs
                files = None
                raise
