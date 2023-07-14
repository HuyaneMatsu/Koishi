import vampytest
from hata import Embed

from ..constants import URL_BASE_ANIME, URL_BASE_MANGA
from ..embed_building_media import build_embed_media_based
from ..keys import (
    KEY_MEDIA_DESCRIPTION, KEY_MEDIA_ID, KEY_MEDIA_IMAGE, KEY_MEDIA_IMAGE_LARGE, KEY_MEDIA_NAME, KEY_MEDIA_NAME_ROMAJI
)
from ..parsers_name import NAME_DEFAULT
from ..parsers_url import parse_url_anime, parse_url_manga


def _iter_options():
    yield (
        {},
        parse_url_anime,
        Embed(
            NAME_DEFAULT,
        )
    )
    
    yield (
        {
            KEY_MEDIA_NAME: {
                KEY_MEDIA_NAME_ROMAJI: 'satori',
            },
            KEY_MEDIA_DESCRIPTION: 'love koishi',
            KEY_MEDIA_ID: 12,
            KEY_MEDIA_IMAGE: {
                KEY_MEDIA_IMAGE_LARGE: 'https://orindance.party/'
            },
        },
        parse_url_anime,
        Embed(
            'satori',
            'love koishi',
            url = f'{URL_BASE_ANIME}{12}',
        ).add_thumbnail(
            'https://orindance.party/'
        )
    )
    
    yield (
        {
            KEY_MEDIA_ID: 12,
        },
        parse_url_manga,
        Embed(
            NAME_DEFAULT,
            url = f'{URL_BASE_MANGA}{12}',
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_embed_media_based(data, url_parser):
    """
    Tests whether ``build_embed_media_based`` works as intended.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Query data.
    url_parser : `FunctionType`
        parser to parse url with.
    
    Returns
    -------
    embed : ``Embed``
    """
    return build_embed_media_based(data, url_parser)
