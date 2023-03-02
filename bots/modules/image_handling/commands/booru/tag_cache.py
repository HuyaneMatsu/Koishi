__all__ = ()

from collections import OrderedDict

from ...constants import (
    NSFW_BOORU_AUTOCOMPLETE_ENDPOINT, NSFW_BOORU_AUTOCOMPLETE_PARAMETERS, NSFW_BOORU_AUTOCOMPLETE_QUERY_KEY,
    NSFW_TAGS_BANNED, SAFE_BOORU_AUTOCOMPLETE_ENDPOINT, SAFE_BOORU_AUTOCOMPLETE_PARAMETERS,
    SAFE_BOORU_AUTOCOMPLETE_QUERY_KEY, SAFE_TAGS_BANNED
)

from .helpers import build_tag_gel_booru, build_tag_safe_booru


CACHE_MAX_SIZE = 1000

SAFE_BOORU_TAG_CACHE = OrderedDict()
NSFW_BOORU_TAG_CACHE = OrderedDict()


async def get_tag_auto_completion(client, query, safe, excluded_tags):
    """
    Gets the auto completion suggestions for the given query.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client to use to request the tags.
    query : `str`
        The value to autocomplete.
    safe : `bool`
        Whether we are using safe-booru.
    excluded_tags : `set` of `str`
        Additionally excluded tags.
    
    Returns
    -------
    tag_names : `None`, `list` of `str`
        Autocomplete suggestions.
    """
    if safe:
        cache = SAFE_BOORU_TAG_CACHE
    else:
        cache = NSFW_BOORU_TAG_CACHE
    
    try:
        tag_name_value_pairs = cache[query]
    except KeyError:
        tag_name_value_pairs = await request_tag_auto_completion(client, query, safe)
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


async def request_tag_auto_completion(client, query, safe):
    """
    Requests the auto completion suggestions for the given query.
    
    Parameters
    ----------
    client : ``Client``
        The client to use to request the tags.
    query : `str`
        The value to autocomplete.
    safe : `bool`
        Whether we are using safe-booru.
    
    Returns
    -------
    tag_name_value_pairs : `None`, `list` of `tuple` (`str`, `str`)
        Autocomplete suggestions.
    """
    if safe:
        tag_builder = build_tag_safe_booru
        tags_banned = SAFE_TAGS_BANNED
        endpoint = SAFE_BOORU_AUTOCOMPLETE_ENDPOINT
        query_parameters = SAFE_BOORU_AUTOCOMPLETE_PARAMETERS.copy()
        query_key = SAFE_BOORU_AUTOCOMPLETE_QUERY_KEY
    else:
        tag_builder = build_tag_gel_booru
        tags_banned = NSFW_TAGS_BANNED
        endpoint = NSFW_BOORU_AUTOCOMPLETE_ENDPOINT
        query_parameters = NSFW_BOORU_AUTOCOMPLETE_PARAMETERS.copy()
        query_key = NSFW_BOORU_AUTOCOMPLETE_QUERY_KEY
    
    query_parameters[query_key] = query
    
    async with client.http.get(endpoint, params = query_parameters) as response:
        if response.status != 200:
            return
        
        tag_datas = await response.json()
    
    return [tag_builder(tag_data) for tag_data in tag_datas if tag_data['value'] not in tags_banned]
