from collections import deque as Deque
from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from scarletio import WeakValueDictionary

from ....bot_utils.models import DB_ENGINE

from ...item_core import ITEM_ID_PEACH, get_item

from ..market_place_item import MarketPlaceItem
from ..queries import get_market_place_item


def _iter_options():
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    user_id = 202512260002
    
    entry_id_00 = 123
    entry_id_01 = 124
    
    item = get_item(ITEM_ID_PEACH)
    
    market_place_item_00 = MarketPlaceItem(
        item,
        1,
        user_id,
        1,
        now,
        1,
    )
    market_place_item_00.entry_id = entry_id_00
    
    market_place_item_01 = MarketPlaceItem(
        item,
        1,
        user_id,
        1,
        now,
        1,
    )
    market_place_item_01.entry_id = entry_id_01
    
    
    market_place_items_patched = WeakValueDictionary()
    market_place_items_patched[entry_id_00] = market_place_item_00
    market_place_items_patched[entry_id_01] = market_place_item_01
    market_place_items_cache_patched = Deque()
    market_place_items_cache_patched.append(market_place_item_00)
    market_place_items_cache_patched.append(market_place_item_01)
    
    yield (
        entry_id_01,
        market_place_items_patched,
        market_place_items_cache_patched,
        market_place_item_01,
    )
    
    yield (
        0,
        market_place_items_patched,
        market_place_items_cache_patched,
        None,
    )


@vampytest.skip_if(DB_ENGINE is not None)
@vampytest._(vampytest.call_from(_iter_options()).returning_last())
async def test__get_market_place_item(
    entry_id, market_place_items_patched, market_place_items_cache_patched
):
    """
    Tests whether ``get_market_place_item`` works as intended.
    
    Parameters
    ----------
    entry_id : `int`
        The entry's identifier.
    
    market_place_items_patched : ``WeakValueDictionary<int, MarketPlaceItem>``
        Market place items patched.
    
    market_place_items_cache_patched : ``Deque<MarketPlaceItem>``
        Market place items cace patched.
    
    Returns
    -------
    output : ``None | MarketPlaceItem``
    """
    market_place_items_patched = market_place_items_patched.copy()
    market_place_items_cache_patched = market_place_items_cache_patched.copy()
    
    mocked = vampytest.mock_globals(
        get_market_place_item,
        2,
        MARKET_PLACE_ITEMS = market_place_items_patched,
        MARKET_PLACE_ITEMS_CACHE = market_place_items_cache_patched,
    )
    
    output = await mocked(entry_id)
    vampytest.assert_instance(output, MarketPlaceItem, nullable = True)
    return output
