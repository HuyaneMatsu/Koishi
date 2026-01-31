from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from hata import Component, create_button, create_section, create_text_display

from ...item_core import ITEM_ID_PEACH, get_item
from ...market_place_core import MarketPlaceItem
from ...user_balance import ALLOCATION_FEATURE_ID_MARKET_PLACE

from ..component_building_market_place import build_market_place_entry_component


def _iter_options():
    user_id_0 = 202512280000
    user_id_1 = 202512280001
    item = get_item(ITEM_ID_PEACH)
    finalises_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    entry_id = 1233
    balance_amount = 200
    page_index = 1
    
    market_place_item = MarketPlaceItem(
        item,
        30,
        user_id_0,
        0,
        finalises_at,
        0,
    )
    market_place_item.entry_id = entry_id
    market_place_item.purchaser_user_id = user_id_1
    market_place_item.purchaser_balance_amount = balance_amount
    
    yield (
        user_id_1,
        page_index,
        entry_id,
        balance_amount,
        create_section(
            create_text_display(
                '`/market-place` allocating 200'
            ),
            thumbnail = create_button(
                'Details',
                custom_id = (
                    f'allocations.details.{user_id_1:x}.{page_index:x}.{ALLOCATION_FEATURE_ID_MARKET_PLACE:x}.{entry_id:x}'
                ),
                enabled = True,
            ),
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_market_place_entry_component(user_id, page_index, session_id, amount):
    """
    Tests whether ``build_market_place_entry_component`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        The invoking user's identifier.
    
    page_index : `int`
        Page index to redirect to.
    
    session_id : `int`
        The session's identifier.
    
    amount : `int`
        The allocated amount.
    
    Returns
    -------
    output : ``Component``
    """
    output = build_market_place_entry_component(user_id, page_index, session_id, amount)
    vampytest.assert_instance(output, Component)
    return output
