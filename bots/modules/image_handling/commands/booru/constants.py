__all__ = ()

import re
from datetime import datetime as DateTime

from hata import datetime_to_unix_time
from hata.ext.slash import Button

from ...constants import EMOJI_CLOSE


SESSION_ID = datetime_to_unix_time(DateTime.utcnow())

CLEANUP_AFTER = 300.0
CLEANUP_INTERVAL = 300.0

CUSTOM_ID_NEW_DISABLED = 'booru.ex.new'
CUSTOM_ID_TAGS_DISABLED = 'booru.ex.tags'
CUSTOM_ID_CLOSE = 'booru.close'


BUTTON_CLOSE = Button(
    'Close',
    EMOJI_CLOSE,
    custom_id = CUSTOM_ID_CLOSE,
)

CACHES = {}


NOTE_TAG_RP = re.compile('\\(\\d*\\)')
SPACE_CHARACTERS = (' ', '\t', '\n', '\r')


AUTOCOMPLETE_VALUE_LENGTH_MAX = 100
