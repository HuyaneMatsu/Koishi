__all__ = ()

from hata import Client

from ..configuration.operations import get_log_mention_channel

from .embed_builder_mention import build_mention_embed


SLASH_CLIENT: Client


@SLASH_CLIENT.events
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
    
    if (not message.mentioned_everyone) and (message.mentioned_users is None) and (message.mentioned_roles is None):
        return
    
    await client.message_create(
        channel,
        embed = build_mention_embed(message),
        allowed_mentions = None,
    )
