__all__ = ()

from collections import OrderedDict

from .notification_settings import NotificationSettings


NOTIFICATION_SETTINGS_CACHE = OrderedDict()
NOTIFICATION_SETTINGS_CACHE_MAX_SIZE = 1000


def get_one_from_cache(user_id):
    """
    Tries to get the given `user_id` from the cache.
    
    Parameters
    ----------
    user_id : `int`
        The user identifier to get notification settings for.
    
    Returns
    -------
    result : `None | NotificationSettings`
        The hit notification settings.
    miss : `bool`
        Whether we hit.
    """
    try:
        result = NOTIFICATION_SETTINGS_CACHE[user_id]
    except KeyError:
        miss = True
        result = None
    else:
        miss = False
        NOTIFICATION_SETTINGS_CACHE.move_to_end(user_id)
        
        if result is None:
            result = NotificationSettings(user_id)
    
    return result, miss


def get_more_from_cache(user_ids):
    """
    Tries to get multiple `user_id`-s from the cache.
    
    Parameters
    ----------
    user_ids : `list<int>`
        User identifiers to get notification settings for.
    
    Returns
    -------
    results : `None | list<NotificationSettings>`
        The hit notification settings.
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
    Puts the notification settings into the cache.
    
    Parameters
    ----------
    result : `NotificationSettings`
        Character preferences to put into the cache.
    """
    user_id = result.user_id
    NOTIFICATION_SETTINGS_CACHE[user_id] = result
    NOTIFICATION_SETTINGS_CACHE.move_to_end(user_id)
    
    if len(NOTIFICATION_SETTINGS_CACHE) > NOTIFICATION_SETTINGS_CACHE_MAX_SIZE:
        del NOTIFICATION_SETTINGS_CACHE[next(iter(NOTIFICATION_SETTINGS_CACHE))]


def put_more_to_cache(results):
    """
    Puts notification settings of multiple users into the cache.
    
    Parameters
    ----------
    results : `None | list<NotificationSettings>`
        Character preferences to put into the cache.
    """
    if results is not None:
        for result in results:
            put_one_to_cache(result)


def put_none_to_cache(user_id):
    """
    Removes a notification settings from the cache.
    
    Parameters
    ----------
    user_id : `int`
        The user's respective identifier.
    """
    NOTIFICATION_SETTINGS_CACHE[user_id] = None
    NOTIFICATION_SETTINGS_CACHE.move_to_end(user_id)
    
    if len(NOTIFICATION_SETTINGS_CACHE) > NOTIFICATION_SETTINGS_CACHE_MAX_SIZE:
        del NOTIFICATION_SETTINGS_CACHE[next(iter(NOTIFICATION_SETTINGS_CACHE))]
