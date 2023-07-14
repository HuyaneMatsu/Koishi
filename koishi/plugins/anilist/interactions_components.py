__all__ = ()

from hata.ext.slash import InteractionResponse

from ...bots import SLASH_CLIENT

from .anilist_api import search
from .constants import (
    CUSTOM_ID_FIND_LEFT_ANIME, CUSTOM_ID_FIND_LEFT_CHARACTER, CUSTOM_ID_FIND_LEFT_DISABLED, CUSTOM_ID_FIND_LEFT_MANGA,
    CUSTOM_ID_FIND_RIGHT_ANIME, CUSTOM_ID_FIND_RIGHT_CHARACTER, CUSTOM_ID_FIND_RIGHT_DISABLED,
    CUSTOM_ID_FIND_RIGHT_MANGA, CUSTOM_ID_FIND_SELECT_ANIME, CUSTOM_ID_FIND_SELECT_CHARACTER,
    CUSTOM_ID_FIND_SELECT_MANGA
)
from .embed_building_character import build_embed_character
from .embed_building_media import build_embed_anime, build_embed_manga
from .helpers import get_name_and_page, get_selected_entity_id, is_event_user_same
from .keys import (
    KEY_QUERY, KEY_VARIABLES, KEY_VARIABLE_CHARACTER_ID, KEY_VARIABLE_MEDIA_ID, KEY_VARIABLE_MEDIA_QUERY,
    KEY_VARIABLE_PAGE_IDENTIFIER
)
from .queries import (
    KEY_VARIABLE_CHARACTER_QUERY, QUERY_ANIME_ARRAY, QUERY_ANIME_BY_ID, QUERY_CHARACTER_ARRAY, QUERY_CHARACTER_BY_ID,
    QUERY_MANGA_ARRAY, QUERY_MANGA_BY_ID
)
from .response_building_listing import (
    build_listing_response_anime, build_listing_response_character, build_listing_response_manga
)

# ---- Anime ----


@SLASH_CLIENT.interactions(custom_id = CUSTOM_ID_FIND_SELECT_ANIME)
async def find_anime_select(client, event):
    """
    Handles when an anime is selected.
    
    This function is a coroutine generator.
    
    Parameters
    ----------
    client : ``Client``
        The client who received event.
    event : ``InteractionEvent``
        The received interaction event.
    
    Yields
    ------
    acknowledge / response : `None` / ``InteractionResponse``
    """
    if not is_event_user_same(event):
        return
    
    anime_id = get_selected_entity_id(event)
    if anime_id == -1:
        return
    
    yield
    data = await search(
        client,
        {
            KEY_QUERY: QUERY_ANIME_BY_ID,
            KEY_VARIABLES: {
                KEY_VARIABLE_MEDIA_ID: anime_id,
            },
        },
    )
    yield InteractionResponse(
        allowed_mentions = None,
        components = None,
        embed = build_embed_anime(data),
    )


@SLASH_CLIENT.interactions(custom_id = CUSTOM_ID_FIND_LEFT_ANIME)
async def find_anime_page_left(client, event):
    """
    Handles when a left anime button is clicked.
    
    This function is a coroutine generator.
    
    Parameters
    ----------
    client : ``Client``
        The client who received event.
    event : ``InteractionEvent``
        The received interaction event.
    
    Yields
    ------
    acknowledge / response : `None` / ``InteractionResponse``
    """
    if not is_event_user_same(event):
        return
    
    name_and_page = get_name_and_page(event.message.embed)
    if name_and_page is None:
        return
    
    name, page_identifier = name_and_page
    page_identifier -= 1
    
    yield
    data = await search(
        client,
        {
            KEY_QUERY: QUERY_ANIME_ARRAY,
            KEY_VARIABLES: {
                KEY_VARIABLE_PAGE_IDENTIFIER: page_identifier,
                KEY_VARIABLE_MEDIA_QUERY: name,
            },
        },
    )
    yield build_listing_response_anime(data, name)


