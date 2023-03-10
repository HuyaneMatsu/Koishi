__all__ = ()

from hata import AnsiForegroundColor, BUILTIN_EMOJIS, create_ansi_format_code
from hata.ext.slash import Button


EMOJI_BACK = BUILTIN_EMOJIS['arrow_backward']
EMOJI_NEXT = BUILTIN_EMOJIS['arrow_forward']
EMOJI_CLOSE = BUILTIN_EMOJIS['x']

MONTH_NAMES = {
    1: 'January',
    2: 'February',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'August',
    9: 'September',
    10: 'October',
    11: 'November',
    12: 'December',
}

DAY_NAMES = {
    0: 'Monday',
    1: 'Tuesday',
    2: 'Wednesday',
    3: 'Thursday',
    4: 'Fumo Friday',
    5: 'Saturday',
    6: 'Sunday',
}

DAY_NAMES_SHORT = {
    0: 'Mon',
    1: 'Tue',
    2: 'Wed',
    3: 'Thu',
    4: 'Fri',
    5: 'Sat',
    6: 'Sun',
}


MONTH_MIN = 1
MONTH_MAX = 12

YEAR_MIN = 1900
YEAR_MAX = 2200


CUSTOM_ID_BACK_DISABLED = 'touhou_calendar.year.min.disabled'
CUSTOM_ID_NEXT_DISABLED = 'touhou_calendar.year.max.disabled'
CUSTOM_ID_CLOSE = 'touhou_calendar.close'


BUTTON_BACK_DISABLED = Button(
    str(YEAR_MIN - 1),
    EMOJI_BACK,
    custom_id = CUSTOM_ID_BACK_DISABLED,
    enabled = False,
)

BUTTON_NEXT_DISABLED = Button(
    str(YEAR_MAX + 1),
    EMOJI_NEXT,
    custom_id = CUSTOM_ID_NEXT_DISABLED,
    enabled = False,
)

BUTTON_CLOSE = Button(
    'Close',
    EMOJI_CLOSE,
    custom_id = CUSTOM_ID_CLOSE,
)

COLOR_CODE_BLACK = create_ansi_format_code(foreground_color = AnsiForegroundColor.black)
COLOR_CODE_RED = create_ansi_format_code(foreground_color = AnsiForegroundColor.red)
COLOR_CODE_GREEN = create_ansi_format_code(foreground_color = AnsiForegroundColor.green)
COLOR_CODE_ORANGE = create_ansi_format_code(foreground_color = AnsiForegroundColor.orange)
COLOR_CODE_BLUE = create_ansi_format_code(foreground_color = AnsiForegroundColor.blue)
COLOR_CODE_PINK = create_ansi_format_code(foreground_color = AnsiForegroundColor.pink)
COLOR_CODE_TEAL = create_ansi_format_code(foreground_color = AnsiForegroundColor.teal)
COLOR_CODE_WHITE = create_ansi_format_code(foreground_color = AnsiForegroundColor.white)

COLOR_CODE_RESET = create_ansi_format_code()
