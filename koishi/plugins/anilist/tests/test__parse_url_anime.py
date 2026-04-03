import vampytest

from ..constants import URL_BASE_ANIME
from ..keys import KEY_MEDIA_ID
from ..parsers_url import parse_url_anime


def _iter_options():
    yield {}, None
    yield {KEY_MEDIA_ID: None}, None
    yield {KEY_MEDIA_ID: 12}, f'{URL_BASE_ANIME}{12}'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_url_anime(input_data):
    """
    Tests whether ``parse_url_anime`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Input data to parse url from.
    
    Returns
    -------
    anime_url : `str`
    """
    return parse_url_anime(input_data)
