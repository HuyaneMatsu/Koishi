import vampytest

from ..keys import KEY_MEDIA_IMAGE, KEY_MEDIA_IMAGE_LARGE
from ..parsers_url import parse_image_url_media


def _iter_options():
    yield {}, None
    yield {KEY_MEDIA_IMAGE: None}, None
    yield {KEY_MEDIA_IMAGE: {}}, None
    yield {KEY_MEDIA_IMAGE: {KEY_MEDIA_IMAGE_LARGE: None}}, None
    yield (
        {KEY_MEDIA_IMAGE: {KEY_MEDIA_IMAGE_LARGE: 'https://www.orindance.party/'}},
        'https://www.orindance.party/',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_image_url_media(input_data):
    """
    Tests whether ``parse_image_url_media`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Input data to parse url from.
    
    Returns
    -------
    media_image_url : `str`
    """
    return parse_image_url_media(input_data)
