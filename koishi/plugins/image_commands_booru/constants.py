__all__ = ()

import re
from datetime import datetime as DateTime, timezone as TimeZone

from hata import BUILTIN_EMOJIS, Color, datetime_to_unix_time
from hata.ext.slash import Button


SESSION_ID = datetime_to_unix_time(DateTime.now(TimeZone.utc))

CLEANUP_AFTER = 300.0
CLEANUP_INTERVAL = 300.0

CUSTOM_ID_NEW_DISABLED = 'booru.ex.new'
CUSTOM_ID_TAGS_DISABLED = 'booru.ex.tags'
CUSTOM_ID_CLOSE = 'booru.close'

EMBED_COLOR = Color(0x138a50)

EMOJI_NEW = BUILTIN_EMOJIS['arrows_counterclockwise']
EMOJI_TAGS = BUILTIN_EMOJIS['notepad_spiral']
EMOJI_CLOSE = BUILTIN_EMOJIS['x']


BUTTON_CLOSE = Button(
    'Close',
    EMOJI_CLOSE,
    custom_id = CUSTOM_ID_CLOSE,
)

CACHES = {}


NOTE_TAG_RP = re.compile('\\(\\d*\\)')
SPACE_CHARACTERS = (' ', '\t', '\n', '\r', ',')
TAG_SPLIT = re.compile('[^ ,\\t\\r\\n]+')

AUTOCOMPLETE_VALUE_LENGTH_MAX = 100
