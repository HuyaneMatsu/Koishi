__all__ = ()

from hata import ChannelType, Client, DiscordException, ERROR_CODES, Permission
from scarletio import CancelledError

from ...bots import MAIN_CLIENT

from ..automation_core import (
    clear_satori_channel, clear_satori_channels, discover_satori_channels, get_log_satori_channel,
    get_log_satori_channel_if_auto_start, get_watcher_channels_for, remove_watcher_channel, reset_satori_channels,
    set_satori_channel
)

from .components_satori_auto_start import build_satori_auto_start_component_row
from .constants import PERMISSIONS_EMBED_LINKS
from .embed_builder_guild_profile import build_guild_profile_update_embed
from .embed_builder_satori import build_presence_update_embeds
from .embed_builder_satori_start import build_satori_auto_start_embeds


REQUIRED_PERMISSIONS = PERMISSIONS_EMBED_LINKS | Permission().update_by_keys(send_messages = True)


# Only added for 1 client.
# Hata best wrapper

def setup(module):
    """
    Called after the module is loaded. Discovers all satori channels if the client is running.
    
    Parameters
    ----------
    module : ``ModuleType``
        This module.
    """
    if MAIN_CLIENT.running:
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


@MAIN_CLIENT.events
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


@MAIN_CLIENT.events
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
    # Do nothing if the guild has clients left.
    if guild.clients:
        return
    
    satori_channel = get_log_satori_channel(guild.id)
    if (satori_channel is not None):
        clear_satori_channel(satori_channel)


@MAIN_CLIENT.events
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


@MAIN_CLIENT.events
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
        return
    
    set_satori_channel(channel.id, user_id)
    await create_initial_message(client, channel, user_id)


@MAIN_CLIENT.events
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
    
    # Moved ?
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
                await create_initial_message(client, channel, user_id)
            return
    
    if channel.parent_id != satori_channel.id:
        return
    
    # renamed ?
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
            await create_initial_message(client, channel, user_id)


@MAIN_CLIENT.events
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
        if channel.cached_permissions_for(client) & REQUIRED_PERMISSIONS != REQUIRED_PERMISSIONS:
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


@MAIN_CLIENT.events
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
            return
    
    # Channel not found -> create
    
    # Check channel permissions
    if satori_channel.cached_permissions_for(client) & REQUIRED_PERMISSIONS != REQUIRED_PERMISSIONS:
        return
    
    try:
        # No need to pass permission overwrites, seems like it is auto inherited from parent.
        await client.channel_create(
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


async def create_initial_message(client, channel, user_id):
    """
    Creates the initial satori message.

    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    channel : ``Channel``
        The created channel.
    user_id : `int`
        The user's identifier.
    """
    # Check permissions of the new channel
    if channel.cached_permissions_for(client) & REQUIRED_PERMISSIONS != REQUIRED_PERMISSIONS:
        return
    
    # Try get user
    try:
        user = await client.user_get(user_id)
    except (GeneratorExit, CancelledError):
        raise
    except ConnectionError:
        return
    except DiscordException as err:
        if err.code == ERROR_CODES.unknown_user:
            return
        
        raise
    
    # Send message
    try:
        await client.message_create(
            channel,
            allowed_mentions = None,
            components = build_satori_auto_start_component_row(user),
            embed = build_satori_auto_start_embeds(user, channel.guild_id),
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
        
        await client.events.error(client, 'log.satori.create_initial_message', err)
        return


@MAIN_CLIENT.events
async def guild_user_update(client, guild, user, old_attributes):
    """
    Handles a user guild profile update event. If the user is watched sends a message to every watching channel.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    guild : ``Guild``
        The guild where the user was updated at.
    user : ``ClientUserBase``
        The updated user.
    old_attributes : `None`, `dict` of (`str` `object`) items
        The user's guild profile's old attributes.
    """
    channels = get_watcher_channels_for(user.id)
    if channels is None:
        return
    
    # We want to send messages only in channels in the current guild!
    channels = [channel for channel in channels if channel.guild_id == guild.id]
    if (not channels):
        return
    
    if old_attributes is None:
        return
    
    guild_profile = user.get_guild_profile_for(guild)
    if guild_profile is None:
        return
    
    embed = build_guild_profile_update_embed(guild_profile, old_attributes)
    
    for channel in channels:
        if channel.cached_permissions_for(client) & REQUIRED_PERMISSIONS != REQUIRED_PERMISSIONS:
            continue
        
        try:
            await client.message_create(
                channel,
                allowed_mentions = None,
                embed = embed,
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
