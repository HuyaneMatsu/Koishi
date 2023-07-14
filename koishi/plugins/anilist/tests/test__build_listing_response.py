import vampytest
from hata import Embed
from hata.ext.slash import InteractionResponse, Option, Row

from ..constants import (
    COMPONENT_LEFT_ANIME, COMPONENT_LEFT_CHARACTER, COMPONENT_LEFT_DISABLED, COMPONENT_LEFT_MANGA,
    COMPONENT_RIGHT_ANIME, COMPONENT_RIGHT_CHARACTER, COMPONENT_RIGHT_DISABLED, COMPONENT_RIGHT_MANGA,
    COMPONENT_SELECT_ANIME, COMPONENT_SELECT_CHARACTER, COMPONENT_SELECT_MANGA, URL_BASE_ANIME, URL_BASE_CHARACTER,
    URL_BASE_MANGA
)
from ..keys import (
    KEY_CHARACTER_ARRAY, KEY_CHARACTER_ID, KEY_CHARACTER_NAME, KEY_CHARACTER_NAME_FIRST, KEY_MEDIA_ARRAY, KEY_MEDIA_ID,
    KEY_MEDIA_NAME, KEY_MEDIA_NAME_ROMAJI, KEY_PAGE, KEY_PAGE_INFO, KEY_PAGE_INFO_CURRENT_PAGE_IDENTIFIER,
    KEY_PAGE_INFO_TOTAL_PAGES
)
from ..parsers_components import parse_page_info_components_character, parse_select_character
from ..parsers_description import parse_listing_character
from ..response_building_listing import (
    build_listing_response_anime, build_listing_response_base, build_listing_response_character,
    build_listing_response_manga
)


def _iter_options__build_listing_response_base():
    yield (
        {
            'data': {
                KEY_PAGE: {
                    KEY_CHARACTER_ARRAY: None,
                    KEY_PAGE_INFO: {},
                },
            }
        },
        'satori',
        KEY_CHARACTER_ARRAY,
        parse_listing_character,
        parse_select_character,
        parse_page_info_components_character,
        InteractionResponse(
            allowed_mentions = None,
            embed = Embed('Search result for: satori', 'No result.'),
            components = [
                COMPONENT_SELECT_CHARACTER.copy_with(
                    options = [Option('-1', 'No result', default = True)],
                    enabled = False,
                ),
                Row(COMPONENT_LEFT_DISABLED, COMPONENT_RIGHT_DISABLED),
            ]
        )
    )
    
    yield (
        {
            'data': {
                KEY_PAGE: {
                    KEY_CHARACTER_ARRAY: [
                        {
                            KEY_CHARACTER_NAME: {
                                KEY_CHARACTER_NAME_FIRST: 'orin',
                            },
                            KEY_CHARACTER_ID: 56,
                        }, {
                            KEY_CHARACTER_NAME: {
                                KEY_CHARACTER_NAME_FIRST: 'okuu',
                            },
                            KEY_CHARACTER_ID: 69,
                        },
                    ],
                    KEY_PAGE_INFO:
                    {
                        KEY_PAGE_INFO_CURRENT_PAGE_IDENTIFIER: 2,
                        KEY_PAGE_INFO_TOTAL_PAGES: 3,
                    },
                }
            }
        },
        'satori',
        KEY_CHARACTER_ARRAY,
        parse_listing_character,
        parse_select_character,
        parse_page_info_components_character,
        InteractionResponse(
            allowed_mentions = None,
            embed = Embed(
                'Search result for: satori',
                (
                    f'[orin]({URL_BASE_CHARACTER}{56})\n'
                    f'[okuu]({URL_BASE_CHARACTER}{69})'
                ),
            ),
            components = [
                COMPONENT_SELECT_CHARACTER.copy_with(
                    options = [
                        Option(
                            str(56),
                            'orin',
                        ),
                        Option(
                            str(69),
                            'okuu',
                        )
                    ],
                ),
                Row(COMPONENT_LEFT_CHARACTER, COMPONENT_RIGHT_CHARACTER),
            ]
        )
    )


@vampytest._(vampytest.call_from(_iter_options__build_listing_response_base()).returning_last())
def test__build_listing_response_base(
    data, search_term, key_listing, listing_parser, select_parser, page_info_components_parser
):
    """
    Tests whether ``build_listing_response_base`` works as intended.
    
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
    return build_listing_response_base(
        data, search_term, key_listing, listing_parser, select_parser, page_info_components_parser
    )


def _iter_options__build_listing_response_character():
    yield (
        {
            'data': {
                KEY_PAGE: {
                    KEY_CHARACTER_ARRAY: None,
                    KEY_PAGE_INFO: {},
                },
            }
        },
        'satori',
        InteractionResponse(
            allowed_mentions = None,
            embed = Embed('Search result for: satori', 'No result.'),
            components = [
                COMPONENT_SELECT_CHARACTER.copy_with(
                    options = [Option('-1', 'No result', default = True)],
                    enabled = False,
                ),
                Row(COMPONENT_LEFT_DISABLED, COMPONENT_RIGHT_DISABLED),
            ]
        )
    )
    
    yield (
        {
            'data': {
                KEY_PAGE: {
                    KEY_CHARACTER_ARRAY: [
                        {
                            KEY_CHARACTER_NAME: {
                                KEY_CHARACTER_NAME_FIRST: 'orin',
                            },
                            KEY_CHARACTER_ID: 56,
                        }, {
                            KEY_CHARACTER_NAME: {
                                KEY_CHARACTER_NAME_FIRST: 'okuu',
                            },
                            KEY_CHARACTER_ID: 69,
                        },
                    ],
                    KEY_PAGE_INFO:
                    {
                        KEY_PAGE_INFO_CURRENT_PAGE_IDENTIFIER: 2,
                        KEY_PAGE_INFO_TOTAL_PAGES: 3,
                    },
                }
            }
        },
        'satori',
        InteractionResponse(
            allowed_mentions = None,
            embed = Embed(
                'Search result for: satori',
                (
                    f'[orin]({URL_BASE_CHARACTER}{56})\n'
                    f'[okuu]({URL_BASE_CHARACTER}{69})'
                ),
            ),
            components = [
                COMPONENT_SELECT_CHARACTER.copy_with(
                    options = [
                        Option(
                            str(56),
                            'orin',
                        ),
                        Option(
                            str(69),
                            'okuu',
                        )
                    ],
                ),
                Row(COMPONENT_LEFT_CHARACTER, COMPONENT_RIGHT_CHARACTER),
            ]
        )
    )


@vampytest._(vampytest.call_from(_iter_options__build_listing_response_character()).returning_last())
def test__build_listing_response_character(data, search_term):
    """
    Tests whether ``build_listing_response_character`` works as intended.
    
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
    return build_listing_response_character(data, search_term)


