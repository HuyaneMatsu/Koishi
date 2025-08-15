__all__ = (
    'build_duration_suggestion', 'parse_duration_suggestion', 'parse_duration_hexadecimal',
    'produce_duration_suggestion'
)

from re import I as re_ignore_case, compile as re_compile


DURATION_VALUE_AND_UNIT_PAIR_RP = re_compile(' *(\\d+) *([dhms]) *', re_ignore_case)


def produce_duration_suggestion(duration):
    """
    Produces a duration suggestion.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    duration : `int`
        Duration to build produce for.
    
    Yields
    ------
    part : `str`
    """
    minutes, seconds = divmod(duration, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    
    element_added = False
    
    if days:
        yield str(days)
        yield 'd'
        element_added = True
    
    if hours:
        if element_added:
            yield ' '
        else:
            element_added = True
        
        yield str(hours)
        yield 'h'
    
    if minutes:
        if element_added:
            yield ' '
        else:
            element_added = True
        
        yield str(minutes)
        yield 'm'
    
    if seconds or (not element_added):
        if element_added:
            yield ' '
        
        yield str(seconds)
        yield 's'


def build_duration_suggestion(duration):
    """
    Builds duration suggestion.
    
    Parameters
    ----------
    duration : `int`
        Duration to build suggestion for.
    
    Returns
    -------
    suggestion : `str`
    """
    return ''.join([*produce_duration_suggestion(duration)])


def parse_duration_hexadecimal(string):
    """
    Parses duration hexadecimal value.
    
    Parameters
    ----------
    string : `str`
        String to parse.
    
    Returns
    -------
    duration : `int`
    """
    if len(string) < 4:
        duration = 0
    
    else:
        try:
            duration = int(string, 16)
        except ValueError:
            duration = 0
    
    return duration


def parse_duration_suggestion(string):
    """
    Parses a duration suggestion.
    
    Parameters
    ----------
    string : `str`
        String to parse.
    
    Returns
    -------
    duration : `int`
    """
    duration = 0
    start = 0
    end = len(string)
    
    while start < end:
        match = DURATION_VALUE_AND_UNIT_PAIR_RP.match(string, start)
        if match is None:
            return 0
        
        value, unit = match.groups()
        start = match.end()
        value = int(value)
        unit = unit.casefold()
        
        if unit == 'd':
            value *= 86400
        
        elif unit == 'h':
            value *= 3600
        
        elif unit == 'm':
            value *= 60
        
        duration += value
    
    return duration
