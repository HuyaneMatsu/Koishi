__all__ = ()

from re import compile as re_compile, escape as re_escape
from datetime import timedelta as TimeDelta

from hata import AnsiForegroundColor, BUILTIN_EMOJIS, Permission, create_ansi_format_code
from hata.ext.slash import Button


DELTA_DAY = TimeDelta(days = 1)

PAGE_SIZE = 20

TYPE_BAN = 1 << 0
TYPE_KICK = 1 << 1
TYPE_MUTE = 1 << 2
TYPE_ALL = TYPE_BAN | TYPE_KICK | TYPE_MUTE

NAME_BAN = 'ban'
NAME_KICK = 'kick'
NAME_MUTE = 'mute'
NAME_ALL = 'all'

TYPES = [
    (NAME_ALL, TYPE_ALL),
    (NAME_BAN, TYPE_BAN),
    (NAME_KICK, TYPE_KICK),
    (NAME_MUTE, TYPE_MUTE),
]

TYPE_TO_NAME = {value: name for name, value in TYPES}

SORT_KEY_ALL = lambda item: (item[1].all, 0 - item[0].id)

SORT_KEYS_BY_TYPE = {
    TYPE_BAN: lambda item: (item[1].ban, 0 - item[0].id),
    TYPE_KICK: lambda item: (item[1].kick, 0 - item[0].id),
    TYPE_MUTE: lambda item: (item[1].mute, 0 - item[0].id),
    TYPE_ALL: SORT_KEY_ALL,
}

STYLE_NUMBER = create_ansi_format_code(text_decoration = AnsiForegroundColor.white)
STYLE_NAME = create_ansi_format_code(text_decoration = AnsiForegroundColor.white)
STYLE_BAN = create_ansi_format_code(text_decoration = AnsiForegroundColor.blue)
STYLE_KICK = create_ansi_format_code(text_decoration = AnsiForegroundColor.teal)
STYLE_MUTE = create_ansi_format_code(text_decoration = AnsiForegroundColor.green)
STYLE_ALL = create_ansi_format_code(text_decoration = AnsiForegroundColor.orange)
STYLE_FOCUS = create_ansi_format_code(text_decoration = AnsiForegroundColor.pink)


NAME_BAN_HEADER = NAME_BAN.upper()
NAME_KICK_HEADER = NAME_KICK.upper()
NAME_MUTE_HEADER = NAME_MUTE.upper()
NAME_ALL_HEADER = NAME_ALL.upper()


EMOJI_PAGE_PREVIOUS = BUILTIN_EMOJIS['arrow_left']
EMOJI_PAGE_NEXT = BUILTIN_EMOJIS['arrow_right']
EMOJI_CLOSE = BUILTIN_EMOJIS['x']

PAGE_MIN = 0
PAGE_MAX = 98

DAYS_MIN = 1
DAYS_MAX = 45

CUSTOM_ID_PAGE_BASE = 'mod.top_list.page.'
CUSTOM_ID_PAGE_BACK_DISABLED = f'{CUSTOM_ID_PAGE_BASE}n-1.disabled'
CUSTOM_ID_NEXT_DISABLED = f'{CUSTOM_ID_PAGE_BASE}.n+1.disabled'
CUSTOM_ID_CLOSE = 'mod.top_list.close'
CUSTOM_ID_PAGE_RP = re_compile(f'{re_escape(CUSTOM_ID_PAGE_BASE)}(\d+);s=(\d+);d=(\d+)')

BUTTON_PAGE_PREVIOUS_DISABLED = Button(
    f'Page {PAGE_MIN}',
    EMOJI_PAGE_PREVIOUS,
    custom_id = CUSTOM_ID_PAGE_BACK_DISABLED,
    enabled = False,
)

BUTTON_PAGE_NEXT_DISABLED = Button(
    f'Page {PAGE_MAX + 2}',
    EMOJI_PAGE_NEXT,
    custom_id = CUSTOM_ID_NEXT_DISABLED,
    enabled = False,
)

BUTTON_CLOSE = Button(
    'Close',
    EMOJI_CLOSE,
    custom_id = CUSTOM_ID_CLOSE,
)


REQUIRED_PERMISSIONS_USER_VALUE = Permission().update_by_keys(
    ban_users = True,
    kick_users = True,
    moderate_users = True,
    view_audit_logs = True,
)

REQUIRED_PERMISSIONS_USER_NAME = 'ban, kick, moderate users and view audit logs'


REQUIRED_PERMISSIONS_CLIENT_VALUE = Permission().update_by_keys(
    view_audit_logs = True,
)
REQUIRED_PERMISSIONS_CLIENT_NAME = 'view audit logs'
