__all__ = ()

from datetime import datetime as DateTime, timedelta as TimeDelta, timezone as TimeZone

from dateutil.relativedelta import relativedelta as RelativeDelta
from hata import (
    DATETIME_FORMAT_CODE, Embed, TIMESTAMP_STYLES, datetime_to_unix_time, elapsed_time, format_unix_time,
    id_to_datetime, unix_time_to_datetime, unix_time_to_id
)
from hata.discord.utils import DATETIME_MAX, DATETIME_MIN, UNIX_TIME_MAX, UNIX_TIME_MIN
from hata.ext.slash import P, abort

from ..bots import FEATURE_CLIENTS


P_TIME_ZONE = P('float', 'timezone offset from utc 0', min_value = -26.0, max_value = +26.0)
ID_MIN = 0
ID_MAX = unix_time_to_id(UNIX_TIME_MAX)


FORMAT_STYLES = (
    TIMESTAMP_STYLES.short_time,
    TIMESTAMP_STYLES.long_time,
    TIMESTAMP_STYLES.short_date,
    TIMESTAMP_STYLES.long_date,
    TIMESTAMP_STYLES.short_date_time,
    TIMESTAMP_STYLES.long_date_time,
    TIMESTAMP_STYLES.relative_time,
)


FORMAT_TIME_COMMANDS = FEATURE_CLIENTS.interactions(
    None,
    integration_types = ['guild_install', 'user_install'],
    is_global = True,
    name = 'format-time',
    description = 'Formats the given time.',
)


def maybe_add_time_zone_offset(date_time, time_zone_offset):
    if time_zone_offset != 0.0:
        date_time += TimeDelta(hours = time_zone_offset)
        
    return date_time


RELATIVE_YEARS_MIN = -100
RELATIVE_YEARS_MAX = 100

RELATIVE_MONTHS_MIN = RELATIVE_YEARS_MIN * 12
RELATIVE_MONTHS_MAX = RELATIVE_YEARS_MAX * 12

RELATIVE_WEEKS_MIN = RELATIVE_MONTHS_MIN * 4
RELATIVE_WEEKS_MAX = RELATIVE_MONTHS_MAX * 4

RELATIVE_DAYS_MIN = RELATIVE_WEEKS_MIN * 7
RELATIVE_DAYS_MAX = RELATIVE_WEEKS_MAX * 7

RELATIVE_HOURS_MIN = RELATIVE_DAYS_MIN * 24
RELATIVE_HOURS_MAX = RELATIVE_DAYS_MAX * 24

RELATIVE_MINUTES_MIN = RELATIVE_HOURS_MIN * 60
RELATIVE_MINUTES_MAX = RELATIVE_HOURS_MAX * 60

RELATIVE_SECONDS_MIN = RELATIVE_MINUTES_MIN * 60
RELATIVE_SECONDS_MAX = RELATIVE_MINUTES_MAX * 60


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
    """Format the given relative time."""
    if (years < RELATIVE_YEARS_MIN) or (years > RELATIVE_YEARS_MAX):
        abort('years out of allowed range')
        
    if (months < RELATIVE_MONTHS_MIN) or (months > RELATIVE_MONTHS_MAX):
        abort('months out of allowed range')
    
    if (weeks < RELATIVE_WEEKS_MIN) or (weeks > RELATIVE_WEEKS_MAX):
        abort('weeks out of allowed range')
    
    if (days < RELATIVE_DAYS_MIN) or (days > RELATIVE_DAYS_MAX):
        abort('days out of allowed range')
    
    if (hours < RELATIVE_HOURS_MIN) or (hours > RELATIVE_HOURS_MAX):
        abort('hours out of allowed range')
    
    if (minutes < RELATIVE_MINUTES_MIN) or (minutes > RELATIVE_MINUTES_MAX):
        abort('minutes out of allowed range')
    
    if (seconds < RELATIVE_SECONDS_MIN) or (seconds > RELATIVE_SECONDS_MAX):
        abort('seconds out of allowed range')
    
    delta = RelativeDelta(
        years = years,
        months = months,
        weeks = weeks,
        days = days,
        hours = hours,
        minutes = minutes,
        seconds = seconds,
    )
    
    return build_format_embed(DateTime.now(TimeZone.utc) + delta)


@FORMAT_TIME_COMMANDS.interactions(name = 'absolute')
async def format_absolute(
    year : P('number', 'year', min_value = DATETIME_MIN.year, max_value = DATETIME_MAX.year) = 0,
    month: P('number', 'days', min_value = 1, max_value = 12) = 1,
    day: P('number', 'days', min_value = 1, max_value = 31) = 1,
    hour: P('number', 'hours', min_value = 0, max_value = 23) = 0,
    minute: P('number', 'minutes', min_value = 0, max_value = 59) = 0,
    second: P('number', 'seconds', min_value = 0, max_value = 59) = 0,
    time_zone_offset: P_TIME_ZONE = 0.0,
):
    """Formats the given time."""
    try:
        date_time = DateTime(year, month, day, hour, minute, second, tzinfo = TimeZone.utc)
    except (ValueError, OverflowError) as err:
        error_parameters = err.args
        if error_parameters:
            error_message = error_parameters[0]
        else:
            error_message = 'Undefined value error occurred.'
        
        return abort(error_message)
    
    date_time = maybe_add_time_zone_offset(date_time, time_zone_offset)
    return build_format_embed(date_time)


@FORMAT_TIME_COMMANDS.interactions(name = 'unix')
async def format_unix(
    unix_time: P('number', 'unix time', min_value = UNIX_TIME_MIN, max_value = UNIX_TIME_MAX),
):
    """Formats the given unix time."""
    return build_format_embed(unix_time_to_datetime(unix_time))


@FORMAT_TIME_COMMANDS.interactions(name = 'snowflake')
async def format_snowflake(
    snowflake: P('int', 'snowflake'),
):
    """Formats the given Discord id."""
    if snowflake < ID_MIN:
        snowflake = ID_MIN
    elif snowflake > ID_MAX:
        snowflake = ID_MAX
    
    return build_format_embed(id_to_datetime(snowflake))


@FORMAT_TIME_COMMANDS.interactions(name = 'now')
async def format_now():
    """Formats he current time"""
    return build_format_embed(DateTime.now(TimeZone.utc))


def build_format_embed(date_time):
    unix_time = datetime_to_unix_time(date_time)
    now = DateTime.now(TimeZone.utc)
    
    formatted_date_times = [format_unix_time(unix_time, format_style) for format_style in FORMAT_STYLES]
    
    return Embed(
        'Formatting time',
        (
            f'UTC: {date_time:{DATETIME_FORMAT_CODE}} | '
            f'{elapsed_time(date_time)} {"ago" if now > date_time else "from now"}'
        ),
        color = 0x6EC8A9,
    ).add_field(
        'Output',
        '\n'.join([
            f'`{formatted_date_time}` {formatted_date_time}'
            for formatted_date_time in formatted_date_times
        ]),
    )
