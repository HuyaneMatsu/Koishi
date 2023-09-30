__all__ = ()

from collections import OrderedDict


CHARACTER_PREFERENCE_CACHE = OrderedDict()
CHARACTER_PREFERENCE_CACHE_MAX_SIZE = 1000


def get_one_from_cache(user_id):
    """
    Tries to get the given `user_id` from the cache.
    
    Parameters
    ----------
    user_id : `int`
        The user identifier to get character preferences for.
    
    Returns
    -------
    result : `None | list<CharacterPreference>`
        The hit character preference(s).
    miss : `bool`
        Whether we hit.
    """
    try:
        result = CHARACTER_PREFERENCE_CACHE[user_id]
    except KeyError:
        miss = True
        result = None
    else:
        miss = False
        CHARACTER_PREFERENCE_CACHE.move_to_end(user_id)
    
    return result, miss


def get_more_from_cache(user_ids):
    """
    Tries to get multiple `user_id`-s from the cache.
    
    Parameters
    ----------
    user_ids : `list<int>`
        User identifiers to get character preferences for.
    
    Returns
    -------
    results : `None | list<CharacterPreference>`
        The hit character preferences.
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
            if (result is not None):
                if results is None:
                    results = []
                results.extend(result)
    
    return results, misses


def put_one_to_cache(user_id, result):
    """
    Puts the character preferences into the cache.
    
    Parameters
    ----------
    user_id : `int`
        User identifier to use.
    result : `None | list<CharacterPreference>`
        Character preferences to put into the cache.
    """
    CHARACTER_PREFERENCE_CACHE[user_id] = result
    CHARACTER_PREFERENCE_CACHE.move_to_end(user_id)
    
    if len(CHARACTER_PREFERENCE_CACHE) > CHARACTER_PREFERENCE_CACHE_MAX_SIZE:
        del CHARACTER_PREFERENCE_CACHE[next(iter(CHARACTER_PREFERENCE_CACHE))]


def put_more_to_cache(user_ids, results):
    """
    Puts character preferences of multiple users into the cache.
    
    Parameters
    ----------
    user_ids : `list<int>`
        User identifiers to use.
    results : `None | list<CharacterPreference>`
        Character preferences to put into the cache.
    """
    if results is None:
        for user_id in user_ids:
            put_one_to_cache(user_id, None)
    else:
        by_user_id = {}
        for entry in results:
            user_id = entry.user_id
            try:
                result = by_user_id[user_id]
            except KeyError:
                result = []
                by_user_id[user_id] = result
            
            result.append(entry)
        
        for user_id in user_ids:
            put_one_to_cache(user_id, by_user_id.get(user_id, None))


def add_to_cache(character_preference):
    """
    Adds one preference to cache.
    
    Parameters
    ----------
    character_preference : ``CharacterPreference``
        The character preference to add.
    """
    user_id = character_preference.user_id
    
    try:
        result = CHARACTER_PREFERENCE_CACHE[user_id]
    except KeyError:
        # Do not save to cache, if we dont know the existing entries do nothing.
        return
    
    if result is None:
        result = []
        CHARACTER_PREFERENCE_CACHE[user_id] = result
    
    result.append(character_preference)
    

def remove_from_cache(character_preference):
    """
    Removes one preference from cache.
    
    Parameters
    ----------
    character_preference : ``CharacterPreference``
        The character preference to remove.
    """
    user_id = character_preference.user_id
    
    try:
        result = CHARACTER_PREFERENCE_CACHE[user_id]
    except KeyError:
        # Do not save to cache, if we dont know the existing entries do nothing.
        return
    
    # No entries, nothing to remove from
    if result is None:
        return
    
    try:
        result.remove(character_preference)
    except ValueError:
        # We did not have this entry.
        return
    
    # We removed the entry. Replaces the entries `list` to `None` if we have `0`.
    if not result:
        CHARACTER_PREFERENCE_CACHE[user_id] = None
