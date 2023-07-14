import vampytest

from ..constants import URL_BASE_CHARACTER
from ..keys import KEY_CHARACTER_ID
from ..parsers_url import parse_url_character


def _iter_options():
    yield {}, None
    yield {KEY_CHARACTER_ID: None}, None
    yield {KEY_CHARACTER_ID: 12}, f'{URL_BASE_CHARACTER}{12}'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_url_character(input_data):
    """
    Tests whether ``parse_url_character`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Input data to parse url from.
    
    Returns
    -------
    character_url : `str`
    """
    return parse_url_character(input_data)
