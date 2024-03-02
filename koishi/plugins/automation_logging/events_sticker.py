__all__ = ()

from hata import Client, DiscordException, ERROR_CODES, GUILDS

from ...bot_utils.multi_client_utils import (
    get_first_client_in_guild_from, get_first_client_with_message_create_permissions_from
)
from ...bots import FEATURE_CLIENTS

from ..automation_core import AUTOMATION_CONFIGURATIONS, get_log_sticker_channel

from .constants import PERMISSIONS_EMBED_LINKS
from .embed_builder_sticker import build_sticker_create_embeds, build_sticker_delete_embeds, build_sticker_update_embeds



@FEATURE_CLIENTS.events
async def sticker_create(client, sticker):
    """
    Handles a sticker create event. If the sticker's guild has sticker logging setup, sends a message there.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    sticker : ``Sticker``
        The created sticker.
    """
    channel = get_log_sticker_channel(sticker.guild_id)
    if (channel is None):
        return
    
    if client is not get_first_client_with_message_create_permissions_from(
        channel, FEATURE_CLIENTS, PERMISSIONS_EMBED_LINKS
    ):
        return
    
    # We get the creator of the sticker.
    try:
        await client.sticker_get_guild(sticker, force_update = True)
    except ConnectionError:
        # No internet connection
        return
    
    except DiscordException as err:
        # Sticker already deleted?
        if err.code != ERROR_CODES.unknown_sticker:
            raise
    
    await client.message_create(
        channel,
        embed = build_sticker_create_embeds(sticker),
        allowed_mentions = None,
    )


@FEATURE_CLIENTS.events
async def sticker_update(client, sticker, old_attributes):
    """
    Handles a sticker edit event. If the sticker's guild has sticker logging setup, sends a message there.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    sticker : ``Sticker``
        The edited sticker.
    old_attributes : `dict` of (`str`, `object`) items
        The sticker's old attributes that have been edited.
    """
    channel = get_log_sticker_channel(sticker.guild_id)
    if (channel is None):
        return
    
    if client is not get_first_client_with_message_create_permissions_from(
        channel, FEATURE_CLIENTS, PERMISSIONS_EMBED_LINKS
    ):
        return
    
    await client.message_create(
        channel,
        embed = build_sticker_update_embeds(sticker, old_attributes),
        allowed_mentions = None,
    )


@FEATURE_CLIENTS.events
async def sticker_delete(client, sticker):
    """
    Handles a sticker delete event. If the sticker's guild has sticker logging setup, sends a message there.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    sticker : ``Sticker``
        The deleted sticker.
    """
    channel = get_log_sticker_channel(sticker.guild_id)
    if (channel is None):
        return
    
    if client is not get_first_client_with_message_create_permissions_from(
        channel, FEATURE_CLIENTS, PERMISSIONS_EMBED_LINKS
    ):
        return
    
    await client.message_create(
        channel,
        embed = build_sticker_delete_embeds(sticker),
        allowed_mentions = None,
    )


@FEATURE_CLIENTS.events(name = 'ready')
async def initial_request_stickers(client):
    """
    Requests the sticker of the guild where sticker logging is set up. On success removes itself from the events.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    """
    try:
        for automation_configuration in [
            automation_configuration for automation_configuration in AUTOMATION_CONFIGURATIONS.values()
            if automation_configuration.log_sticker_channel_id
        ]:
            guild = GUILDS.get(automation_configuration.guild_id, None)
            if (guild is not None) and (client is get_first_client_in_guild_from(guild, FEATURE_CLIENTS)):
                await client.sticker_get_all_guild(guild)
    
    except ConnectionError:
        # No internet connection
        return

    client.events.remove(initial_request_stickers, name = 'ready')
