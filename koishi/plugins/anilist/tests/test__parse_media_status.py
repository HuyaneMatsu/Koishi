import vampytest

from ..parsers_media import MEDIA_STATUS_DEFAULT, parse_media_status
from ..keys import KEY_MEDIA_STATUS


def _iter_options():
    yield {}, MEDIA_STATUS_DEFAULT
    yield {KEY_MEDIA_STATUS: None}, MEDIA_STATUS_DEFAULT
    yield {KEY_MEDIA_STATUS: 'FINISHED'}, 'finished'
    yield {KEY_MEDIA_STATUS: 'DANCING_CAT'}, 'dancing cat'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_media_status(input_data):
    """
    Tests whether ``parse_media_status`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Input data to parse status from.
    
    Returns
    -------
    media_status : `str`
    """
    return parse_media_status(input_data)
