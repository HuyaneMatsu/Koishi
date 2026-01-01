from collections import deque as Deque
from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from scarletio import WeakValueDictionary

from ....bot_utils.models import DB_ENGINE

from ...item_core import ITEM_ID_PEACH, get_item

from ..market_place_item import MarketPlaceItem
from ..queries import delete_market_place_item_listing


@vampytest.skip_if(DB_ENGINE is not None)
async def test__delete_market_place_item_listing():
    """
    Tests whether ``delete_market_place_item_listing`` works as intended.
    
    This function is a coroutine.
    """
    item = get_item(ITEM_ID_PEACH)
    item_amount = 30
    user_id = 202512230008
    balance_amount = 20
    finalises_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    initial_sell_fee = 100
    
    entry_id_0 = 133
    entry_id_1 = 134
    
    market_place_item_0 = MarketPlaceItem(
        item,
        item_amount,
        user_id,
        balance_amount,
        finalises_at,
        initial_sell_fee,
    )
    
    market_place_item_0.entry_id = entry_id_0
    
    market_place_item_1 = MarketPlaceItem(
        item,
        item_amount,
        user_id,
        balance_amount,
        finalises_at,
        initial_sell_fee,
    )
    
    market_place_item_1.entry_id = entry_id_1
    
    market_place_items_patched = WeakValueDictionary()
    market_place_items_patched[entry_id_0] = market_place_item_0
    market_place_items_patched[entry_id_1] = market_place_item_1
    market_place_items_cache_patched = Deque()
    market_place_items_cache_patched.append(market_place_item_0)
    market_place_items_cache_patched.append(market_place_item_1)
    
    mocked = vampytest.mock_globals(
        delete_market_place_item_listing,
        2,
        MARKET_PLACE_ITEMS = market_place_items_patched,
        MARKET_PLACE_ITEMS_CACHE = market_place_items_cache_patched,
    )
    
    await mocked([market_place_item_0, market_place_item_1])
    
    vampytest.assert_eq(
        {*market_place_items_patched.keys()},
        set(),
    )
    vampytest.assert_eq(
        [*market_place_items_cache_patched],
        [],
    )
