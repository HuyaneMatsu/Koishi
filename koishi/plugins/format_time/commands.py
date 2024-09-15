__all__ = ()

from datetime import datetime as DateTime, timezone as TimeZone

from dateutil.relativedelta import relativedelta as RelativeDelta
from hata import Embed, id_to_datetime, unix_time_to_datetime
from hata.discord.utils import DATETIME_MAX, DATETIME_MIN, UNIX_TIME_MAX, UNIX_TIME_MIN
from hata.ext.slash import P, abort

from ...bots import FEATURE_CLIENTS

from .helpers import (
    bound_limit_snowflake, build_format_time_embed, check_relative_ranges, get_time_zone_offset,
    get_time_zone_suggestions, maybe_add_time_zone_offset
)


FORMAT_TIME_COMMANDS = FEATURE_CLIENTS.interactions(
    None,
    integration_types = ['guild_install', 'user_install'],
    is_global = True,
    name = 'format-time',
    description = 'Formats the given time.',
)



@FORMAT_TIME_COMMANDS.interactions(name = 'absolute')
async def format_absolute(
    year : P('number', 'year', min_value = DATETIME_MIN.year, max_value = DATETIME_MAX.year) = 0,
    month: P('number', 'days', min_value = 1, max_value = 12) = 1,
    day: P('number', 'days', min_value = 1, max_value = 31) = 1,
    hour: P('number', 'hours', min_value = 0, max_value = 23) = 0,
    minute: P('number', 'minutes', min_value = 0, max_value = 59) = 0,
    second: P('number', 'seconds', min_value = 0, max_value = 59) = 0,
    time_zone: P('str', 'Time zone or UTC if omitted.') = None,
    daylight_saving_time : P('bool', 'Whether should apply date time saving shift to time zone offset.') = False,
):
    """
    Formats the given time.
    
    This function is a coroutine.
    
    Parameters
    ----------
    year : `int` = `1`, Optional
        Absolute years.
    
    month : `int` = `1`, Optional
        Absolute months.
    
    day : `int` = `1`, Optional
        Absolute days.
    
    hour : `int` = `0`, Optional
        Absolute hours.
    
    minutes : `int` = `0`, Optional
        Absolute minutes.
    
    second : `int` = `0`, Optional
        Absolute hours.
    
    time_zone : `None | str` = None, Optional
        Timezone offset in hours.
    
    Returns
    -------
    response : ``Embed``
    """
    try:
        date_time = DateTime(year, month, day, hour, minute, second, tzinfo = TimeZone.utc)
    except (ValueError, OverflowError) as err:
        error_parameters = err.args
        if error_parameters:
            error_message = error_parameters[0]
        else:
            error_message = 'Undefined value error occurred.'
        
        return abort(error_message)
    
    if time_zone is None:
        time_zone_offset = 0.0
    else:
        time_zone_offset = get_time_zone_offset(time_zone)
    
    if daylight_saving_time:
        time_zone_offset += 1.0
    
    date_time = maybe_add_time_zone_offset(date_time, time_zone_offset)
    return build_format_time_embed(date_time)


@format_absolute.autocomplete('time_zone')
async def autocomplete_time_zone(value):
    """
    Autocompletes the given time zone value.
    
    This function is a coroutine.
    
    Parameters
    ----------
    value : `None | str`
        The typed in value.
    
    Returns
    -------
    suggestions : `list<str>`
    """
    return get_time_zone_suggestions(value)


@FORMAT_TIME_COMMANDS.interactions(name = 'now')
async def format_now():
    """
    Formats he current time.
    
    This function is a coroutine.
    
    Returns
    -------
    response : ``Embed``
    """
    return build_format_time_embed(DateTime.now(TimeZone.utc))


@FORMAT_TIME_COMMANDS.interactions(name = 'relative')
async def format_relative(
    years : ('number', 'years') = 0,
    months: ('number', 'days') = 0,
    weeks: ('number', 'weeks') = 0,
    days: ('number', 'days') = 0,
    hours: ('number', 'hours') = 0,
    minutes: ('number', 'minutes') = 0,
    seconds: ('number', 'seconds') = 0,
):
    """
    Format the given relative time.
    
    This function is a coroutine.
    
    Parameters
    ----------
    years : `int` = `0`, Optional
        Relative years.
    
    months : `int` = `0`, Optional
        Relative months.
    
    weeks : `int` = `0`, Optional
        Relative weeks.
    
    days : `int` = `0`, Optional
        Relative days.
    
    hours : `int` = `0`, Optional
        Relative hours.
    
    minutes : `int`
        Relative minutes.
    
    seconds : `int` = `0`, Optional
        Relative hours.
    
    Returns
    -------
    response : ``Embed``
    """
    check_relative_ranges(years, months, weeks, days, hours, minutes, seconds)
    delta = RelativeDelta(
        years = years,
        months = months,
        weeks = weeks,
        days = days,
        hours = hours,
        minutes = minutes,
        seconds = seconds,
    )
    
    return build_format_time_embed(DateTime.now(TimeZone.utc) + delta)


@FORMAT_TIME_COMMANDS.interactions(name = 'snowflake')
async def format_snowflake(
    snowflake: P('int', 'snowflake'),
):
    """
    Formats the given Discord id.
    
    This function is a coroutine.
    
    Parameters
    ----------
    snowflake : `int`
        The snowflake to convert to date.
    
    Returns
    -------
    response : ``Embed``
    """
    snowflake = bound_limit_snowflake(snowflake)
    return build_format_time_embed(id_to_datetime(snowflake))


@FORMAT_TIME_COMMANDS.interactions(name = 'unix')
async def format_unix(
    unix_time: P('number', 'unix time', min_value = UNIX_TIME_MIN, max_value = UNIX_TIME_MAX),
):
    """
    Formats the given unix time.
    
    This function is a coroutine.
    
    Parameters
    ----------
    unix_time : `int`
        The unix time to convert to date.
    
    Returns
    -------
    response : ``Embed``
    """
    return build_format_time_embed(unix_time_to_datetime(unix_time))