@SLASH_CLIENT.interactions(custom_id = CUSTOM_ID_FIND_RIGHT_ANIME)
async def find_anime_page_right(client, event):
    """
    Handles when a right anime button is clicked.
    
    This function is a coroutine generator.
    
    Parameters
    ----------
    client : ``Client``
        The client who received event.
    event : ``InteractionEvent``
        The received interaction event.
    
    Yields
    ------
    acknowledge / response : `None` / ``InteractionResponse``
    """
    if not is_event_user_same(event):
        return
    
    name_and_page = get_name_and_page(event.message.embed)
    if name_and_page is None:
        return
    
    name, page_identifier = name_and_page
    page_identifier += 1
    
    yield
    data = await search(
        client,
        {
            KEY_QUERY: QUERY_ANIME_ARRAY,
            KEY_VARIABLES: {
                KEY_VARIABLE_PAGE_IDENTIFIER: page_identifier,
                KEY_VARIABLE_MEDIA_QUERY: name,
            },
        },
    )
    yield build_listing_response_anime(data, name)



# ---- Character ----


@SLASH_CLIENT.interactions(custom_id = CUSTOM_ID_FIND_SELECT_CHARACTER)
async def find_character_select(client, event):
    """
    Handles when a character is selected.
    
    This function is a coroutine generator.
    
    Parameters
    ----------
    client : ``Client``
        The client who received event.
    event : ``InteractionEvent``
        The received interaction event.
    
    Yields
    ------
    acknowledge / response : `None` / ``InteractionResponse``
    """
    if not is_event_user_same(event):
        return
    
    character_id = get_selected_entity_id(event)
    if character_id == -1:
        return
    
    yield
    data = await search(
        client,
        {
            KEY_QUERY: QUERY_CHARACTER_BY_ID,
            KEY_VARIABLES: {
                KEY_VARIABLE_CHARACTER_ID: character_id,
            },
        },
    )
    yield InteractionResponse(
        allowed_mentions = None,
        components = None,
        embed = build_embed_character(data),
    )


@SLASH_CLIENT.interactions(custom_id = CUSTOM_ID_FIND_LEFT_CHARACTER)
async def find_character_page_left(client, event):
    """
    Handles when a left character button is clicked.
    
    This function is a coroutine generator.
    
    Parameters
    ----------
    client : ``Client``
        The client who received event.
    event : ``InteractionEvent``
        The received interaction event.
    
    Yields
    ------
    acknowledge / response : `None` / ``InteractionResponse``
    """
    if not is_event_user_same(event):
        return
    
    name_and_page = get_name_and_page(event.message.embed)
    if name_and_page is None:
        return
    
    name, page_identifier = name_and_page
    page_identifier -= 1
    
    yield 
    data = await search(
        client,
        {
            KEY_QUERY: QUERY_CHARACTER_ARRAY,
            KEY_VARIABLES: {
                KEY_VARIABLE_PAGE_IDENTIFIER: page_identifier,
                KEY_VARIABLE_CHARACTER_QUERY: name,
            },
        },
    )
    yield build_listing_response_character(data, name)


@SLASH_CLIENT.interactions(custom_id = CUSTOM_ID_FIND_RIGHT_CHARACTER)
async def find_character_page_right(client, event):
    """
    Handles when a right character button is clicked.
    
    This function is a coroutine generator.
    
    Parameters
    ----------
    client : ``Client``
        The client who received event.
    event : ``InteractionEvent``
        The received interaction event.
    
    Yields
    ------
    acknowledge / response : `None` / ``InteractionResponse``
    """
    if not is_event_user_same(event):
        return
    
    name_and_page = get_name_and_page(event.message.embed)
    if name_and_page is None:
        return
    
    name, page_identifier = name_and_page
    page_identifier += 1
    
    yield
    data = await search(
        client,
        {
            KEY_QUERY: QUERY_CHARACTER_ARRAY,
            KEY_VARIABLES: {
                KEY_VARIABLE_PAGE_IDENTIFIER: page_identifier,
                KEY_VARIABLE_CHARACTER_QUERY: name,
            },
        },
    )
    yield build_listing_response_character(data, name)


