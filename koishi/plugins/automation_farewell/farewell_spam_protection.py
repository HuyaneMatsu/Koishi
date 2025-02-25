__all__ = ()

from .constants import FAREWELL_CACHE, FAREWELL_CACHE_MAX_SIZE


def is_farewell_in_cache(guild_id, farewelled_id):
    """
    Checks whether a farewell action is in the cache.
    
    Parameters
    ----------
    guild_id : `int`
        The guild's identifier where the user is farewelled.
    
    farewelled_id : `int`
        The farewelled user's identifier.
    
    Returns
    -------
    in_cache : `bool`
    """
    unit = (guild_id, farewelled_id)
    
    try:
        FAREWELL_CACHE.move_to_end(unit)
    except KeyError:
        return False
    
    return True


def put_farewell_in_cache(guild_id, farewelled_id):
    """
    Checks whether a farewell action is in the cache. If it is not adds it obviously.
    
    Parameters
    ----------
    guild_id : `int`
        The guild's identifier where the user is farewelled.
    
    farewelled_id : `int`
        The farewelled user's identifier.
    
    Returns
    -------
    in_cache : `bool`
    """
    unit = (guild_id, farewelled_id)
    
    try:
        FAREWELL_CACHE.move_to_end(unit)
    except KeyError:
        pass
    else:
        return True
    
    if len(FAREWELL_CACHE) == FAREWELL_CACHE_MAX_SIZE:
        del FAREWELL_CACHE[next(iter(FAREWELL_CACHE))]
    
    FAREWELL_CACHE[unit] = None
    return False
