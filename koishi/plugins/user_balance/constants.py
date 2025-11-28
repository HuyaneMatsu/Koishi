__all__ = ('USER_BALANCE_ALLOCATION_HOOKS',)

from collections import OrderedDict
from struct import Struct

from scarletio import WeakValueDictionary


USER_BALANCES = WeakValueDictionary()
USER_BALANCE_CACHE = OrderedDict()
USER_BALANCE_QUERY_TASKS = {}
USER_BALANCE_CACHE_SIZE = 100

USER_RELATIONSHIP_SLOTS_DEFAULT = 1

USER_BALANCE_SAVE_TASKS = {}

ALLOCATION_STRUCT = Struct(b'<HQQ')
ALLOCATION_STRUCT_SIZE = 18

USER_BALANCE_ALLOCATION_HOOKS = {}
