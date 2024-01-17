__all__ = ()

from collections import OrderedDict

from hata import KOKORO
from scarletio import Lock


CACHE = OrderedDict()

# Update cache size if we will have more guilds (we wont)
CACHE_SIZE = 100


def get_lock_for(message):
    """
    Adds the given message to cache.
    
    Parameters
    ----------
    message : ``Message``
        The message to get lock for.
    
    Returns
    -------
    lock : ``Lock``
    """
    try:
        lock = CACHE[message]
    except KeyError:
        lock = Lock(KOKORO)
        CACHE[message] = lock
        
        if len(CACHE) > CACHE_SIZE:
            del CACHE[next(iter(CACHE))]
    else:
        CACHE.move_to_end(message)
    
    return lock


def delete_lock_of(message):
    """
    Deletes the given message from the cache.
    
    Parameters
    ----------
    message : ``Message``
        the message to remove from cache.
    """
    CACHE.pop(message, None)
