__all__ = ()

from hata import Client

from ...bot_utils.multi_client_utils import get_first_client_with_message_create_permissions_from
from ...bots import FEATURE_CLIENTS

from ..automation_core import get_log_mention_channel

from .embed_builder_mention import build_mention_embed


@FEATURE_CLIENTS.events
async def message_create(client, message):
    """
    Handles a message create event. If the message contains any mentions and if its guild has mention logging setup,
    sends a message there.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the message.
    message : ``Message``
        The created message.
    """
    channel = get_log_mention_channel(message.guild_id)
    if (channel is None):
        return
    
    if client is not get_first_client_with_message_create_permissions_from(channel, FEATURE_CLIENTS):
        return
    
    if (not message.mentioned_everyone) and (message.mentioned_users is None) and (message.mentioned_roles is None):
        return
    
    await client.message_create(
        channel,
        embed = build_mention_embed(message),
        allowed_mentions = None,
    )
