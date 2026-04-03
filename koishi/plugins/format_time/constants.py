__all__ = ()

from re import compile as re_compile
from hata import Color, TIMESTAMP_STYLES, unix_time_to_id
from hata.discord.utils import UNIX_TIME_MAX


TIME_ZONE_RP = re_compile('(.*?)\\s*(?:\\([+-]\\d\\d\\:\\d\\d\\))?\\s*')

EMBED_COLOR = Color(0x6EC8A9)

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


RELATIVE_YEARS_MIN = -100
RELATIVE_YEARS_MAX = +100

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


TIME_ZONE_OFFSETS = {
    'Pacific/Tongatapu'         : +13.0,
    
    'Pacific/Auckland'          : +12.0,
    'Pacific/Fiji'              : +12.0,
    
    'Pacific/Guadalcanal'       : +11.0,
    
    'Asia/Vladivostok'          : +10.0,
    'Australia/Brisbane'        : +10.0,
    'Australia/Hobart'          : +10.0,
    'Australia/Sydney'          : +10.0,
    'Pacific/Guam'              : +10.0,
    
    'Australia/Adelaide'        : + 9.5,
    'Australia/Darwin'          : + 9.5,
    
    'Asia/Seoul'                : + 9.0,
    'Asia/Tokyo'                : + 9.0,
    'Asia/Yakutsk'              : + 9.0,
    
    'Asia/Hong Kong'            : + 8.0,
    'Asia/Irkutsk'              : + 8.0,
    'Asia/Taipei'               : + 8.0,
    'Australia/Perth'           : + 8.0,
    
    'Asia/Bangkok'              : + 7.0,
    
    'Asia/Rangoon'              : + 6.5,
    
    'Asia/Dhaka'                : + 6.0,
    
    'Asia/Chennai'              : + 5.5,
    'Asia/Kolkata'              : + 5.5,
    'Asia/New Delhi'            : + 5.5,
    'Asia/Mumbai'               : + 5.5,

    'Asia/Karachi'              : + 5.0,
    'Asia/Katmandu'             : + 5.0,
    'Asia/Yekaterinburg'        : + 5.0,
    
    'Asia/Baku'                 : + 4.0,
    'Asia/Muscat'               : + 4.0,
    
    'Asia/Tehran'               : + 3.5,
    
    'Asia/Baghdad'              : + 3.0,
    'Asia/Kuwait'               : + 3.0,
    'Europe/Moscow'             : + 3.0,
    
    'Africa/Cairo'              : + 2.0,
    'Africa/Harare'             : + 2.0,
    'Asia/Jerusalem'            : + 2.0,
    'Europe/Bucharest'          : + 2.0,
    'Europe/Helsinki'           : + 2.0,
    
    'Africa/Douala'             : + 1.0,
    'Europe/Copenhagen'         : + 1.0,
    'Europe/Sarajevo'           : + 1.0,
    
    'Atlantic/Azores'           : - 1.0,
    'Atlantic/Cape Verde'       : - 1.0,
    
    'America/Buenos Aires'      : - 3.0,
    'America/Montevideo'        : - 3.0,
    'America/Godthab'           : - 3.0,
    'America/Sao Paulo'         : - 3.0,
    'SA Eastern Standard Time'  : - 3.0,
    
    'Canada/Newfoundland'       : - 3.5,
    
    'America/Aruba'             : - 4.0,
    
    'America/Caracas'           : - 4.5,
    
    'America/Bogota'            : - 5.0,
    'America/Halifax'           : - 5.0,
    'America/New York'          : - 5.0,
    
    'Canada/Saskatchewan'       : - 6.0,
    'America/Chicago'           : - 6.0,
    'America/Mexico City'       : - 6.0,
    
    'America/Denver'            : - 7.0,
    'America/Mazatlan'          : - 7.0,
    'America/Phoenix'           : - 7.0,
    
    'America/Los Angeles'       : - 8.0,
    
    'America/Anchorage'         : - 9.0,
    
    'Pacific/Honolulu'          : -10.0,
    
    'Pacific/Midway'            : -11.0,
}
