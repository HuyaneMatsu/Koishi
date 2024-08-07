__all__ = ()

from datetime import date as Date, datetime as DateTime, time as Time, timezone as TimeZone
from time import mktime as make_time, struct_time as TimeStruct

from werkzeug.http import http_date


def iso_date(timestamp = None):
    """
    Returns iso timestamp.
    
    Parameters
    ----------
    timestamp : `DateTime | Date | int | float | TimeStruct | None` = `None`, Optional
    
    Returns
    -------
    output : `str`
    """
    if timestamp is None:
        timestamp = DateTime.now(TimeZone.utc)
    
    elif isinstance(timestamp, DateTime):
        if timestamp.tzinfo is None:
            timestamp = timestamp.replace(tzinfo = TimeZone.utc)
    
    elif isinstance(timestamp, Date):
        timestamp = DateTime.combine(timestamp, Time(), TimeZone.utc)
    
    else:
        if isinstance(timestamp, TimeStruct):
            timestamp = make_time(timestamp)
        
        timestamp = DateTime.fromtimestamp(timestamp, tz = TimeZone.utc)
    
    return timestamp.isoformat()


http_date.__code__ = iso_date.__code__
http_date.__globals__.update({
    'Date': Date,
    'DateTime': DateTime,
    'Time': Time,
    'TimeStruct': TimeStruct,
    'TimeZone': TimeZone,
    'make_time': make_time,
})
