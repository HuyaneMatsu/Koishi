import vampytest

from ..parsers_media import MEDIA_FORMAT_DEFAULT, parse_media_format
from ..keys import KEY_MEDIA_FORMAT


def _iter_options():
    yield {}, MEDIA_FORMAT_DEFAULT
    yield {KEY_MEDIA_FORMAT: None}, MEDIA_FORMAT_DEFAULT
    yield {KEY_MEDIA_FORMAT: 'TV'}, 'tv'
    yield {KEY_MEDIA_FORMAT: 'DANCING_CAT'}, 'dancing cat'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_media_format(input_data):
    """
    Tests whether ``parse_media_format`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Input data to parse format from.
    
    Returns
    -------
    media_format : `str`
    """
    return parse_media_format(input_data)
