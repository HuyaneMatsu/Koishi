__all__ = ('AMOUNT_TYPE_NAME_DEFAULT',)

from collections import OrderedDict
from datetime import datetime as DateTime, timezone as TimeZone


QUEST_TEMPLATES = {}
HOUR_IN_SECONDS = 3600
DAY_IN_SECONDS = 86400

AMOUNT_TYPE_NAME_DEFAULT = 'unknown'
QUEST_TYPE_NAME_DEFAULT = 'unknown'

UNIX_EPOCH = DateTime(1970, 1, 1, tzinfo = TimeZone.utc)

LINKED_QUEST_LISTING_CACHE = OrderedDict()
LINKED_QUEST_LISTING_CACHE_SIZE_MAX = 100
LINKED_QUEST_LISTING_GET_QUERY_TASKS = {}