def _iter_options__build_listing_response_anime():
    yield (
        {
            'data': {
                KEY_PAGE: {
                    KEY_MEDIA_ARRAY: None,
                    KEY_PAGE_INFO: {},
                },
            }
        },
        'satori',
        InteractionResponse(
            allowed_mentions = None,
            embed = Embed('Search result for: satori', 'No result.'),
            components = [
                COMPONENT_SELECT_ANIME.copy_with(
                    options = [Option('-1', 'No result', default = True)],
                    enabled = False,
                ),
                Row(COMPONENT_LEFT_DISABLED, COMPONENT_RIGHT_DISABLED),
            ]
        )
    )
    
    yield (
        {
            'data': {
                KEY_PAGE: {
                    KEY_MEDIA_ARRAY: [
                        {
                            KEY_MEDIA_NAME: {
                                KEY_MEDIA_NAME_ROMAJI: 'orin',
                            },
                            KEY_MEDIA_ID: 56,
                        }, {
                            KEY_MEDIA_NAME: {
                                KEY_MEDIA_NAME_ROMAJI: 'okuu',
                            },
                            KEY_MEDIA_ID: 69,
                        },
                    ],
                    KEY_PAGE_INFO:
                    {
                        KEY_PAGE_INFO_CURRENT_PAGE_IDENTIFIER: 2,
                        KEY_PAGE_INFO_TOTAL_PAGES: 3,
                    },
                }
            }
        },
        'satori',
        InteractionResponse(
            allowed_mentions = None,
            embed = Embed(
                'Search result for: satori',
                (
                    f'[orin]({URL_BASE_ANIME}{56})\n'
                    f'[okuu]({URL_BASE_ANIME}{69})'
                ),
            ),
            components = [
                COMPONENT_SELECT_ANIME.copy_with(
                    options = [
                        Option(
                            str(56),
                            'orin',
                        ),
                        Option(
                            str(69),
                            'okuu',
                        )
                    ],
                ),
                Row(COMPONENT_LEFT_ANIME, COMPONENT_RIGHT_ANIME),
            ]
        )
    )


@vampytest._(vampytest.call_from(_iter_options__build_listing_response_anime()).returning_last())
def test__build_listing_response_anime(data, search_term):
    """
    Tests whether ``build_listing_response_anime`` works as intended.
    
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
    return build_listing_response_anime(data, search_term)


def _iter_options__build_listing_response_manga():
    yield (
        {
            'data': {
                KEY_PAGE: {
                    KEY_MEDIA_ARRAY: None,
                    KEY_PAGE_INFO: {},
                },
            }
        },
        'satori',
        InteractionResponse(
            allowed_mentions = None,
            embed = Embed('Search result for: satori', 'No result.'),
            components = [
                COMPONENT_SELECT_MANGA.copy_with(
                    options = [Option('-1', 'No result', default = True)],
                    enabled = False,
                ),
                Row(COMPONENT_LEFT_DISABLED, COMPONENT_RIGHT_DISABLED),
            ]
        )
    )
    
    yield (
        {
            'data': {
                KEY_PAGE: {
                    KEY_MEDIA_ARRAY: [
                        {
                            KEY_MEDIA_NAME: {
                                KEY_MEDIA_NAME_ROMAJI: 'orin',
                            },
                            KEY_MEDIA_ID: 56,
                        }, {
                            KEY_MEDIA_NAME: {
                                KEY_MEDIA_NAME_ROMAJI: 'okuu',
                            },
                            KEY_MEDIA_ID: 69,
                        },
                    ],
                    KEY_PAGE_INFO:
                    {
                        KEY_PAGE_INFO_CURRENT_PAGE_IDENTIFIER: 2,
                        KEY_PAGE_INFO_TOTAL_PAGES: 3,
                    },
                }
            }
        },
        'satori',
        InteractionResponse(
            allowed_mentions = None,
            embed = Embed(
                'Search result for: satori',
                (
                    f'[orin]({URL_BASE_MANGA}{56})\n'
                    f'[okuu]({URL_BASE_MANGA}{69})'
                ),
            ),
            components = [
                COMPONENT_SELECT_MANGA.copy_with(
                    options = [
                        Option(
                            str(56),
                            'orin',
                        ),
                        Option(
                            str(69),
                            'okuu',
                        )
                    ],
                ),
                Row(COMPONENT_LEFT_MANGA, COMPONENT_RIGHT_MANGA),
            ]
        )
    )


@vampytest._(vampytest.call_from(_iter_options__build_listing_response_manga()).returning_last())
def test__build_listing_response_manga(data, search_term):
    """
    Tests whether ``build_listing_response_manga`` works as intended.
    
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
    return build_listing_response_manga(data, search_term)
