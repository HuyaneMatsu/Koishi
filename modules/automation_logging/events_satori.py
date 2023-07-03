__all__ = ()

from hata import ChannelType, Client, DiscordException, ERROR_CODES
from scarletio import CancelledError

from bots import SLASH_CLIENT

from ..automation_core import (
    clear_satori_channel, clear_satori_channels, discover_satori_channels, get_log_satori_channel,
    get_log_satori_channel_if_auto_start, get_watcher_channels_for, remove_watcher_channel, reset_satori_channels,
    set_satori_channel
)

from .components_satori_auto_start import build_satori_auto_start_component_row
from .embed_builder_satori import build_presence_update_embeds
from .embed_builder_satori_auto_start import build_satori_auto_start_embed


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
    except ValueError:
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
        except ValueError:
            pass
        else:
            remove_watcher_channel(channel.id, user_id)
    
    try:
        user_id = int(channel.name)
    except ValueError:
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
        if not channel.cached_permissions_for(client).can_send_messages:
            continue
        
        try:
            await client.message_create(
                channel,
                allowed_mentions = None,
                embed = embeds,
            )
        except (GeneratorExit, CancelledError):
            raise
        
        except ConnectionError:
            break
        
        except BaseException as err:
            if isinstance(err, DiscordException) and err.code in (
                ERROR_CODES.unknown_channel, # channel deleted
                ERROR_CODES.missing_access, # client removed
                ERROR_CODES.missing_permissions, # permissions changed
            ):
                continue
            
            await client.events.error(client, 'log.satori.user_presence_update', err)
            continue


@SLASH_CLIENT.events
async def guild_user_add(client, guild, user):
    """ 
    Handles a user guild add event. If the guild has satori channel set with auto start then creates a new channel for
    the user and sends a starting message.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    guild : ``Guild``
        The joined guild..
    user : ``ClientUserBase``
        The user who joined.
    """
    # Bots are invited, so we do not really care about them
    if user.bot:
        return
    
    satori_channel = get_log_satori_channel_if_auto_start(guild.id)
    if satori_channel is None:
        return
    
    # Try to find the channel
    channel_name = str(user.id)
    for channel in satori_channel.iter_channels():
        if channel.name == channel_name:
            break
    
    else:
        # Channel not found -> create
        
        # Check channel permissions
        if not satori_channel.cached_permissions_for(client).can_manage_channels:
            return
        
        try:
            # No need to pass permission overwrites, seems like it is auto inherited from parent.
            channel = await client.channel_create(
                guild,
                channel_type = ChannelType.guild_text,
                name = channel_name,
                parent_id = satori_channel.id,
            )
        except (GeneratorExit, CancelledError):
            raise
        
        except ConnectionError:
            return
        
        except BaseException as err:
            if isinstance(err, DiscordException) and err.code in (
                ERROR_CODES.unknown_channel, # channel deleted
                ERROR_CODES.missing_access, # client removed
                ERROR_CODES.missing_permissions, # permissions changed
            ):
                return
            
            await client.events.error(client, 'log.satori.guild_user_add', err)
            return
    
    # Check permissions of the new channel
    if not channel.cached_permissions_for(client).can_send_messages:
        return
    
    try:
        await client.message_create(
            channel,
            allowed_mentions = None,
            components = build_satori_auto_start_component_row(user),
            embed = build_satori_auto_start_embed(guild, user),
        )
    except (GeneratorExit, CancelledError):
        raise
    
    except ConnectionError:
        return
    
    except BaseException as err:
        if isinstance(err, DiscordException) and err.code in (
            ERROR_CODES.unknown_channel, # channel deleted
            ERROR_CODES.missing_access, # client removed
            ERROR_CODES.missing_permissions, # permissions changed
        ):
            return
        
        await client.events.error(client, 'log.satori.guild_user_add', err)
        return
