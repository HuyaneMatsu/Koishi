__all__ = ()

from collections import OrderedDict
from scarletio import WeakValueDictionary


GUILD_STATS = WeakValueDictionary()
GUILD_STATS_CACHE = OrderedDict()
GUILD_STATS_CACHE_SIZE = 100
GUILD_STATS_SAVE_TASKS = {}
GUILD_STATS_QUERY_TASKS = {}
