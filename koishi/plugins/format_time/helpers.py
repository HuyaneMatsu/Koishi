__all__ = ()

from datetime import datetime as DateTime, timedelta as TimeDelta, timezone as TimeZone
from re import I as re_ignore_case, compile as re_compile, escape as re_escape


from hata import DATETIME_FORMAT_CODE, Embed, datetime_to_unix_time, elapsed_time, format_unix_time
from hata.ext.slash import abort

from .constants import (
    FORMAT_STYLES, EMBED_COLOR, ID_MAX, ID_MIN, RELATIVE_DAYS_MAX, RELATIVE_DAYS_MIN, RELATIVE_HOURS_MAX,
    RELATIVE_HOURS_MIN, RELATIVE_MINUTES_MAX, RELATIVE_MINUTES_MIN, RELATIVE_MONTHS_MAX, RELATIVE_MONTHS_MIN,
    RELATIVE_SECONDS_MAX, RELATIVE_SECONDS_MIN, RELATIVE_WEEKS_MAX, RELATIVE_WEEKS_MIN, RELATIVE_YEARS_MAX,
    RELATIVE_YEARS_MIN, TIME_ZONE_OFFSETS, TIME_ZONE_RP
)


def check_relative_ranges(years, months, weeks, days, hours, minutes, seconds):
    """
    Checks whether every relative date value is within the expected range.
    
    Parameters
    ----------
    years : `int`
        Relative years.
    
    months : `int`
        Relative months.
    
    weeks : `int`
        Relative weeks.
    
    days : `int`
        Relative days.
    
    hours : `int`
        Relative hours.
    
    minutes : `int`
        Relative minutes.
    
    seconds : `int`
        Relative hours.
    
    Raises
    ------
    interaction_aborted : ``InteractionAbortedError``
    """
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


def bound_limit_snowflake(snowflake):
    """
    Bounds limits the given snowflake.
    
    Parameters
    ----------
    snowflake : `int`
        The snowflake to limit.
    
    Returns
    -------
    snowflake : `int`
    """
    if snowflake < ID_MIN:
        snowflake = ID_MIN
    elif snowflake > ID_MAX:
        snowflake = ID_MAX
    
    return snowflake


def maybe_add_time_zone_offset(date_time, time_zone_offset):
    """
    Adds time zone offset to the given date time.
    
    Parameters
    ----------
    date_time : `DateTime`
        Date time to apply time zone offset.
    
    time_zone_offset : `float`
        Time zone offset to apply.
    
    Returns
    -------
    date_time : `DateTime`
    """
    if time_zone_offset != 0.0:
        date_time -= TimeDelta(hours = time_zone_offset)
    
    return date_time


def build_format_time_embed(date_time):
    """
    Builds a format time response embed.
    
    Parameters
    ----------
    date_time : `DateTime`
        The date time to build embed for.
    
    Returns
    -------
    embed : ``Embed``
    """
    unix_time = datetime_to_unix_time(date_time)
    now = DateTime.now(TimeZone.utc)
    
    formatted_date_times = [format_unix_time(unix_time, format_style) for format_style in FORMAT_STYLES]
    
    return Embed(
        'Formatting time',
        (
            f'UTC: {date_time:{DATETIME_FORMAT_CODE}} | '
            f'{elapsed_time(date_time)} {"ago" if now > date_time else "from now"}'
        ),
        color = EMBED_COLOR,
    ).add_field(
        'Output',
        '\n'.join([
            f'`{formatted_date_time}` {formatted_date_time}'
            for formatted_date_time in formatted_date_times
        ]),
    )


def build_suggested_time_zone(time_zone_name, time_zone_offset):
    """
    Builds a suggested time tone.
    
    Parameters
    ----------
    time_zone_name : `str`
        The time zone's name.
    
    time_zone_offset : `float`
        The time zone's offset.
    
    Returns
    -------
    suggestion : `str`
    """
    prefix = '+' if time_zone_offset >= 0.0 else '-'
    hours_float, minutes_ratio_float = divmod(abs(time_zone_offset), 1.0)
    hours = format(hours_float, '0>2.0f')
    minutes = format(minutes_ratio_float * 60.0, '0>2.0f')
    return f'{time_zone_name} ({prefix}{hours}:{minutes})'


def get_time_zone_suggestions(name):
    """
    Auto completes the given time zone name.
    
    This function is a coroutine.
    
    Parameters
    ----------
    name : `None | str`
        Time zone name.
    
    Returns
    -------
    suggestions : `list<str>`
    """
    if name is None:
        return [build_suggested_time_zone(*item) for item in sorted(TIME_ZONE_OFFSETS.items())[:25]]
    
    match = TIME_ZONE_RP.fullmatch(name)
    if (match is not None):
        name = match.group(1)
    
    time_zone_pattern = re_compile('.*?'.join(re_escape(char) for char in name), re_ignore_case)
    matches = []
    
    for (time_zone_name, time_zone_offset) in TIME_ZONE_OFFSETS.items():
        parsed = time_zone_pattern.search(time_zone_name)
        if parsed is None:
            continue
        
        match_start = parsed.start()
        match_length = parsed.end() - match_start
        
        matches.append(((time_zone_name, time_zone_offset), (match_length, match_start)))
    
    if not matches:
        return []
    
    matches.sort()
    return [build_suggested_time_zone(*item[0]) for item in matches]


def get_time_zone_offset(name):
    """
    Gets the zone offset for the given name.
    
    Parameters
    ----------
    name : `str`
        The name to get time zone offset for.
    
    Returns
    -------
    time_zone_offset : `float`
    """
    match = TIME_ZONE_RP.fullmatch(name)
    if (match is not None):
        name = match.group(1)
    
    try:
        return TIME_ZONE_OFFSETS[name]
    except KeyError:
        pass
    
    time_zone_pattern = re_compile('.*?'.join(re_escape(char) for char in name), re_ignore_case)

    accurate_time_zone_offset = None
    accurate_match_key = None
    
    for time_zone_name, time_zone_offset in TIME_ZONE_OFFSETS.items():
        parsed = time_zone_pattern.search(time_zone_name)
        if parsed is None:
            continue
        
        match_start = parsed.start()
        match_length = parsed.end() - match_start
        
        match_rate = (match_length, match_start)
        if (accurate_match_key is not None) and (accurate_match_key < match_rate):
            continue
        
        accurate_time_zone_offset = time_zone_offset
        accurate_match_key = match_rate
    
    return accurate_time_zone_offset
