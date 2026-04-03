import vampytest

from ..parsers_date import parse_fuzzy_date
from ..keys import KEY_FUZZY_DATE_DAY, KEY_FUZZY_DATE_MONTH, KEY_FUZZY_DATE_YEAR


def _iter_options():
    # None
    yield None, None
    yield {}, None
    yield {KEY_FUZZY_DATE_YEAR: None, KEY_FUZZY_DATE_MONTH: None, KEY_FUZZY_DATE_DAY: None}, None
    
    # Single
    yield {KEY_FUZZY_DATE_YEAR: 4}, '4 (year)'
    yield {KEY_FUZZY_DATE_MONTH: 6}, 'June'
    yield {KEY_FUZZY_DATE_DAY: 8}, '8 (day of month)'
    
    # Double
    yield {KEY_FUZZY_DATE_YEAR: 4, KEY_FUZZY_DATE_MONTH: 6}, '4-6-??'
    yield {KEY_FUZZY_DATE_YEAR: 4, KEY_FUZZY_DATE_DAY: 8}, '4-??-8'
    yield {KEY_FUZZY_DATE_MONTH: 6, KEY_FUZZY_DATE_DAY: 8}, 'Jun 8'

    # Triple
    yield {KEY_FUZZY_DATE_YEAR: 4, KEY_FUZZY_DATE_MONTH: 6, KEY_FUZZY_DATE_DAY: 8}, '4-6-8'

    # Out of range (month only)
    yield {KEY_FUZZY_DATE_MONTH: 66}, '???'
    yield {KEY_FUZZY_DATE_MONTH: 66, KEY_FUZZY_DATE_DAY: 8}, '??? 8'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_fuzzy_date(input_data):
    """
    Tests whether ``parse_fuzzy_date`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Input data to parse date from.
    
    Returns
    -------
    date_value : `None`, `str`
    """
    return parse_fuzzy_date(input_data)
