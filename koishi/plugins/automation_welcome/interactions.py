__all__ = ()

from hata import Embed

from ...bots import SLASH_CLIENT

from .helpers import can_send_messages
from .constants import CUSTOM_ID_WELCOME_REPLY, REPLY_EXPIRES_AFTER
from .spam_protection import is_reply_in_cache
from .welcome_styles import WELCOME_STYLE_DEFAULT


@SLASH_CLIENT.interactions(custom_id = CUSTOM_ID_WELCOME_REPLY)
async def welcome_reply(client, event):
    """
    Sends a welcome reply.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    """
    await client.interaction_component_acknowledge(event)
    
    channel = event.channel
    user = event.user
    if not can_send_messages(channel, channel.permissions_for(user)):
        return
    
    message = event.message
    if message is None:
        return None
    
    mentioned_users = message.mentioned_users
    if mentioned_users is None:
        return
    
    joined_user = mentioned_users[0]
    if user is joined_user:
        return
    
    # If the welcome is too old, notify and remove button.
    if event.id - message.id > REPLY_EXPIRES_AFTER:
        await client.interaction_followup_message_create(
            event,
            content = 'You are late to the party! Be earlier next time :3',
            show_for_invoking_user_only = True,
            silent = True,
        )
        
        await client.interaction_response_message_edit(
            event,
            components = None,
        )
        return
    
    # Check cache
    if is_reply_in_cache(event.guild_id, message.id, event.user_id):
        return
    
    # We are in time (yay)
    welcome_style = WELCOME_STYLE_DEFAULT
    
    seed = event.guild_id ^ joined_user.id
    reply_content_builders = welcome_style.reply_content_builders
    message_content = reply_content_builders[seed % len(reply_content_builders)](user.mention, joined_user.mention)
    
    seed = seed ^ event.user_id
    images = welcome_style.images
    image = images[seed % len(images)]
    
    color = (event.id >> 22) & 0xffffff
    
    await client.interaction_followup_message_create(
        event,
        allowed_mentions = [joined_user],
        content = f'> {message_content}',
        embed = Embed(color = color).add_image(image),
        silent = True,
    )
