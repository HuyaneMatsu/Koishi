__all__ = ()

from random import choice, random

from ...bots import SLASH_CLIENT

from ..blacklist_core import is_user_id_in_blacklist

from .chat_interactions import CHAT_INTERACTIONS
from .constants import ALLOWED_GUILD_IDS, TRIGGER_CHANCE


@SLASH_CLIENT.events
async def message_create(client, message):
    """
    Client message create event handler.
    
    Triggers a chat interaction if applicable.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the message.
    message : ``Message``
        The received message.
    """
    # Check author.
    author = message.author
    if author.bot or is_user_id_in_blacklist(author.id):
        return
    
    # Check guild_id.
    if message.guild_id not in ALLOWED_GUILD_IDS:
        return
    
    # Check permissions
    channel = message.channel
    permissions = channel.cached_permissions_for(client)
    if channel.is_in_group_thread():
        can_send_message = permissions.can_send_messages_in_threads
    else:
        can_send_message = permissions.can_send_messages
    if not can_send_message:
        return
    
    # Check whether should trigger.
    if random() > TRIGGER_CHANCE:
        return
    
    # Roll.
    chat_interaction = choice(CHAT_INTERACTIONS)
    
    # Trigger if applicable.
    outcome = chat_interaction.check_can_trigger(client, message)
    if outcome is not None:
        await chat_interaction.trigger(client, message, outcome)
