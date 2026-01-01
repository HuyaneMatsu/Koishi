from collections import deque as Deque
from datetime import datetime as DateTime, timedelta as TimeDelta, timezone as TimeZone

import vampytest
from scarletio import WeakValueDictionary

from ....bot_utils.models import DB_ENGINE

from ...item_core import ITEM_ID_BUNNY_SUIT, ITEM_ID_GARLIC, ITEM_ID_PEACH, get_item

from ..market_place_item import MarketPlaceItem
from ..queries import get_market_place_item_listing_inbox


def _iter_options():
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    user_id_0 = 202512230012
    user_id_1 = 202512230013
    user_id_2 = 202512230014
    
    item_0 = get_item(ITEM_ID_PEACH)
    item_1 = get_item(ITEM_ID_GARLIC)
    item_2 = get_item(ITEM_ID_BUNNY_SUIT)
    
    entry_id_00 = 123
    entry_id_01 = 124
    entry_id_02 = 125
    entry_id_03 = 126
    entry_id_04 = 127
    entry_id_05 = 128
    entry_id_06 = 129
    entry_id_07 = 130
    entry_id_08 = 131
    entry_id_09 = 132
    entry_id_10 = 133
    
    market_place_item_00 = MarketPlaceItem(
        item_0,
        1,
        user_id_0,
        1,
        now - TimeDelta(seconds = 3600),
        1,
    )
    market_place_item_00.entry_id = entry_id_00
    
    market_place_item_01 = MarketPlaceItem(
        item_0,
        1,
        user_id_1,
        1,
        now - TimeDelta(seconds = 3601),
        1,
    )
    market_place_item_01.entry_id = entry_id_01
    
    market_place_item_02 = MarketPlaceItem(
        item_0,
        1,
        user_id_2,
        1,
        now - TimeDelta(seconds = 3602),
        1,
    )
    market_place_item_02.entry_id = entry_id_02
    
    
    market_place_item_03 = MarketPlaceItem(
        item_1,
        1,
        user_id_0,
        1,
        now - TimeDelta(seconds = 3603),
        1,
    )
    market_place_item_03.entry_id = entry_id_03
    
    market_place_item_04 = MarketPlaceItem(
        item_1,
        1,
        user_id_1,
        1,
        now - TimeDelta(seconds = 3604),
        1,
    )
    market_place_item_04.entry_id = entry_id_04
    
    market_place_item_05 = MarketPlaceItem(
        item_1,
        1,
        user_id_2,
        1,
        now - TimeDelta(seconds = 3605),
        1,
    )
    market_place_item_05.entry_id = entry_id_05
    
    
    market_place_item_06 = MarketPlaceItem(
        item_2,
        1,
        user_id_0,
        1,
        now - TimeDelta(seconds = 3606),
        1,
    )
    market_place_item_06.entry_id = entry_id_06
    
    market_place_item_07 = MarketPlaceItem(
        item_2,
        1,
        user_id_1,
        1,
        now - TimeDelta(seconds = 3607),
        1,
    )
    market_place_item_07.entry_id = entry_id_07
    
    market_place_item_08 = MarketPlaceItem(
        item_2,
        1,
        user_id_2,
        1,
        now - TimeDelta(seconds = 3608),
        1,
    )
    market_place_item_08.entry_id = entry_id_08
    market_place_item_08.purchaser_user_id = user_id_0
    
    market_place_item_09 = MarketPlaceItem(
        item_0,
        1,
        user_id_0,
        1,
        now + TimeDelta(seconds = 3609),
        1,
    )
    market_place_item_09.entry_id = entry_id_09
    
    market_place_item_10 = MarketPlaceItem(
        item_0,
        1,
        user_id_0,
        1,
        now - TimeDelta(days = 8),
        1,
    )
    market_place_item_10.entry_id = entry_id_10
    
    market_place_items_patched = WeakValueDictionary()
    market_place_items_patched[entry_id_00] = market_place_item_00
    market_place_items_patched[entry_id_01] = market_place_item_01
    market_place_items_patched[entry_id_02] = market_place_item_02
    market_place_items_patched[entry_id_03] = market_place_item_03
    market_place_items_patched[entry_id_04] = market_place_item_04
    market_place_items_patched[entry_id_05] = market_place_item_05
    market_place_items_patched[entry_id_06] = market_place_item_06
    market_place_items_patched[entry_id_07] = market_place_item_07
    market_place_items_patched[entry_id_08] = market_place_item_08
    market_place_items_patched[entry_id_09] = market_place_item_09
    market_place_items_patched[entry_id_10] = market_place_item_10
    market_place_items_cache_patched = Deque()
    market_place_items_cache_patched.append(market_place_item_00)
    market_place_items_cache_patched.append(market_place_item_01)
    market_place_items_cache_patched.append(market_place_item_02)
    market_place_items_cache_patched.append(market_place_item_03)
    market_place_items_cache_patched.append(market_place_item_04)
    market_place_items_cache_patched.append(market_place_item_05)
    market_place_items_cache_patched.append(market_place_item_06)
    market_place_items_cache_patched.append(market_place_item_07)
    market_place_items_cache_patched.append(market_place_item_08)
    market_place_items_cache_patched.append(market_place_item_09)
    market_place_items_cache_patched.append(market_place_item_10)
    
    yield (
        user_id_0,
        now,
        0,
        3,
        market_place_items_patched,
        market_place_items_cache_patched,
        (
            [
                market_place_item_00,
                market_place_item_03,
                market_place_item_06,
            ],
            True,
        ),
    )
    
    yield (
        user_id_0,
        now,
        1,
        3,
        market_place_items_patched,
        market_place_items_cache_patched,
        (
            [
                market_place_item_08,
            ],
            False,
        ),
    )
    
    yield (
        user_id_0,
        now,
        0,
        10,
        market_place_items_patched,
        market_place_items_cache_patched,
        (
            [
                market_place_item_00,
                market_place_item_03,
                market_place_item_06,
                market_place_item_08,
            ],
            False,
        ),
    )


@vampytest.skip_if(DB_ENGINE is not None)
@vampytest._(vampytest.call_from(_iter_options()).returning_last())
async def test__get_market_place_item_listing_inbox(
    user_id, now, page_index, page_size, market_place_items_patched, market_place_items_cache_patched
):
    """
    Tests whether ``get_market_place_item_listing_inbox`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        Seller user's identifier.
    
    now : `DateTime`
        The current time.
    
    page_index : `int`
        The page's index to get.
    
    page_size : `int`
        The page's size to get.
    
    market_place_items_patched : ``WeakValueDictionary<int, MarketPlaceItem>``
        Market place items patched.
    
    market_place_items_cache_patched : ``Deque<MarketPlaceItem>``
        Market place items cace patched.
    
    Returns
    -------
    output : ``(list<MarketPlaceItem>, bool)``
    """
    market_place_items_patched = market_place_items_patched.copy()
    market_place_items_cache_patched = market_place_items_cache_patched.copy()
    
    mocked = vampytest.mock_globals(
        get_market_place_item_listing_inbox,
        2,
        MARKET_PLACE_ITEMS = market_place_items_patched,
        MARKET_PLACE_ITEMS_CACHE = market_place_items_cache_patched,
    )
    
    output = await mocked(user_id, now, page_index, page_size)
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(len(output), 2)
    market_place_items, has_more = output
    vampytest.assert_instance(market_place_items, list)
    for element in market_place_items:
        vampytest.assert_instance(element, MarketPlaceItem)
    vampytest.assert_instance(has_more, bool)
    return output
