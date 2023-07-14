__all__ = ()

from hata import Client, DiscordException, ERROR_CODES

from ...bots import SLASH_CLIENT

from ..automation_core import AUTOMATION_CONFIGURATIONS, get_log_sticker_channel

from .embed_builder_sticker import build_sticker_create_embed, build_sticker_delete_embed, build_sticker_edit_embed



@SLASH_CLIENT.events
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
        embed = build_sticker_create_embed(sticker),
        allowed_mentions = None,
    )


@SLASH_CLIENT.events
async def sticker_edit(client, sticker, old_attributes):
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
    
    await client.message_create(
        channel,
        embed = build_sticker_edit_embed(sticker, old_attributes),
        allowed_mentions = None,
    )


@SLASH_CLIENT.events
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
    
    await client.message_create(
        channel,
        embed = build_sticker_delete_embed(sticker),
        allowed_mentions = None,
    )


@SLASH_CLIENT.events(name = 'ready')
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
            await client.sticker_get_all_guild(automation_configuration.guild_id)
    
    except ConnectionError:
        # No internet connection
        return

    client.events.remove(initial_request_stickers, name = 'ready')
