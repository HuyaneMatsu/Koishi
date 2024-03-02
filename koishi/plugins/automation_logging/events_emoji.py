__all__ = ()

from hata import Client, DiscordException, ERROR_CODES, GUILDS

from ...bot_utils.multi_client_utils import (
    get_first_client_in_guild_from, get_first_client_with_message_create_permissions_from
)
from ...bots import FEATURE_CLIENTS

from ..automation_core import AUTOMATION_CONFIGURATIONS, get_log_emoji_channel

from .constants import PERMISSIONS_EMBED_LINKS
from .embed_builder_emoji import build_emoji_create_embed, build_emoji_delete_embed, build_emoji_update_embed


@FEATURE_CLIENTS.events
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
    
    if client is not get_first_client_with_message_create_permissions_from(
        channel, FEATURE_CLIENTS, PERMISSIONS_EMBED_LINKS
    ):
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


@FEATURE_CLIENTS.events
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
    
    if client is not get_first_client_with_message_create_permissions_from(
        channel, FEATURE_CLIENTS, PERMISSIONS_EMBED_LINKS
    ):
        return
    
    await client.message_create(
        channel,
        embed = build_emoji_update_embed(emoji, old_attributes),
        allowed_mentions = None,
    )


@FEATURE_CLIENTS.events
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
    
    if client is not get_first_client_with_message_create_permissions_from(
        channel, FEATURE_CLIENTS, PERMISSIONS_EMBED_LINKS
    ):
        return
    
    await client.message_create(
        channel,
        embed = build_emoji_delete_embed(emoji),
        allowed_mentions = None
    )


@FEATURE_CLIENTS.events(name = 'ready')
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
            guild = GUILDS.get(automation_configuration.guild_id, None)
            if (guild is not None) and (client is get_first_client_in_guild_from(guild, FEATURE_CLIENTS)):
                await client.emoji_guild_get_all(guild)
    except ConnectionError:
        # No internet connection
        return
    
    client.events.remove(initial_request_emmojis, name = 'ready')
