__all__ = ()

from hata import Client, DiscordException, ERROR_CODES

from ...bots import SLASH_CLIENT

from ..automation_core import AUTOMATION_CONFIGURATIONS, get_log_emoji_channel

from .embed_builder_emoji import build_emoji_create_embed, build_emoji_delete_embed, build_emoji_update_embed


@SLASH_CLIENT.events
async def emoji_create(client, emoji):
    """
    Handles a emoji create event. If the emoji's guild has emoji logging setup, sends a message there.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    emoji : ``Emoji``
        The created emoji.
    """
    channel = get_log_emoji_channel(emoji.guild_id)
    if (channel is None):
        return
    
    # We get the creator of the emoji.
    try:
        await client.emoji_get(emoji, force_update = True)
    except ConnectionError:
        # No internet connection
        return
    
    except DiscordException as err:
        # Sticker already deleted?
        if err.code != ERROR_CODES.unknown_emoji:
            raise
    
    await client.message_create(
        channel,
        embed = build_emoji_create_embed(emoji),
        allowed_mentions = None,
    )


@SLASH_CLIENT.events
async def emoji_update(client, emoji, old_attributes):
    """
    Handles a emoji edit event. If the emoji's guild has emoji logging setup, sends a message there.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    emoji : ``Emoji``
        The edited emoji.
    old_attributes : `dict` of (`str`, `object`) items
        The emoji's old attributes that have been edited.
    """
    channel = get_log_emoji_channel(emoji.guild_id)
    if (channel is None):
        return
    
    await client.message_create(
        channel,
        embed = build_emoji_update_embed(emoji, old_attributes),
        allowed_mentions = None,
    )


@SLASH_CLIENT.events
async def emoji_delete(client, emoji):
    """
    Handles a emoji delete event. If the emoji's guild has emoji logging setup, sends a message there.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    emoji : ``Emoji``
        The deleted emoji.
    """
    channel = get_log_emoji_channel(emoji.guild_id)
    if (channel is None):
        return
    
    await client.message_create(
        channel,
        embed = build_emoji_delete_embed(emoji),
        allowed_mentions = None
    )


@SLASH_CLIENT.events(name = 'ready')
async def initial_request_emmojis(client):
    """
    Requests the emojis of the guild where emoji logging is set up. On success removes itself from the events.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    """
    try:
        for automation_configuration in [
            automation_configuration for automation_configuration in AUTOMATION_CONFIGURATIONS.values()
            if automation_configuration.log_emoji_channel_id
        ]:
            await client.emoji_guild_get_all(automation_configuration.guild_id)
    except ConnectionError:
        # No internet connection
        return
    
    client.events.remove(initial_request_emmojis, name = 'ready')
