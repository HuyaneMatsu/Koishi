__all__ = ()

from math import floor


def produce_time_delta(time_delta):
    """
    Produces a time delta.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    time_delta : ``TimeDelta``
        The time delta to convert.
    
    Yields
    ------
    part : `str`
    """
    field_added = False
    
    seconds = floor(time_delta.total_seconds())
    
    days, seconds = divmod(seconds, 86400)
    if days:
        yield str(days)
        yield ' days'
        field_added = True
    
    hours, seconds = divmod(seconds, 3600)
    if hours:
        if field_added:
            yield ', '
        else:
            field_added = True
        
        yield str(hours)
        yield ' hours'
    
    minutes, seconds = divmod(seconds, 60)
    if minutes:
        if field_added:
            yield ', '
        else:
            field_added = True
        
        yield str(minutes)
        yield ' minutes'
    
    if seconds or (not field_added):
        if field_added:
            yield ', '
        yield str(seconds)
        yield ' seconds'


def convert_time_delta(time_delta):
    """
    Converts the time delta to a string and returns it.
    
    Parameters
    ----------
    time_delta : ``TimeDelta``
        The time delta to convert.
    
    Returns
    -------
    output : `str`
    """
    return ''.join([*produce_time_delta(time_delta)])
