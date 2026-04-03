__all__ = ()

from collections import OrderedDict

from ..image_handling_core import (
    get_autocompletion_suggestions_safe_booru, get_autocompletion_suggestions_dan_booru,
    NSFW_TAGS_BANNED, SAFE_TAGS_BANNED,
)


CACHE_MAX_SIZE = 1000

SAFE_BOORU_TAG_CACHE = OrderedDict()
NSFW_BOORU_TAG_CACHE = OrderedDict()


async def get_tag_auto_completion(query, safe, excluded_tags):
    """
    Gets the auto completion suggestions for the given query.
    
    This function is a coroutine.
    
    Parameters
    ----------
    query : `str`
        The value to autocomplete.
    
    safe : `bool`
        Whether we are using safe-booru.
    
    excluded_tags : `set<str>`
        Additionally excluded tags.
    
    Returns
    -------
    tag_names : `None | list<str>`
        Autocomplete suggestions.
    """
    if safe:
        cache = SAFE_BOORU_TAG_CACHE
    else:
        cache = NSFW_BOORU_TAG_CACHE
    
    try:
        tag_name_value_pairs = cache[query]
    except KeyError:
        tag_name_value_pairs = await request_tag_auto_completion(query, safe)
        if tag_name_value_pairs is None:
            return None
        
        if len(cache) == CACHE_MAX_SIZE:
            del cache[next(iter(cache))]
        
        cache[query] = tag_name_value_pairs
    
    else:
        cache.move_to_end(query)
    
    return [
        tag_name_value_pair[0] for tag_name_value_pair in tag_name_value_pairs
        if tag_name_value_pair[1] not in excluded_tags
    ]


async def request_tag_auto_completion(query, safe):
    """
    Requests the auto completion suggestions for the given query.
    
    Parameters
    ----------
    query : `str`
        The value to autocomplete.
        
    safe : `bool`
        Whether we are using safe-booru.
    
    Returns
    -------
    tag_name_value_pairs : `None | list<(str, str)>`
        Autocomplete suggestions.
    """
    if safe:
        function = get_autocompletion_suggestions_safe_booru
        banned_tags = SAFE_TAGS_BANNED
    else:
        function = get_autocompletion_suggestions_dan_booru
        banned_tags = NSFW_TAGS_BANNED
    
    return await function(query, banned_tags)
