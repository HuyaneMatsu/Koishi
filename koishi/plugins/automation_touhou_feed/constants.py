__all__ = ()

import re

from dateutil.relativedelta import relativedelta as RelativeDelta
from hata import AnsiForegroundColor, BUILTIN_EMOJIS, Permission, create_ansi_format_code, elapsed_time
from hata.ext.slash import Button, Row


FEEDERS = {}

TAG_NAME_REQUIRED = 'touhou-feed'
TAG_NAME_SOLO = 'solo'

DEFAULT_INTERVAL = 4 * 3600
MIN_INTERVAL = 15 * 60
MAX_INTERVAL = 24 * 3600

PERMISSION_MASK_EMBED_LINKS = Permission().update_by_keys(embed_links = True)


TAG_REQUIRED_RP = re.compile(f'(?:\\s|^)#{TAG_NAME_REQUIRED}(?:\\s|$)', re.M | re.U)
TAG_ITER_RP = re.compile(f'(?:\\s|^)#([\\w\\-\\_\\+\\:]+)', re.M | re.U)

INTERVAL_RP = re.compile(f'interval(?:lum)?\\s*\\:((?:\\s*\\d+\\s*[hms])+)')
INTERVAL_UNIT_RP = re.compile('0*?(\\d+)\\s*([hms])')



STYLE_RESET = create_ansi_format_code()
STYLE_RED = create_ansi_format_code(foreground_color = AnsiForegroundColor.red)
STYLE_GREEN = create_ansi_format_code(foreground_color = AnsiForegroundColor.green)
STYLE_BLUE = create_ansi_format_code(foreground_color = AnsiForegroundColor.blue)

MIN_DELTA = elapsed_time(RelativeDelta(seconds = MIN_INTERVAL))
MAX_DELTA = elapsed_time(RelativeDelta(seconds = MAX_INTERVAL))
DEFAULT_DELTA = elapsed_time(RelativeDelta(seconds = DEFAULT_INTERVAL))

EMOJI_PAGE_PREVIOUS = BUILTIN_EMOJIS['arrow_left']
EMOJI_PAGE_NEXT = BUILTIN_EMOJIS['arrow_right']
EMOJI_REFRESH = BUILTIN_EMOJIS['arrows_counterclockwise']
EMOJI_CLOSE = BUILTIN_EMOJIS['x']

CUSTOM_ID_CLOSE = 'touhou_feed.close'

CUSTOM_ID_PAGE_BASE = 'touhou_feed.page.'
CUSTOM_ID_REFRESH_BASE = 'touhou_feed.refresh.'

CUSTOM_ID_PAGE_PREVIOUS_DISABLED = CUSTOM_ID_PAGE_BASE + 'd1'
CUSTOM_ID_PAGE_NEXT_DISABLED = CUSTOM_ID_PAGE_BASE + 'd2'

CUSTOM_ID_ABOUT_MAIN = 'touhou_feed.about.main'
CUSTOM_ID_ABOUT_EXAMPLES = 'touhou_feed.about.examples'
CUSTOM_ID_ABOUT_INTERVAL = 'touhou_feed.about.interval'


BUTTON_PREVIOUS_DISABLED = Button(
    emoji = EMOJI_PAGE_PREVIOUS,
    custom_id = CUSTOM_ID_PAGE_PREVIOUS_DISABLED,
    enabled = False,
)

BUTTON_NEXT_DISABLED = Button(
    emoji = EMOJI_PAGE_NEXT,
    custom_id = CUSTOM_ID_PAGE_NEXT_DISABLED,
    enabled = False,
)

BUTTON_REFRESH_BASE = Button(
    'Refresh',
    EMOJI_REFRESH,
)
    
BUTTON_CLOSE = Button(
    'Close',
    EMOJI_CLOSE,
    custom_id = CUSTOM_ID_CLOSE,
)

BUTTON_ABOUT_MAIN = Button(
    'About',
    custom_id = CUSTOM_ID_ABOUT_MAIN,
)

BUTTON_ABOUT_EXAMPLES = Button(
    'Examples',
    custom_id = CUSTOM_ID_ABOUT_EXAMPLES,
)

BUTTON_ABOUT_INTERVAL = Button(
    'Interval',
    custom_id = CUSTOM_ID_ABOUT_INTERVAL,
)

COMPONENTS_ABOUT_MAIN = Row(
    BUTTON_ABOUT_MAIN.copy_with(enabled = False),
    BUTTON_ABOUT_EXAMPLES,
    BUTTON_ABOUT_INTERVAL,
    BUTTON_CLOSE,
)

COMPONENTS_ABOUT_EXAMPLES = Row(
    BUTTON_ABOUT_MAIN,
    BUTTON_ABOUT_EXAMPLES.copy_with(enabled = False),
    BUTTON_ABOUT_INTERVAL,
    BUTTON_CLOSE,
)

COMPONENTS_ABOUT_INTERVAL = Row(
    BUTTON_ABOUT_MAIN,
    BUTTON_ABOUT_EXAMPLES,
    BUTTON_ABOUT_INTERVAL.copy_with(enabled = False),
    BUTTON_CLOSE,
)

DISPLAY_PER_PAGE = min(25 // 3, 4)
