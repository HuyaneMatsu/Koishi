import vampytest

from ..constants import URL_BASE_ANIME, URL_BASE_CHARACTER, URL_BASE_MANGA
from ..keys import (
    KEY_CHARACTER_ID, KEY_CHARACTER_NAME, KEY_CHARACTER_NAME_FIRST, KEY_MEDIA_ID, KEY_MEDIA_NAME, KEY_MEDIA_NAME_ROMAJI,
    KEY_MEDIA_TYPE, KEY_MEDIA_TYPE_ANIME
)
from ..parsers_description import parse_listing_base, parse_listing_anime, parse_listing_manga, parse_listing_character
from ..parsers_name import parse_name_character, parse_name_media
from ..parsers_url import parse_url_anime, parse_url_character, parse_url_manga, parse_url_media


def _iter_options__parse_listing_base():
    yield (
        None,
        parse_name_media,
        parse_url_media,
        None,
    )
    yield (
        [],
        parse_name_media,
        parse_url_media,
        None,
    )
    yield (
        [
            {
                KEY_MEDIA_NAME: {
                    KEY_MEDIA_NAME_ROMAJI: 'Koishi'
                },
                KEY_MEDIA_TYPE: KEY_MEDIA_TYPE_ANIME,
                KEY_MEDIA_ID: 12,
            }
        ],
        parse_name_media,
        parse_url_media,
        (
            f'[Koishi]({URL_BASE_ANIME}{12})'
        )
    )
    yield (
        [
            {
                KEY_MEDIA_NAME: {
                    KEY_MEDIA_NAME_ROMAJI: 'Satori'
                },
            }, {
                KEY_MEDIA_NAME: {
                    KEY_MEDIA_NAME_ROMAJI: 'Koishi'
                },
                KEY_MEDIA_TYPE: KEY_MEDIA_TYPE_ANIME,
                KEY_MEDIA_ID: 12,
            }
        ],
        parse_name_media,
        parse_url_media,
        (
            f'Satori\n'
            f'[Koishi]({URL_BASE_ANIME}{12})'
        )
    )
    yield (
        [
            {
                KEY_MEDIA_NAME: {
                    KEY_MEDIA_NAME_ROMAJI: 'Koishi'
                },
                KEY_MEDIA_ID: 12,
            }
        ],
        parse_name_media,
        parse_url_anime,
        (
            f'[Koishi]({URL_BASE_ANIME}{12})'
        )
    )
    yield (
        [
            {
                KEY_MEDIA_NAME: {
                    KEY_MEDIA_NAME_ROMAJI: 'Koishi'
                },
                KEY_MEDIA_ID: 12,
            }
        ],
        parse_name_media,
        parse_url_manga,
        (
            f'[Koishi]({URL_BASE_MANGA}{12})'
        )
    )
    yield (
        [
            {
                KEY_CHARACTER_NAME: {
                    KEY_CHARACTER_NAME_FIRST: 'Koishi'
                },
                KEY_CHARACTER_ID: 12,
            }
        ],
        parse_name_character,
        parse_url_character,
        (
            f'[Koishi]({URL_BASE_CHARACTER}{12})'
        )
    )


@vampytest._(vampytest.call_from(_iter_options__parse_listing_base()).returning_last())
def test__parse_listing_base(character_data, name_parser, url_parser):
    """
    Tests whether ``parse_listing_base`` works as intended.
    
    Parameters
    ----------
    character_data : `dict<str, object>`
        Character data to pass to the function.
    name_parser : `FunctionType`
        Name parser to use.
    url_parser : `FunctionType`
        Url parser to use.
    
    Returns
    -------
    listing : `None`, `str`
        The parsed description.
    """
    return parse_listing_base(character_data, name_parser, url_parser)