# ---- Manga ----


@SLASH_CLIENT.interactions(custom_id = CUSTOM_ID_FIND_SELECT_MANGA)
async def find_manga_select(client, event):
    """
    Handles when a manga is selected.
    
    This function is a coroutine generator.
    
    Parameters
    ----------
    client : ``Client``
        The client who received event.
    event : ``InteractionEvent``
        The received interaction event.
    
    Yields
    ------
    acknowledge / response : `None` / ``InteractionResponse``
    """
    if not is_event_user_same(event):
        return
    
    manga_id = get_selected_entity_id(event)
    if manga_id == -1:
        return
    
    yield
    data = await  search(
        client,
        {
            KEY_QUERY: QUERY_MANGA_BY_ID,
            KEY_VARIABLES: {
                KEY_VARIABLE_MEDIA_ID: manga_id,
            },
        },
    )
    yield InteractionResponse(
        allowed_mentions = None,
        components = None,
        embed = build_embed_manga(data),
    )


@SLASH_CLIENT.interactions(custom_id = CUSTOM_ID_FIND_LEFT_MANGA)
async def find_manga_page_left(client, event):
    """
    Handles when a left manga button is clicked.
    
    This function is a coroutine generator.
    
    Parameters
    ----------
    client : ``Client``
        The client who received event.
    event : ``InteractionEvent``
        The received interaction event.
    
    Yields
    ------
    acknowledge / response : `None` / ``InteractionResponse``
    """
    if not is_event_user_same(event):
        return
    
    name_and_page = get_name_and_page(event.message.embed)
    if name_and_page is None:
        return
    
    name, page_identifier = name_and_page
    page_identifier -= 1
    
    yield
    data = await search(
        client,
        {
            KEY_QUERY: QUERY_MANGA_ARRAY,
            KEY_VARIABLES: {
                KEY_VARIABLE_PAGE_IDENTIFIER: page_identifier,
                KEY_VARIABLE_MEDIA_QUERY: name,
            },
        },
    )
    yield build_listing_response_manga(data, name)


@SLASH_CLIENT.interactions(custom_id = CUSTOM_ID_FIND_RIGHT_MANGA)
async def find_manga_page_right(client, event):
    """
    Handles when a right manga button is clicked.
    
    This function is a coroutine generator.
    
    Parameters
    ----------
    client : ``Client``
        The client who received event.
    event : ``InteractionEvent``
        The received interaction event.
    
    Yields
    ------
    acknowledge / response : `None` / ``InteractionResponse``
    """
    if not is_event_user_same(event):
        return
    
    name_and_page = get_name_and_page(event.message.embed)
    if name_and_page is None:
        return
    
    name, page_identifier = name_and_page
    page_identifier += 1
    
    yield
    data = await search(
        client,
        {
            KEY_QUERY: QUERY_MANGA_ARRAY,
            KEY_VARIABLES: {
                KEY_VARIABLE_PAGE_IDENTIFIER: page_identifier,
                KEY_VARIABLE_MEDIA_QUERY: name,
            },
        },
    )
    yield build_listing_response_manga(data, name)


# ---- Generic ----


@SLASH_CLIENT.interactions(
    custom_id = [
        CUSTOM_ID_FIND_LEFT_DISABLED,
        CUSTOM_ID_FIND_RIGHT_DISABLED,
    ],
)
async def handle_disabled_component_interaction():
    """
    Dummy component interaction handler.
    
    Handles interactions that we should not receive.
    
    This function is a coroutine.
    """
    pass
