__all__ = ()

from hata import Permission


PERMISSION_MASK_MESSAGING__DEFAULT = Permission().update_by_keys(
    send_messages = True,
)

PERMISSION_MASK_MESSAGING__THREAD = Permission().update_by_keys(
    send_messages_in_threads = True,
)


def get_first_client_with_message_create_permissions_from(channel, client_wrapper, extra = 0):
    """
    Returns the first client who has message create permissions into the given channel.
    
    Parameters
    ----------
    chanel : ``Channel``
        Channel to check.
    client_wrapper : ``ClientWrapper``
        The allowed clients.
    extra : `int` = `0`, Optional
        Additional permissions to check for.
    
    Returns
    -------
    client : `None | Client`
    """
    if channel.is_in_group_thread():
        mask = PERMISSION_MASK_MESSAGING__THREAD
    else:
        mask = PERMISSION_MASK_MESSAGING__DEFAULT
    
    mask |= extra
    
    return get_first_client_with_permissions(channel, client_wrapper, mask)


def get_first_client_with_permissions(channel, client_wrapper, mask):
    """
    Returns the first client who has message create permissions into the given channel.
    
    Parameters
    ----------
    chanel : ``Channel``
        Channel to check.
    client_wrapper : ``ClientWrapper``
        The allowed clients.
    mask : `int`
        The permissions to check for.
    
    Returns
    -------
    client : `None | Client`
    """
    for client in channel.clients:
        if client not in client_wrapper:
            continue
        
        if channel.cached_permissions_for(client) & mask != mask:
            continue
        
        return client


def get_first_client_in_channel_from(channel, client_wrapper):
    """
    Returns the first client in the channel.
    
    Parameters
    ----------
    channel : ``Channel``
        The channel to get its first guild of.
    client_wrapper : ``ClientWrapper``
        The allowed clients.
    
    Returns
    -------
    client : `None | Client`
    """
    for client in channel.clients:
        if client in client_wrapper:
            return client


def get_first_client_in_guild_from(guild, client_wrapper):
    """
    Returns the first client in the guild.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild to get its first guild of.
    client_wrapper : ``ClientWrapper``
        The allowed clients.
    
    Returns
    -------
    client : `None | Client`
    """
    for client in guild.clients:
        if client in client_wrapper:
            return client
