__all__ = ()

from collections import OrderedDict
from scarletio import WeakValueDictionary


INVENTORIES = WeakValueDictionary()
INVENTORY_CACHE = OrderedDict()
INVENTORY_CACHE_SIZE_MAX = 100


INVENTORY_GET_TASKS = {}
INVENTORY_SAVE_TASKS = {}