def _iter_options__parse_listing_anime():
    yield (
        None,
        None,
    )
    yield (
        [],
        None,
    )
    yield (
        [
            {
                KEY_MEDIA_NAME: {
                    KEY_MEDIA_NAME_ROMAJI: 'Koishi'
                },
                KEY_MEDIA_ID: 12,
            }
        ],
        (
            f'[Koishi]({URL_BASE_ANIME}{12})'
        )
    )
    yield (
        [
            {
                KEY_MEDIA_NAME: {
                    KEY_MEDIA_NAME_ROMAJI: 'Satori'
                },
            }, {
                KEY_MEDIA_NAME: {
                    KEY_MEDIA_NAME_ROMAJI: 'Koishi'
                },
                KEY_MEDIA_ID: 12,
            }
        ],
        (
            f'Satori\n'
            f'[Koishi]({URL_BASE_ANIME}{12})'
        )
    )


@vampytest._(vampytest.call_from(_iter_options__parse_listing_anime()).returning_last())
def test__parse_listing_anime(character_data):
    """
    Tests whether ``parse_listing_anime`` works as intended.
    
    Parameters
    ----------
    character_data : `dict<str, object>`
        Character data to pass to the function.
    
    Returns
    -------
    listing : `None`, `str`
        The parsed description.
    """
    return parse_listing_anime(character_data)


def _iter_options__parse_listing_manga():
    yield (
        None,
        None,
    )
    yield (
        [],
        None,
    )
    yield (
        [
            {
                KEY_MEDIA_NAME: {
                    KEY_MEDIA_NAME_ROMAJI: 'Koishi'
                },
                KEY_MEDIA_ID: 12,
            }
        ],
        (
            f'[Koishi]({URL_BASE_MANGA}{12})'
        )
    )
    yield (
        [
            {
                KEY_MEDIA_NAME: {
                    KEY_MEDIA_NAME_ROMAJI: 'Satori'
                },
            }, {
                KEY_MEDIA_NAME: {
                    KEY_MEDIA_NAME_ROMAJI: 'Koishi'
                },
                KEY_MEDIA_ID: 12,
            }
        ],
        (
            f'Satori\n'
            f'[Koishi]({URL_BASE_MANGA}{12})'
        )
    )


@vampytest._(vampytest.call_from(_iter_options__parse_listing_manga()).returning_last())
def test__parse_listing_manga(character_data):
    """
    Tests whether ``parse_listing_manga`` works as intended.
    
    Parameters
    ----------
    character_data : `dict<str, object>`
        Character data to pass to the function.
    
    Returns
    -------
    listing : `None`, `str`
        The parsed description.
    """
    return parse_listing_manga(character_data)


def _iter_options__parse_listing_character():
    yield (
        None,
        None,
    )
    yield (
        [],
        None,
    )
    yield (
        [
            {
                KEY_CHARACTER_NAME: {
                    KEY_CHARACTER_NAME_FIRST: 'Koishi'
                },
                KEY_CHARACTER_ID: 12,
            }
        ],
        (
            f'[Koishi]({URL_BASE_CHARACTER}{12})'
        )
    )
    yield (
        [
            {
                KEY_CHARACTER_NAME: {
                    KEY_CHARACTER_NAME_FIRST: 'Satori'
                },
            }, {
                KEY_CHARACTER_NAME: {
                    KEY_CHARACTER_NAME_FIRST: 'Koishi'
                },
                KEY_CHARACTER_ID: 12,
            }
        ],
        (
            f'Satori\n'
            f'[Koishi]({URL_BASE_CHARACTER}{12})'
        )
    )


@vampytest._(vampytest.call_from(_iter_options__parse_listing_character()).returning_last())
def test__parse_listing_character(character_data):
    """
    Tests whether ``parse_listing_character`` works as intended.
    
    Parameters
    ----------
    character_data : `dict<str, object>`
        Character data to pass to the function.
    
    Returns
    -------
    listing : `None`, `str`
        The parsed description.
    """
    return parse_listing_character(character_data)
