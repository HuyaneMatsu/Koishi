from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from hata import Component, InteractionForm, create_label, create_text_display, create_text_input

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ...item_core import ITEM_ID_PEACH, get_item
from ...market_place_core import MarketPlaceItem

from ..component_building import build_bid_form


def _iter_options():
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    user_id_0 = 202512300000
    user_id_1 = 202512310001
    
    item_0 = get_item(ITEM_ID_PEACH)
    
    entry_id_0 = 120
    entry_id_1 = 121
    
    market_place_item_0 = MarketPlaceItem(
        item_0,
        5,
        user_id_0,
        0,
        DateTime(2016, 5, 15, tzinfo = TimeZone.utc),
        100,
    )
    market_place_item_0.entry_id = entry_id_0
    
    market_place_item_1 = MarketPlaceItem(
        item_0,
        5,
        user_id_0,
        0,
        DateTime(2016, 5, 15, tzinfo = TimeZone.utc),
        100,
    )
    market_place_item_1.entry_id = entry_id_1
    market_place_item_1.purchaser_user_id = user_id_1
    market_place_item_1.purchaser_balance_amount = 200
    
    
    yield (
        user_id_0,
        0,
        item_0.flags,
        now,
        1,
        10,
        True,
        market_place_item_0,
        InteractionForm(
            'Specify your bid amount',
            [
                create_text_display(
                    f'### 5 {item_0.emoji} {item_0.name} ({item_0.weight * 5 / 1000:.03f} kg)\n'
                    f'Time left: 1 day\n'
                    f'No bids yet...'
                ),
                create_label(
                    'Bid amount',
                    'Lowest allowed bid auto-filled, modify or just confirm.',
                    create_text_input(
                        custom_id = 'bid_balance_amount',
                        value = '10',
                    ),
                ),
            ],
            f'market_place.bid.{user_id_0:x}.{0:x}.{item_0.flags:x}.{1:x}.{10:x}.{True:x}.{entry_id_0:x}',
        ),
    )
    
    
    yield (
        user_id_1,
        item_0.id,
        0,
        now,
        0,
        10,
        False,
        market_place_item_1,
        InteractionForm(
            'Specify your bid amount',
            [
                create_text_display(
                    f'### 5 {item_0.emoji} {item_0.name} ({item_0.weight * 5 / 1000:.03f} kg)\n'
                    f'Time left: 1 day\n'
                    f'Highest bid: 200 {EMOJI__HEART_CURRENCY}'
                ),
                create_label(
                    'Bid amount',
                    'You are currently the highest bidder.',
                    create_text_input(
                        custom_id = 'bid_balance_amount',
                        value = '200',
                    ),
                ),
            ],
            f'market_place.bid.{user_id_1:x}.{item_0.id:x}.{0:x}.{0:x}.{10:x}.{False:x}.{entry_id_1:x}',
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_bid_form(
    user_id,
    item_id,
    required_flags,
    now,
    page_index,
    page_size,
    internal_call,
    market_place_item,
):
    """
    Tests whether ``build_bid_form`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        The invoking user's identifier.
    
    item_id : `int`
        Item identifier to back-direct to.
    
    required_flags : `int`
        Item flags to back-direct to.
    
    now : `DateTime`
        The current time.
    
    page_index : `int`
        The page's index to back-direct to.
    
    page_size : `int`
        The page's size to back-direct to.
    
    internal_call : `bool`
        Whether the offer is shown from an internal source to back-direct to.
    
    market_place_item : ``MarketPlaceItem``
        The market place item to bid for.
    
    Returns
    -------
    output : ``InteractionForm``
    """
    output = build_bid_form(
        user_id,
        item_id,
        required_flags,
        now,
        page_index,
        page_size,
        internal_call,
        market_place_item,
    )
    
    vampytest.assert_instance(output, InteractionForm)
    return output
