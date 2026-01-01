from collections import deque as Deque
from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from scarletio import WeakValueDictionary

from ....bot_utils.models import DB_ENGINE

from ...item_core import ITEM_ID_PEACH, get_item

from ..market_place_item import MarketPlaceItem
from ..queries import delete_market_place_item


@vampytest.skip_if(DB_ENGINE is not None)
async def test__delete_market_place_item():
    """
    Tests whether ``delete_market_place_item`` works as intended.
    
    This function is a coroutine.
    """
    item = get_item(ITEM_ID_PEACH)
    item_amount = 30
    user_id = 202512220006
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
    
    entry_id = 133
    market_place_item.entry_id = entry_id
    
    market_place_items_patched = WeakValueDictionary()
    market_place_items_patched[entry_id] = market_place_item
    market_place_items_cache_patched = Deque()
    market_place_items_cache_patched.append(market_place_item)
    
    mocked = vampytest.mock_globals(
        delete_market_place_item,
        2,
        MARKET_PLACE_ITEMS = market_place_items_patched,
        MARKET_PLACE_ITEMS_CACHE = market_place_items_cache_patched,
    )
    
    await mocked(market_place_item)
    
    vampytest.assert_eq(
        {*market_place_items_patched.keys()},
        set(),
    )
    vampytest.assert_eq(
        [*market_place_items_cache_patched],
        [],
    )
