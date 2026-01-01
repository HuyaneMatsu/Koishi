from collections import deque as Deque
from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from scarletio import WeakValueDictionary

from ....bot_utils.models import DB_ENGINE

from ...item_core import ITEM_ID_PEACH, get_item

from ..market_place_item import MarketPlaceItem
from ..queries import insert_market_place_item


@vampytest.skip_if(DB_ENGINE is not None)
async def test__insert_market_place_item():
    """
    Tests whether ``insert_market_place_item`` works as intended.
    
    This function is a coroutine.
    """
    item = get_item(ITEM_ID_PEACH)
    item_amount = 30
    user_id = 202512220004
    balance_amount = 20
    finalises_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    initial_sell_fee = 100
    
    market_place_item = MarketPlaceItem(
        item,
        item_amount,
        user_id,
        balance_amount,
        finalises_at,
        initial_sell_fee,
    )
    
    market_place_items_patched = WeakValueDictionary()
    market_place_items_cache_patched = Deque()
    
    mocked = vampytest.mock_globals(
        insert_market_place_item,
        2,
        MARKET_PLACE_ITEMS = market_place_items_patched,
        MARKET_PLACE_ITEMS_CACHE = market_place_items_cache_patched,
    )
    
    await mocked(market_place_item)
    
    vampytest.assert_true(market_place_item.entry_id)
    vampytest.assert_eq(
        {*market_place_items_patched.keys()},
        {market_place_item.entry_id},
    )
    vampytest.assert_eq(
        [*market_place_items_cache_patched],
        [market_place_item],
    )
