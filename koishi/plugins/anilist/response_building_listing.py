__all__ = ()

from hata import Embed
from hata.ext.slash import InteractionResponse

from .keys import KEY_CHARACTER_ARRAY, KEY_MEDIA_ARRAY, KEY_PAGE, KEY_PAGE_INFO
from .parsers_components import (
    parse_page_info_components_anime, parse_page_info_components_character, parse_page_info_components_manga,
    parse_select_anime, parse_select_character, parse_select_manga
)
from .parsers_description import parse_listing_anime, parse_listing_character, parse_listing_manga


def build_listing_response_base(
    data, search_term, key_listing, listing_parser, select_parser, page_info_components_parser
):
    """
    Builds a base listing response.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Response data.
    search_term : `str`
        The searched term.
    key_listing : `str`
        Key to use to get the listing.
    listing_parser : `FunctionType`
        Function to parse listing description with.
    select_parser : `FunctionType`
        Function to parse select with.
    page_info_components_parser : `FunctionType`
        function to parse page info with.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    page_data = data['data'][KEY_PAGE]
    character_array_data = page_data[key_listing]
    page_info_data = page_data[KEY_PAGE_INFO]
    
    description = listing_parser(character_array_data)
    if description is None:
        description = 'No result.'
    
    return InteractionResponse(
        allowed_mentions = None,
        embed = Embed(f'Search result for: {search_term}', description),
        components = [
            select_parser(character_array_data),
            page_info_components_parser(page_info_data),
        ],
    )


def build_listing_response_anime(data, search_term):
    """
    Builds anime listing response.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Response data.
    search_term : `str`
        The searched term.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    return build_listing_response_base(
        data,
        search_term,
        KEY_MEDIA_ARRAY,
        parse_listing_anime,
        parse_select_anime,
        parse_page_info_components_anime,
    )


def build_listing_response_character(data, search_term):
    """
    Builds character listing response.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Response data.
    search_term : `str`
        The searched term.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    return build_listing_response_base(
        data,
        search_term,
        KEY_CHARACTER_ARRAY,
        parse_listing_character,
        parse_select_character,
        parse_page_info_components_character,
    )


def build_listing_response_manga(data, search_term):
    """
    Builds manga listing response.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Response data.
    search_term : `str`
        The searched term.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    return build_listing_response_base(
        data,
        search_term,
        KEY_MEDIA_ARRAY,
        parse_listing_manga,
        parse_select_manga,
        parse_page_info_components_manga,
    )
