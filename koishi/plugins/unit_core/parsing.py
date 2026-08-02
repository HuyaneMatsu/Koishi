__all__ = ('parse_duration',)

from re import compile as re_compile

DURATION_UNIT_PATTERN = re_compile('(\\d+)\\s*([wWdDhHmMsS])?')


def parse_duration(value):
    """
    Converts a duration value into duration in seconds.
    
    Parameters
    ----------
    value : `None | str`
        Duration value.
    
    Returns
    -------
    duration : `int`
    """
    if value is None:
        return 0
    
    duration = 0
    
    for match in DURATION_UNIT_PATTERN.finditer(value):
        amount, unit = match.groups()
        
        if unit in ('w', 'W'):
            multiplier = 604800
        
        elif unit in ('d', 'D'):
            multiplier = 86400
        
        elif unit in ('h', 'H'):
            multiplier = 3600
        
        elif unit in ('m', 'M'):
            multiplier = 60
        
        else:
            multiplier = 1
        
        duration += int(amount) * multiplier
    
    return duration
