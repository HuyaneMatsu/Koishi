__all__ = ()

from hata import Client
from scarletio import CancelledError

from ..configuration.operations import get_log_satori_channel
from ..configuration.satori import (
    clear_satori_channel, clear_satori_channels, discover_satori_channels, get_watcher_channels_for,
    remove_watcher_channel, reset_satori_channels, set_satori_channel
)

from .embed_builder_satori import build_presence_update_embeds


SLASH_CLIENT: Client


# Hata best wrapper

def setup(module):
    """
    Called after the module is loaded. Discovers all satori channels if the client is running.
    
    Parameters
    ----------
    module : ``ModuleType``
        This module.
    """
    if SLASH_CLIENT.running:
        discover_satori_channels()


def teardown(module):
    """
    Called after the module is unloaded. Clears all satori channels.
    
    Parameters
    ----------
    module : ``ModuleType``
        This module.
    """
    clear_satori_channels()


@SLASH_CLIENT.events
async def ready(client):
    """
    Handles a ready event. Resets all satori channels.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    """
    reset_satori_channels()


@SLASH_CLIENT.events
async def guild_delete(client, guild, guild_profile):
    """
    Handles a guild delete event. Removes all of it
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    guild : ``Guild``
        The deleted guild.
    guild_profile : `None`, ``GuildProfile``
        The client's guild profile at the guild.
    """
    satori_channel = get_log_satori_channel(guild.id)
    if (satori_channel is not None):
        clear_satori_channel(satori_channel)


@SLASH_CLIENT.events
async def channel_delete(client, channel):
    """
    Handles a channel delete event. Removes the channel from watchers if present.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    channel : ``Channel``
        The deleted channel.
    """
    if not channel.is_in_group_guild_system():
        return
    
    try:
        user_id = int(channel.name)
    except ValueError:
        return
    else:
        remove_watcher_channel(channel.id, user_id)


@SLASH_CLIENT.events
async def channel_create(client, channel):
    """
    Handles a channel create event. Registers the channel as a watchers if applicable.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    channel : ``Channel``
        The created channel.
    """
    if not channel.is_in_group_guild_system():
        return
    
    satori_channel = get_log_satori_channel(channel.guild_id)
    if (satori_channel is None):
        return
    
    if channel.parent_id != satori_channel.id:
        return
    
    try:
        user_id = int(channel.name)
    except KeyError:
        pass
    else:
        set_satori_channel(channel.id, user_id)


@SLASH_CLIENT.events
async def channel_edit(client, channel, old_attributes):
    """
    Handles a channel edition event.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    channel : ``Channel``
        The modified channel.
    old_attributes : `dict` of (`str` `object`) items
        The channel's modified attributes.
    """
    if not channel.is_in_group_guild_system():
        return
    
    satori_channel = get_log_satori_channel(channel.guild_id)
    if (satori_channel is None):
        return
    
    try:
        old_parent_id = old_attributes['parent_id']
    except KeyError:
        pass
    else:
        # Moved out
        if old_parent_id == satori_channel.id:
            try:
                user_id = int(old_attributes.get('name', channel.name))
            except ValueError:
                return
            else:
                remove_watcher_channel(channel.id, user_id)
            return
        
        # Moved in
        if channel.parent_id == satori_channel.id:
            try:
                user_id = int(channel.name)
            except ValueError:
                return
            else:
                set_satori_channel(channel.id, user_id)
            return
    
    if channel.parent_id != satori_channel.id:
        return
    
    try:
        name = old_attributes['name']
    except KeyError:
        pass
    else:
        try:
            user_id = int(name)
        except KeyError:
            pass
        else:
            remove_watcher_channel(channel.id, user_id)
    
    try:
        user_id = int(channel.name)
    except KeyError:
        pass
    else:
        set_satori_channel(channel.id, user_id)


@SLASH_CLIENT.events
async def user_presence_update(client, user, old_attributes):
    """
    Handles a user presence update event. If the user is watched sends a message to every watching channel.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    user : ``ClientUserBase``
        The user, who's presence was updated.
    old_attributes : `dict` of (`str` `object`) items
        The user's old presence.
    """
    channels = get_watcher_channels_for(user.id)
    if channels is None:
        return
    
    embeds = build_presence_update_embeds(user, old_attributes)
    
    for channel in channels:
        try:
            await client.message_create(channel, embed = embeds)
        except GeneratorExit:
            raise
        
        except CancelledError:
            raise
        
        except BaseException as err:
            await client.events.error(client, 'log.user_presence_update', err)
