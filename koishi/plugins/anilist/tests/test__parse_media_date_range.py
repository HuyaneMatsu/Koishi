import vampytest
from ..keys import (
    KEY_FUZZY_DATE_DAY, KEY_FUZZY_DATE_MONTH, KEY_FUZZY_DATE_YEAR, KEY_MEDIA_END_DATE, KEY_MEDIA_START_DATE
)
from ..parsers_date import parse_media_date_range


def _iter_options():
    yield {}, None
    yield {KEY_MEDIA_START_DATE: None, KEY_MEDIA_END_DATE: None}, None
    yield {KEY_MEDIA_START_DATE: {}, KEY_MEDIA_END_DATE: {}}, None
    yield {KEY_MEDIA_START_DATE: {}, KEY_MEDIA_END_DATE: {}}, None
    yield (
        {
            KEY_MEDIA_START_DATE: {KEY_FUZZY_DATE_YEAR: 4, KEY_FUZZY_DATE_MONTH: 6, KEY_FUZZY_DATE_DAY: 8},
            KEY_MEDIA_END_DATE: None,
        },
        ('Started', '4-6-8'),
    )
    yield (
        {
            KEY_MEDIA_START_DATE: None,
            KEY_MEDIA_END_DATE: {KEY_FUZZY_DATE_YEAR: 5, KEY_FUZZY_DATE_MONTH: 7, KEY_FUZZY_DATE_DAY: 9},
        },
        ('Ended', '5-7-9'),
    )
    yield (
        {
            KEY_MEDIA_START_DATE: {KEY_FUZZY_DATE_YEAR: 4, KEY_FUZZY_DATE_MONTH: 6, KEY_FUZZY_DATE_DAY: 8},
            KEY_MEDIA_END_DATE: {KEY_FUZZY_DATE_YEAR: 5, KEY_FUZZY_DATE_MONTH: 7, KEY_FUZZY_DATE_DAY: 9},
        },
        ('Released', 'Between 4-6-8 and 5-7-9'),
    )
    yield (
        {
            KEY_MEDIA_START_DATE: {KEY_FUZZY_DATE_YEAR: 4, KEY_FUZZY_DATE_MONTH: 6, KEY_FUZZY_DATE_DAY: 8},
            KEY_MEDIA_END_DATE: {KEY_FUZZY_DATE_YEAR: 4, KEY_FUZZY_DATE_MONTH: 6, KEY_FUZZY_DATE_DAY: 8},
        },
        ('Aired', '4-6-8'),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_media_date_range(input_data):
    """
    Tests whether ``parse_media_date_range`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Input data to parse media date range from.
    
    Returns
    -------
    date_range : `None | (str, str)`
    """
    return parse_media_date_range(input_data)
