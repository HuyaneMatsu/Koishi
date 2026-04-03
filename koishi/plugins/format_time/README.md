# Format time

Allows inputting time and outputs it in various embedded formats.


# Commands

- `/format-time`
    - `/format_absolute(
        years : int<min = 1970, max = 3000> = 0,
        months : int<min = 1, max = 12> = 1,
        days : int<min = 1, max = 31 = 1,
        hours : int<min = 0, max = 23> = 0,
        minutes : int<min = 0, max = 59> = 0,
        seconds : int<min = 0, max = 59> = 0
        time_zone : null | Autocomplete = null,
        daylight_saving_time : bool = false,
    )`
    - `/format_now`
    - `/format_relative (
        years : int = 0,
        months : int = 0,
        weeks : int = 0,
        days : int = 0,
        hours : int = 0,
        minutes : int = 0,
        seconds : int = 0
    )`
    - `/format_snowflake (snowflake : int)`
    - `/format_unix (unix_time : int<min = 0, max = 32503680000>)`
