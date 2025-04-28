import vampytest

from ..parsers_name import NAME_DEFAULT, parse_character_name
from ..keys import (
    KEY_CHARACTER_NAME, KEY_CHARACTER_NAME_FIRST, KEY_CHARACTER_NAME_LAST, KEY_CHARACTER_NAME_MIDDLE,
    KEY_CHARACTER_NAME_NATIVE
)


def _iter_options():
    yield {}, NAME_DEFAULT
    yield {KEY_CHARACTER_NAME: None}, NAME_DEFAULT
    yield {KEY_CHARACTER_NAME: {}}, NAME_DEFAULT
    yield {KEY_CHARACTER_NAME: {KEY_CHARACTER_NAME_FIRST: None}}, NAME_DEFAULT
    yield {KEY_CHARACTER_NAME: {KEY_CHARACTER_NAME_FIRST: 'koishi'}}, 'koishi'
    yield {KEY_CHARACTER_NAME: {KEY_CHARACTER_NAME_MIDDLE: None}}, NAME_DEFAULT
    yield {KEY_CHARACTER_NAME: {KEY_CHARACTER_NAME_MIDDLE: 'koishi'}}, 'koishi'
    yield {KEY_CHARACTER_NAME: {KEY_CHARACTER_NAME_LAST: None}}, NAME_DEFAULT
    yield {KEY_CHARACTER_NAME: {KEY_CHARACTER_NAME_LAST: 'koishi'}}, 'koishi'
    yield {KEY_CHARACTER_NAME: {KEY_CHARACTER_NAME_NATIVE: None}}, NAME_DEFAULT
    yield {KEY_CHARACTER_NAME: {KEY_CHARACTER_NAME_NATIVE: 'koishi'}}, 'koishi'
    
    yield (
        {
            KEY_CHARACTER_NAME: {
                KEY_CHARACTER_NAME_FIRST: 'koishi',
                KEY_CHARACTER_NAME_MIDDLE: 'satori',
                KEY_CHARACTER_NAME_LAST: 'okuu',
                KEY_CHARACTER_NAME_NATIVE: 'orin',
            }
        },
        'koishi satori okuu (orin)'
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_character_name(input_data):
    """
    Tests whether ``parse_character_name`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Input data to parse name from.
    
    Returns
    -------
    name_value : `str`
    """
    output = parse_character_name(input_data)
    vampytest.assert_instance(output, str)
    return output
