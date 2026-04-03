__all__ = ()

from .constants import WELCOME_CACHE, WELCOME_CACHE_MAX_SIZE


def is_welcome_in_cache(guild_id, welcomed_id):
    """
    Checks whether a welcome action is in the cache.
    
    Parameters
    ----------
    guild_id : `int`
        The guild's identifier where the user is welcomed.
    
    welcomed_id : `int`
        The welcomed user's identifier.
    
    Returns
    -------
    in_cache : `bool`
    """
    unit = (guild_id, welcomed_id)
    
    try:
        WELCOME_CACHE.move_to_end(unit)
    except KeyError:
        return False
    
    return True


def put_welcome_in_cache(guild_id, welcomed_id):
    """
    Checks whether a welcome action is in the cache. If it is not adds it obviously.
    
    Parameters
    ----------
    guild_id : `int`
        The guild's identifier where the user is welcomed.
    
    welcomed_id : `int`
        The welcomed user's identifier.
    
    Returns
    -------
    in_cache : `bool`
    """
    unit = (guild_id, welcomed_id)
    
    try:
        WELCOME_CACHE.move_to_end(unit)
    except KeyError:
        pass
    else:
        return True
    
    if len(WELCOME_CACHE) == WELCOME_CACHE_MAX_SIZE:
        del WELCOME_CACHE[next(iter(WELCOME_CACHE))]
    
    WELCOME_CACHE[unit] = None
    return False
