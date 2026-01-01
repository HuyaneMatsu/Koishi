from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....bot_utils.models import DB_ENGINE

from ...item_core import ITEM_ID_PEACH, get_item

from ..market_place_item import MarketPlaceItem
from ..queries import update_market_place_item


@vampytest.skip_if(DB_ENGINE is not None)
async def test__update_market_place_item():
    """
    Tests whether ``update_market_place_item`` works as intended.
    
    This function is a coroutine.
    """
    item = get_item(ITEM_ID_PEACH)
    item_amount = 30
    user_id = 202512220005
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
    
    query_called = False
    
    async def query_update_market_place_item_patched(input_market_place_item):
        nonlocal market_place_item
        nonlocal query_called
        vampytest.assert_is(market_place_item, input_market_place_item)
        query_called = True
    
    mocked = vampytest.mock_globals(
        update_market_place_item,
        query_update_market_place_item = query_update_market_place_item_patched,
    )
    
    await mocked(market_place_item)
    
    vampytest.assert_true(query_called)
