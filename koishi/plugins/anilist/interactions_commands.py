__all__ = ()

from hata.ext.slash import InteractionResponse, P

from ...bots import SLASH_CLIENT

from .anilist_api import search
from .constants import PARAMETER_LENGTH_MAX
from .embed_building_character import build_embed_character
from .embed_building_media import build_embed_anime, build_embed_manga
from .keys import (
    KEY_QUERY, KEY_VARIABLES, KEY_VARIABLE_CHARACTER_ID, KEY_VARIABLE_MEDIA_ID, KEY_VARIABLE_MEDIA_QUERY,
    KEY_VARIABLE_PAGE_IDENTIFIER
)
from .queries import (
    KEY_VARIABLE_CHARACTER_QUERY, QUERY_ANIME, QUERY_ANIME_ARRAY, QUERY_ANIME_BY_ID, QUERY_CHARACTER,
    QUERY_CHARACTER_ARRAY, QUERY_CHARACTER_BY_ID, QUERY_MANGA, QUERY_MANGA_ARRAY, QUERY_MANGA_BY_ID
)
from .response_building_listing import (
    build_listing_response_anime, build_listing_response_character, build_listing_response_manga
)


# ---- Anime ----

@SLASH_CLIENT.interactions(is_global = True, name = 'anime')
async def show_anime(
    client,
    name_or_id: P(str, 'The anime\'s name or it\'s id.', max_length = PARAMETER_LENGTH_MAX)
):
    """
    Shows a single anime. Query it either by name or id.
    
    This function is a coroutine generator.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    name_or_id : `str`
        The name of the anime or its identifier.
    
    Yields
    ------
    acknowledge / response : `None` / ``InteractionResponse``
    """
    if name_or_id.isdecimal():
        json_query = {
            KEY_QUERY: QUERY_ANIME_BY_ID,
            KEY_VARIABLES: {
                KEY_VARIABLE_MEDIA_ID: int(name_or_id),
            },
        }
    else:
        json_query = {
            KEY_QUERY: QUERY_ANIME,
            KEY_VARIABLES: {
                KEY_VARIABLE_MEDIA_QUERY: name_or_id,
            },
        }
    
    yield 
    data = await search(
        client,
        json_query,
    )
    yield InteractionResponse(
        allowed_mentions = None,
        embed = build_embed_anime(data),
    )


@SLASH_CLIENT.interactions(is_global = True)
async def find_anime(
    client,
    name: P(str, 'The anime\'s name to try to find.', max_length = PARAMETER_LENGTH_MAX)
):
    """
    Finds the animes matching the given name.
    
    This function is a coroutine generator.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    name : `str`
        The value to match.
    
    Yields
    ------
    acknowledge / response : `None` / ``InteractionResponse``
    """
    yield
    data = await search(
        client,
        {
            KEY_QUERY: QUERY_ANIME_ARRAY,
            KEY_VARIABLES: {
                KEY_VARIABLE_PAGE_IDENTIFIER: 1,
                KEY_VARIABLE_MEDIA_QUERY: name,
            },
        },
    )
    yield build_listing_response_anime(data, name)


# ---- Character ----


@SLASH_CLIENT.interactions(is_global = True, name = 'character')
async def show_character(
    client,
    name_or_id: P(str, 'The character\'s name or it\'s id.', max_length = PARAMETER_LENGTH_MAX)
):
    """
    Shows a single character. Query it either by name or id.
    
    This function is a coroutine generator.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    name_or_id : `str`
        The name of the character or its identifier.
    
    Yields
    ------
    acknowledge / response : `None` / ``InteractionResponse``
    """
    if name_or_id.isdecimal():
        json_query = {
            KEY_QUERY: QUERY_CHARACTER_BY_ID,
            KEY_VARIABLES: {
                KEY_VARIABLE_CHARACTER_ID: int(name_or_id),
            },
        }
    else:
        json_query = {
            KEY_QUERY: QUERY_CHARACTER,
            KEY_VARIABLES: {
                KEY_VARIABLE_CHARACTER_QUERY: name_or_id,
            },
        }
    
    yield
    data = await search(
        client,
        json_query,
    )
    yield InteractionResponse(
        allowed_mentions = None,
        embed = build_embed_character(data),
    )


@SLASH_CLIENT.interactions(is_global = True)
async def find_character(
    client,
    name: P(str, 'The character\'s name to try to find.', max_length = PARAMETER_LENGTH_MAX)
):
    """
    Finds the characters matching the given name.
    
    This function is a coroutine generator.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    name : `str`
        The value to match.
    
    Yields
    ------
    acknowledge / response : `None` / ``InteractionResponse``
    """
    yield
    data = await search(
        client,
        {
            KEY_QUERY: QUERY_CHARACTER_ARRAY,
            KEY_VARIABLES: {
                KEY_VARIABLE_PAGE_IDENTIFIER: 1,
                KEY_VARIABLE_CHARACTER_QUERY: name,
            },
        },
    )
    yield build_listing_response_character(data, name)


# ---- Manga ----


@SLASH_CLIENT.interactions(is_global = True, name = 'manga')
async def show_manga(
    client,
    name_or_id: P(str, 'The manga\'s name or it\'s id.', max_length = PARAMETER_LENGTH_MAX)
):
    """
    Shows a single manga. Query it either by name or id.
    
    This function is a coroutine generator.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    name_or_id : `str`
        The name of the manga or its identifier.
    
    Yields
    ------
    acknowledge / response : `None` / ``InteractionResponse``
    """
    if name_or_id.isdecimal():
        json_query = {
            KEY_QUERY: QUERY_MANGA_BY_ID,
            KEY_VARIABLES: {
                KEY_VARIABLE_MEDIA_ID: int(name_or_id),
            },
        }
    else:
        json_query = {
            KEY_QUERY: QUERY_MANGA,
            KEY_VARIABLES: {
                KEY_VARIABLE_MEDIA_QUERY: name_or_id,
            },
        }
    
    yield
    data = await search(
        client,
        json_query,
    )
    yield InteractionResponse(
        allowed_mentions = None,
        embed = build_embed_manga(data),
    )


@SLASH_CLIENT.interactions(is_global = True)
async def find_manga(
    client,
    name: P(str, 'The manga\'s name to try to find.', max_length = PARAMETER_LENGTH_MAX)
):
    """
    Finds the mangas matching the given name.
    
    This function is a coroutine generator.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    name : `str`
        The value to match.
    
    Yields
    ------
    acknowledge / response : `None` / ``InteractionResponse``
    """
    yield
    data = await search(
        client,
        {
            KEY_QUERY: QUERY_MANGA_ARRAY,
            KEY_VARIABLES: {
                KEY_VARIABLE_PAGE_IDENTIFIER: 1,
                KEY_VARIABLE_MEDIA_QUERY: name,
            },
        },
    )
    yield build_listing_response_manga(data, name)
