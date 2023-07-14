import vampytest

from ..constants import URL_BASE_ANIME
from ..keys import (
    KEY_CHARACTER_MEDIA_CONNECTIONS, KEY_CHARACTER_MEDIA_CONNECTIONS_MEDIA_ARRAY, KEY_MEDIA_ID, KEY_MEDIA_NAME,
    KEY_MEDIA_NAME_ROMAJI, KEY_MEDIA_TYPE, KEY_MEDIA_TYPE_ANIME
)
from ..parsers_description import parse_character_media_connections_description


def _iter_options():
    yield (
        {},
        None,
    )
    yield (
        {
            KEY_CHARACTER_MEDIA_CONNECTIONS: None,
        },
        None,
    )
    yield (
        {
            KEY_CHARACTER_MEDIA_CONNECTIONS: {},
        },
        None,
    )
    yield (
        {
            KEY_CHARACTER_MEDIA_CONNECTIONS: {
                KEY_CHARACTER_MEDIA_CONNECTIONS_MEDIA_ARRAY: None,
            },
        },
        None,
    )
    yield (
        {
            KEY_CHARACTER_MEDIA_CONNECTIONS: {
                KEY_CHARACTER_MEDIA_CONNECTIONS_MEDIA_ARRAY: [],
            },
        },
        None,
    )
    yield (
        {
            KEY_CHARACTER_MEDIA_CONNECTIONS: {
                KEY_CHARACTER_MEDIA_CONNECTIONS_MEDIA_ARRAY: [
                    {
                        KEY_MEDIA_NAME: {
                            KEY_MEDIA_NAME_ROMAJI: 'Koishi'
                        },
                        KEY_MEDIA_TYPE: KEY_MEDIA_TYPE_ANIME,
                        KEY_MEDIA_ID: 12,
                    }
                ],
            },
        },
        (
            f'[Koishi]({URL_BASE_ANIME}{12})'
        )
    )
    yield (
        {
            KEY_CHARACTER_MEDIA_CONNECTIONS: {
                KEY_CHARACTER_MEDIA_CONNECTIONS_MEDIA_ARRAY: [
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
            },
        },
        (
            f'Satori\n'
            f'[Koishi]({URL_BASE_ANIME}{12})'
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_character_media_connections_description(character_data):
    """
    Tests whether ``parse_character_media_connections_description`` works as intended.
    
    Parameters
    ----------
    character_data : `dict<str, object>`
        Character data to pass to the function.
    
    Returns
    -------
    description : `str`
        The parsed description.
    """
    return parse_character_media_connections_description(character_data)
