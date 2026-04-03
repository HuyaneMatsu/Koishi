import vampytest
from hata import Embed

from ..constants import URL_BASE_ANIME, URL_BASE_CHARACTER
from ..embed_building_character import TEXT_RELATED_MEDIAS_TOP_N, build_embed_character
from ..keys import (
    KEY_CHARACTER, KEY_CHARACTER_DESCRIPTION, KEY_CHARACTER_ID, KEY_CHARACTER_IMAGE, KEY_CHARACTER_IMAGE_LARGE,
    KEY_CHARACTER_MEDIA_CONNECTIONS, KEY_CHARACTER_MEDIA_CONNECTIONS_MEDIA_ARRAY, KEY_CHARACTER_NAME,
    KEY_CHARACTER_NAME_FIRST, KEY_MEDIA_ID, KEY_MEDIA_NAME, KEY_MEDIA_NAME_ROMAJI, KEY_MEDIA_TYPE, KEY_MEDIA_TYPE_ANIME
)
from ..parsers_name import NAME_DEFAULT


def _iter_options():
    yield (
        None,
        Embed(description = 'No result.'),
    )
    yield (
        {
            'data': {
                KEY_CHARACTER: {}
            }
        },
        Embed(
            NAME_DEFAULT,
        )
    )
    
    yield (
        {
            'data': {
                KEY_CHARACTER: {
                    KEY_CHARACTER_NAME: {
                        KEY_CHARACTER_NAME_FIRST: 'satori',
                    },
                    KEY_CHARACTER_DESCRIPTION: 'love koishi',
                    KEY_CHARACTER_ID: 12,
                    KEY_CHARACTER_IMAGE: {
                        KEY_CHARACTER_IMAGE_LARGE: 'https://orindance.party/'
                    },
                    KEY_CHARACTER_MEDIA_CONNECTIONS: {
                        KEY_CHARACTER_MEDIA_CONNECTIONS_MEDIA_ARRAY: [
                            {
                                KEY_MEDIA_NAME: {
                                    KEY_MEDIA_NAME_ROMAJI: 'Orin'
                                },
                                KEY_MEDIA_TYPE: KEY_MEDIA_TYPE_ANIME,
                                KEY_MEDIA_ID: 13
                            }
                        ],
                    },
                },
            }
        },
        Embed(
            'satori',
            'love koishi',
            url = f'{URL_BASE_CHARACTER}{12}',
        ).add_thumbnail(
            'https://orindance.party/'
        ).add_field(
            TEXT_RELATED_MEDIAS_TOP_N,
            f'[Orin]({URL_BASE_ANIME}{13})',
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_embed_character(data):
    """
    Tests whether ``build_embed_character`` works as intended.
    
    Parameters
    ----------
    data : `None | dict<str, object>`
        Query response data.
    
    Returns
    -------
    embed : ``Embed``
    """
    return build_embed_character(data)
