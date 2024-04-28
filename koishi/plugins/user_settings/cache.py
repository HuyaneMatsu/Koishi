__all__ = ()

from collections import OrderedDict

from .user_settings import UserSettings


USER_SETTINGS_CACHE = OrderedDict()
USER_SETTINGS_CACHE_MAX_SIZE = 1000


def get_one_from_cache(user_id):
    """
    Tries to get the given `user_id` from the cache.
    
    Parameters
    ----------
    user_id : `int`
        The user identifier to get user settings for.
    
    Returns
    -------
    result : `None | UserSettings`
        The hit user settings.
    miss : `bool`
        Whether we hit.
    """
    try:
        result = USER_SETTINGS_CACHE[user_id]
    except KeyError:
        miss = True
        result = None
    else:
        miss = False
        USER_SETTINGS_CACHE.move_to_end(user_id)
        
        if result is None:
            result = UserSettings(user_id)
    
    return result, miss


def get_more_from_cache(user_ids):
    """
    Tries to get multiple `user_id`-s from the cache.
    
    Parameters
    ----------
    user_ids : `list<int>`
        User identifiers to get user settings for.
    
    Returns
    -------
    results : `None | list<UserSettings>`
        The hit user settings.
    misses : `None | list<int>`
        Missed `user_id`-s.
    """
    misses = None
    results = None
    
    for user_id in user_ids:
        result, miss = get_one_from_cache(user_id)
        if miss:
            if (misses is None):
                misses = []
            
            misses.append(user_id)
        else:
            if results is None:
                results = []
            results.append(result)
    
    return results, misses


def put_one_to_cache(result):
    """
    Puts the user settings into the cache.
    
    Parameters
    ----------
    result : `UserSettings`
        Character preferences to put into the cache.
    """
    user_id = result.user_id
    USER_SETTINGS_CACHE[user_id] = result
    USER_SETTINGS_CACHE.move_to_end(user_id)
    
    if len(USER_SETTINGS_CACHE) > USER_SETTINGS_CACHE_MAX_SIZE:
        del USER_SETTINGS_CACHE[next(iter(USER_SETTINGS_CACHE))]


def put_more_to_cache(results):
    """
    Puts user settings of multiple users into the cache.
    
    Parameters
    ----------
    results : `None | list<UserSettings>`
        Character preferences to put into the cache.
    """
    if results is not None:
        for result in results:
            put_one_to_cache(result)


def put_none_to_cache(user_id):
    """
    Removes a user settings from the cache.
    
    Parameters
    ----------
    user_id : `int`
        The user's respective identifier.
    """
    USER_SETTINGS_CACHE[user_id] = None
    USER_SETTINGS_CACHE.move_to_end(user_id)
    
    if len(USER_SETTINGS_CACHE) > USER_SETTINGS_CACHE_MAX_SIZE:
        del USER_SETTINGS_CACHE[next(iter(USER_SETTINGS_CACHE))]
