__all__ = ()

from hata import CHANNELS

from .constants import SATORI_CHANNELS
from .operations import iter_log_satori_channels


def clear_satori_channels():
    """
    Clears all satori channels.
    """
    SATORI_CHANNELS.clear()


def reset_satori_channels():
    """
    Resets all satori channels.
    """
    clear_satori_channels()
    discover_satori_channels()


def set_satori_channel(channel_id, user_id):
    """
    Sets a satori channel.
    
    Parameters
    ----------
    channel_id : `int`
        The channel's identifier.
    user_id : `int`
        The watched user's identifier.
    """
    try:
        channel_ids = SATORI_CHANNELS[user_id]
    except KeyError:
        channel_ids = set()
        SATORI_CHANNELS[user_id] = channel_ids
    
    channel_ids.add(channel_id)


def discover_satori_channels():
    """
    Discovers all satori channels.
    """
    for satori_channel in iter_log_satori_channels():
        discover_satori_channel(satori_channel)


def clear_satori_channel(satori_channel):
    """
    Clears all watcher channels in the satori channel.
    
    Parameters
    ----------
    satori_channel : ``Channel``
        The channel to clear.
    """
    for channel in satori_channel.channel_list:
        try:
            user_id = int(channel.name)
        except ValueError:
            return
        else:
            remove_watcher_channel(channel.id, user_id)


def discover_satori_channel(satori_channel):
    """
    Discovers the satori channel.
    
    Parameters
    ----------
    satori_channel : ``Channel``
        The channel to discover.
    """
    for watcher_channel in satori_channel.channel_list:
        try:
            user_id = int(watcher_channel.name)
        except ValueError:
            continue
        else:
            set_satori_channel(watcher_channel.id, user_id)


def remove_watcher_channel(channel_id, user_id):
    """
    Removes a satori channel.
    
    Parameters
    ----------
    channel_id : `int`
        The channel's identifier.
    user_id : `int`
        The watched user's identifier.
    """
    try:
        channel_ids = SATORI_CHANNELS[user_id]
    except KeyError:
        pass
    
    else:
        try:
            channel_ids.remove(channel_id)
        except KeyError:
            pass
        else:
            if not channel_ids:
                try:
                    del SATORI_CHANNELS[user_id]
                except KeyError:
                    pass


def get_watcher_channels_for(user_id):
    """
    gets the satori channels for the given user identifier.
    
    Parameters
    ----------
    user_id : `int`
        A user's identifier.
    
    Returns
    -------
    channels : `None`, `list` of ``Channel``
    """
    try:
        channel_ids = SATORI_CHANNELS[user_id]
    except KeyError:
        return None
    
    channels = None
    channel_ids_to_discard = None
    
    for channel_id in channel_ids:
        try:
            channel = CHANNELS[channel_id]
        except KeyError:
            if channel_ids_to_discard is None:
                channel_ids_to_discard = []
            channel_ids_to_discard.append(channel_id)
        else:
            if channels is None:
                channels = []
            channels.append(channel)
    
    # All channel has been discarded?
    if channels is None:
        try:
            del SATORI_CHANNELS[user_id]
        except KeyError:
            pass
        
        return None
    
    # Are there discarded channels?
    if (channel_ids_to_discard is not None):
        for channel_id in channel_ids_to_discard:
            channel_ids.discard(channel_id)
    
    return channels
