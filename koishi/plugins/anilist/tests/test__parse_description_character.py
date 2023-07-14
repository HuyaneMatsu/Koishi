import vampytest

from ..constants import DESCRIPTION_LENGTH_MAX
from ..parsers_description import parse_description_character
from ..keys import (
    KEY_CHARACTER_AGE, KEY_CHARACTER_BIRTH_DATE, KEY_CHARACTER_BLOOD_TYPE, KEY_CHARACTER_DESCRIPTION,
    KEY_CHARACTER_GENDER, KEY_FUZZY_DATE_DAY, KEY_FUZZY_DATE_MONTH, KEY_FUZZY_DATE_YEAR
)


def _iter_options():
    yield (
        {},
        None,
    )
    yield (
        {
            KEY_CHARACTER_AGE: '17', # Age is string
            KEY_CHARACTER_BIRTH_DATE: {
                KEY_FUZZY_DATE_YEAR: 8,
                KEY_FUZZY_DATE_MONTH: 6,
                KEY_FUZZY_DATE_DAY: 7,
            },
            KEY_CHARACTER_BLOOD_TYPE: 'A+',
            KEY_CHARACTER_DESCRIPTION: 'She likes Koishi',
            KEY_CHARACTER_GENDER: 'youkai',
        },
        (
            '**Birthday:** 8-6-7\n'
            '**Age:** 17\n'
            '**Gender:** youkai\n'
            '**Blood type:** A+\n'
            '\n'
            'She likes Koishi'
        ),
    )
    yield (
        {
            KEY_CHARACTER_DESCRIPTION: 'a' * (DESCRIPTION_LENGTH_MAX + 1),
        },
        'a' * (DESCRIPTION_LENGTH_MAX - 4) + ' ...',
    )

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_description_character(character_data):
    """
    Tests whether ``parse_description_character`` works as intended.
    
    Parameters
    ----------
    character_data : `dict<str, object>`
        Character data to pass to the function.
    
    Returns
    -------
    description : `str`
        The parsed description.
    """
    return parse_description_character(character_data)
