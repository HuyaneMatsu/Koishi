__all__ = ()

from .constants import REPLY_CACHE, REPLY_CACHE_MAX_SIZE


def is_reply_in_cache(guild_id, welcome_message_id, welcomer_id):
    """
    Checks whether a reply action is in the cache.
    
    Parameters
    ----------
    guild_id : `int`
        The guild's identifier where we are replying at.
    welcome_message_id : `int`
        The welcome message's identifier.
    welcomer_id : `int`
        The welcomer user's identifier.
    
    Returns
    -------
    in_cache : `bool`
    """
    unit = (guild_id, welcome_message_id, welcomer_id)
    
    try:
        REPLY_CACHE.move_to_end(unit)
    except KeyError:
        return False
    
    return True


def put_reply_in_cache(guild_id, welcome_message_id, welcomer_id):
    """
    Checks whether a reply action is in the cache. If it is not adds it obviously.
    
    Parameters
    ----------
    guild_id : `int`
        The guild's identifier where we are replying at.
    welcome_message_id : `int`
        The welcome message's identifier.
    welcomer_id : `int`
        The welcomer user's identifier.
    
    Returns
    -------
    in_cache : `bool`
    """
    unit = (guild_id, welcome_message_id, welcomer_id)
    
    try:
        REPLY_CACHE.move_to_end(unit)
    except KeyError:
        pass
    else:
        return True
    
    if len(REPLY_CACHE) == REPLY_CACHE_MAX_SIZE:
        del REPLY_CACHE[next(iter(REPLY_CACHE))]
    
    REPLY_CACHE[unit] = None
    return False
