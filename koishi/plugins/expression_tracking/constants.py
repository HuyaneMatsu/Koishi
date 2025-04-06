__all__ = ()

from collections import OrderedDict
from datetime import timedelta as TimeDelta

from dateutil.relativedelta import relativedelta as RelativeDelta
from hata import Permission
from scarletio import ScarletLock, get_event_loop


ACTION_TYPE_EMOJI_CONTENT = 1
ACTION_TYPE_EMOJI_REACTION = 2
ACTION_TYPE_STICKER = 3

PERMISSION_MASK = Permission().update_by_keys(view_channel = True)

RELATIVE_MONTH = RelativeDelta(months = 1)

MONTH = TimeDelta(days = 367, hours = 6) / 12

STATISTIC_CACHE = OrderedDict()
STATISTIC_CACHE_SIZE_MAX = OrderedDict
STATISTIC_CACHE_TIMEOUT = 300.0

STATISTIC_QUERY_TASKS = {}

TRACKING_QUERY_LOCK = ScarletLock(get_event_loop(), 5)
