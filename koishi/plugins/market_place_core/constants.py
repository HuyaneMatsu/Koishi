__all__ = ('MARKET_PLACE_ITEM_FLAG_BUYER_RETRIEVED', 'MARKET_PLACE_ITEM_FLAG_SELLER_RETRIEVED',)

from collections import deque as Deque
from datetime import timedelta as TimeDelta

from scarletio import WeakValueDictionary

from ...bot_utils.models import DB_ENGINE


MARKET_PLACE_ITEMS = WeakValueDictionary()

if (DB_ENGINE is None):
    MARKET_PLACE_ITEMS_CACHE = Deque(maxlen = 1000)


FINALISED_KEPT_DURATION = TimeDelta(days = 7)

MARKET_PLACE_ITEM_FLAG_BUYER_RETRIEVED = 1 << 0
MARKET_PLACE_ITEM_FLAG_SELLER_RETRIEVED = 1 << 1
