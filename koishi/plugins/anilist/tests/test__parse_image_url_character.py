import vampytest

from ..keys import KEY_CHARACTER_IMAGE, KEY_CHARACTER_IMAGE_LARGE
from ..parsers_url import parse_image_url_character


def _iter_options():
    yield {}, None
    yield {KEY_CHARACTER_IMAGE: None}, None
    yield {KEY_CHARACTER_IMAGE: {}}, None
    yield {KEY_CHARACTER_IMAGE: {KEY_CHARACTER_IMAGE_LARGE: None}}, None
    yield (
        {KEY_CHARACTER_IMAGE: {KEY_CHARACTER_IMAGE_LARGE: 'https://www.orindance.party/'}},
        'https://www.orindance.party/',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_image_url_character(input_data):
    """
    Tests whether ``parse_image_url_character`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Input data to parse url from.
    
    Returns
    -------
    character_image_url : `str`
    """
    return parse_image_url_character(input_data)
