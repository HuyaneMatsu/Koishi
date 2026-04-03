import vampytest

from hata.discord.embed.embed.constants import TITLE_LENGTH_MAX

from ..parsers_name import NAME_DEFAULT, parse_media_name
from ..keys import KEY_MEDIA_NAME, KEY_MEDIA_NAME_NATIVE, KEY_MEDIA_NAME_ROMAJI


def _iter_options():
    yield (
        {},
        NAME_DEFAULT,
    )
    
    yield (
        {
            KEY_MEDIA_NAME: None,
        },
        NAME_DEFAULT,
    )
    
    yield (
        {
            KEY_MEDIA_NAME: {},
        },
        NAME_DEFAULT,
    )
    
    yield (
        {
            KEY_MEDIA_NAME: {
                KEY_MEDIA_NAME_ROMAJI: None,
            },
        },
        NAME_DEFAULT,
    )
    
    yield (
        {
            KEY_MEDIA_NAME: {
                KEY_MEDIA_NAME_ROMAJI: 'koishi',
            },
        },
        'koishi',
    )
    
    yield (
        {
            KEY_MEDIA_NAME: {
                KEY_MEDIA_NAME_NATIVE: None,
            }
        },
        NAME_DEFAULT,
    )
    
    yield (
        {
            KEY_MEDIA_NAME: {
                KEY_MEDIA_NAME_NATIVE: 'koishi',
            }
        },
        'koishi',
    )
    
    yield (
        {
            KEY_MEDIA_NAME: {
                KEY_MEDIA_NAME_ROMAJI: 'koishi',
                KEY_MEDIA_NAME_NATIVE: 'koishi',
            }
        },
        'koishi'
    )
    
    yield (
        {
            KEY_MEDIA_NAME: {
                KEY_MEDIA_NAME_ROMAJI: 'koishi',
                KEY_MEDIA_NAME_NATIVE: 'okuu',
            }
        },
        'koishi (okuu)'
    )
    
    yield (
        {
            KEY_MEDIA_NAME: {
                KEY_MEDIA_NAME_ROMAJI: 'k' * TITLE_LENGTH_MAX,
            }
        },
        'k' * TITLE_LENGTH_MAX
    )
    
    yield (
        {
            KEY_MEDIA_NAME: {
                KEY_MEDIA_NAME_ROMAJI: 'k' * (TITLE_LENGTH_MAX + 1),
            }
        },
        'k' * (TITLE_LENGTH_MAX - 4) + ' ...'
    )
    
    yield (
        {
            KEY_MEDIA_NAME: {
                KEY_MEDIA_NAME_NATIVE: 'k' * TITLE_LENGTH_MAX,
            }
        },
        'k' * TITLE_LENGTH_MAX
    )
    
    yield (
        {
            KEY_MEDIA_NAME: {
                KEY_MEDIA_NAME_NATIVE: 'k' * (TITLE_LENGTH_MAX + 1),
            }
        },
        'k' * (TITLE_LENGTH_MAX - 4) + ' ...'
    )
    
    yield (
        {
            KEY_MEDIA_NAME: {
                KEY_MEDIA_NAME_ROMAJI: 'k' * TITLE_LENGTH_MAX,
                KEY_MEDIA_NAME_NATIVE: 'o' * TITLE_LENGTH_MAX,
            }
        },
        'k' * (TITLE_LENGTH_MAX - 10) + ' ... (...)'
    )
    
    yield (
        {
            KEY_MEDIA_NAME: {
                KEY_MEDIA_NAME_ROMAJI: 'k' * (TITLE_LENGTH_MAX - 6),
                KEY_MEDIA_NAME_NATIVE: 'o' * TITLE_LENGTH_MAX,
            }
        },
        'k' * (TITLE_LENGTH_MAX - 6) + ' (...)'
    )
    
    # We need at least 2 extra spaces to insert a character due to leaving 1 space after the character
    yield (
        {
            KEY_MEDIA_NAME: {
                KEY_MEDIA_NAME_ROMAJI: 'k' * (TITLE_LENGTH_MAX - 7),
                KEY_MEDIA_NAME_NATIVE: 'o' * TITLE_LENGTH_MAX,
            }
        },
        'k' * (TITLE_LENGTH_MAX - 7) + ' (...)'
    )
    
    yield (
        {
            KEY_MEDIA_NAME: {
                KEY_MEDIA_NAME_ROMAJI: 'k' * (TITLE_LENGTH_MAX - 8),
                KEY_MEDIA_NAME_NATIVE: 'o' * TITLE_LENGTH_MAX,
            }
        },
        'k' * (TITLE_LENGTH_MAX - 8) + ' (' + ('o' * 1) + ' ...)'
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_media_name(input_data):
    """
    Tests whether ``parse_media_name`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Media data to parse name from.
    
    Returns
    -------
    name_value : `str`
    """
    output = parse_media_name(input_data)
    vampytest.assert_instance(output, str)
    vampytest.assert_true(len(output) <= TITLE_LENGTH_MAX)
    return output
