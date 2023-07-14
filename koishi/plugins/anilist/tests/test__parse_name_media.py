import vampytest

from ..parsers_name import NAME_DEFAULT, parse_name_media
from ..keys import KEY_MEDIA_NAME, KEY_MEDIA_NAME_NATIVE, KEY_MEDIA_NAME_ROMAJI


def _iter_options():
    yield {}, NAME_DEFAULT
    yield {KEY_MEDIA_NAME: None}, NAME_DEFAULT
    yield {KEY_MEDIA_NAME: {}}, NAME_DEFAULT
    yield {KEY_MEDIA_NAME: {KEY_MEDIA_NAME_ROMAJI: None}}, NAME_DEFAULT
    yield {KEY_MEDIA_NAME: {KEY_MEDIA_NAME_ROMAJI: 'koishi'}}, 'koishi'
    yield {KEY_MEDIA_NAME: {KEY_MEDIA_NAME_NATIVE: None}}, NAME_DEFAULT
    yield {KEY_MEDIA_NAME: {KEY_MEDIA_NAME_NATIVE: 'koishi'}}, 'koishi'
    
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


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_name_media(input_data):
    """
    Tests whether ``parse_name_media`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Media data to parse name from.
    
    Returns
    -------
    name_value : `None`, `str`
    """
    return parse_name_media(input_data)
