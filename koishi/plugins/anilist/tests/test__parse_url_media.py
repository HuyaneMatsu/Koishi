import vampytest

from ..constants import URL_BASE_ANIME, URL_BASE_MANGA
from ..keys import KEY_MEDIA_ID, KEY_MEDIA_TYPE, KEY_MEDIA_TYPE_ANIME, KEY_MEDIA_TYPE_MANGA
from ..parsers_url import parse_url_media


def _iter_options():
    yield {}, None
    yield {KEY_MEDIA_TYPE: None, KEY_MEDIA_ID: None}, None
    yield {KEY_MEDIA_TYPE: KEY_MEDIA_TYPE_ANIME}, None
    yield {KEY_MEDIA_ID: 12}, None
    yield {KEY_MEDIA_TYPE: KEY_MEDIA_TYPE_ANIME, KEY_MEDIA_ID: 12}, f'{URL_BASE_ANIME}{12}'
    yield {KEY_MEDIA_TYPE: KEY_MEDIA_TYPE_MANGA, KEY_MEDIA_ID: 12}, f'{URL_BASE_MANGA}{12}'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_url_media(input_data):
    """
    Tests whether ``parse_url_media`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Input data to parse url from.
    
    Returns
    -------
    media_url : `str`
    """
    return parse_url_media(input_data)
