__all__ = ()

from .keys import (
    KEY_FUZZY_DATE_DAY, KEY_FUZZY_DATE_MONTH, KEY_FUZZY_DATE_YEAR, KEY_MEDIA_END_DATE, KEY_MEDIA_START_DATE
)


MONTH_NAMES_SHORT = {
    1: 'Jan',
    2: 'Feb',
    3: 'Mar',
    4: 'Apr',
    5: 'May',
    6: 'Jun',
    7: 'Jul',
    8: 'Aug',
    9: 'Sep',
    10: 'Oct',
    11: 'Nov',
    12: 'Dec',
}

MONTH_NAMES_FULL = {
    1: 'January',
    2: 'February',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'August',
    9: 'September',
    10: 'October',
    11: 'November',
    12: 'December',
}


def parse_fuzzy_date(fuzzy_date_data):
    """
    Parses the given fuzzy date data and returns the built value.
    
    Parameters
    ----------
    fuzzy_date_data : `null | dict<str, object>`
        Fuzzy date data.
    
    Returns
    -------
    date_value : `None`, `str`
    """
    if fuzzy_date_data is None:
        return None
    
    fuzzy_date_year = fuzzy_date_data.get(KEY_FUZZY_DATE_YEAR, None)
    fuzzy_date_month = fuzzy_date_data.get(KEY_FUZZY_DATE_MONTH, None)
    fuzzy_date_day = fuzzy_date_data.get(KEY_FUZZY_DATE_DAY, None)

    if (fuzzy_date_year is not None) or (fuzzy_date_month is not None) or (fuzzy_date_day is not None):
        date_value_parts = []
        if fuzzy_date_year is None:
            if (fuzzy_date_month is None):
                fuzzy_date_day_value = str(fuzzy_date_day)
                date_value_parts.append(fuzzy_date_day_value)
                date_value_parts.append(' (day of month)')
            else:
                if (fuzzy_date_day is None):
                    fuzzy_date_month_value = MONTH_NAMES_FULL.get(fuzzy_date_month, '???')
                    date_value_parts.append(fuzzy_date_month_value)
                else:
                    fuzzy_date_month_value = MONTH_NAMES_SHORT.get(fuzzy_date_month, '???')
                    fuzzy_date_day_value = str(fuzzy_date_day)
                    date_value_parts.append(fuzzy_date_month_value)
                    date_value_parts.append(' ')
                    date_value_parts.append(fuzzy_date_day_value)
        else:
            fuzzy_date_year_value = str(fuzzy_date_year)
            date_value_parts.append(fuzzy_date_year_value)
            if (fuzzy_date_month is None):
                if (fuzzy_date_day is None):
                    date_value_parts.append(' (year)')
                else:
                    fuzzy_date_day_value = str(fuzzy_date_day)
                    date_value_parts.append('-??-')
                    date_value_parts.append(fuzzy_date_day_value)
            else:
                fuzzy_date_month_value = str(fuzzy_date_month)
                date_value_parts.append('-')
                date_value_parts.append(fuzzy_date_month_value)
                date_value_parts.append('-')
                
                if (fuzzy_date_day is None):
                    fuzzy_date_day_value = '??'
                else:
                    fuzzy_date_day_value = str(fuzzy_date_day)
                
                date_value_parts.append(fuzzy_date_day_value)
        
        date_value = ''.join(date_value_parts)
    else:
        date_value = None
    
    return date_value


def parse_media_date_range(media_data):
    """
    Parses media date range.
    
    Parameters
    ----------
    media_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    date_range : `None | (str, str)`
        Returns a `None` on failure.
        
        First element is the state and the second is the value.
    """
    start_date = parse_fuzzy_date(media_data.get(KEY_MEDIA_START_DATE, None))
    end_date = parse_fuzzy_date(media_data.get(KEY_MEDIA_END_DATE, None))
    
    
    if (start_date is None):
        if (end_date is None):
            date_range = None
        else:
            date_range = 'Ended', end_date
    else:
        if (end_date is None):
            date_range = 'Started', start_date
        else:
            if (start_date == end_date):
                date_range = 'Aired', start_date
            else:
                date_range = 'Released', f'Between {start_date} and {end_date}'
    
    return date_range
