__all__ = ()

from datetime import timedelta as TimeDelta

from hata.ext.slash import P


PARAMETER_DAYS = P('int', 'days', min_value = 0, max_value = 28)
PARAMETER_HOURS = P('int', 'hours', min_value = 0, max_value = 24)
PARAMETER_MINUTES = P('int', 'minutes', min_value = 0, max_value = 60)
PARAMETER_SECONDS = P('int', 'seconds', min_value = 0, max_value = 60)

DURATION_MAX = TimeDelta(days = 28)
DURATION_UNITS = ('days', 'hours', 'minutes', 'seconds')


def get_duration(days, hours, minutes, seconds):
    """
    Gets mute duration in time delta.
    
    Parameters
    ----------
    days : `int`
        the amount of days to mute the user for.
    hours : `int`
        The amount of hours to mute the user for.
    minutes : `int`
        the amount of minutes to mute the user for.
    seconds : `int`
        The amount of seconds to mute the users for.
    
    Returns
    -------
    duration : `TimeDelta`
        Mute duration if any.
    """
    if not (days or hours or minutes or seconds):
        return DURATION_MAX
    
    duration = TimeDelta(days = days, hours = hours, minutes = minutes, seconds = seconds)
    if duration > DURATION_MAX:
        duration = DURATION_MAX
    
    return duration


def iter_deconstruct_duration(duration):
    """
    Deconstructs the duration into days, hours, minutes, seconds.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    duration : `TimeDelta`
        The duration to deconstruct.
    
    Yields
    ------
    unit : `int`
    """
    yield duration.days
    hours, seconds = divmod(duration.seconds, 60 * 60)
    yield hours
    yield from divmod(seconds, 60)


def build_duration_string(duration):
    """
    Converts the mute duration to string.
    
    Parameters
    ----------
    duration : `TimeDelta`
        Mute duration.
    
    Returns
    -------
    duration_string : `str`
    """
    string_parts = []
    
    field_added = False
    
    for unit_value, unit_name in zip(iter_deconstruct_duration(duration), DURATION_UNITS):
        if unit_value:
            if field_added:
                string_parts.append(', ')
            else:
                field_added = True
            
            string_parts.append(str(unit_value))
            string_parts.append(' ')
            string_parts.append(unit_name)
    
    return ''.join(string_parts)
