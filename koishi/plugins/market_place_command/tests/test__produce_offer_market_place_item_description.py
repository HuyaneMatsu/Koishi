from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ...item_core import ITEM_ID_PEACH, get_item_nullable
from ...market_place_core import MarketPlaceItem

from ..content_building import produce_offer_market_place_item_description


def _iter_options():
    item_peach = get_item_nullable(ITEM_ID_PEACH)
    assert item_peach is not None
    
    market_place_item_0 = MarketPlaceItem(
        item_peach,
        5,
        202512230003,
        0,
        DateTime(2016, 5, 15, tzinfo = TimeZone.utc),
        100,
    )
    market_place_item_0.purchaser_user_id = 202512230004
    market_place_item_0.purchaser_balance_amount = 200
    
    yield (
        market_place_item_0,
        DateTime(2016, 5, 14, tzinfo = TimeZone.utc),
        (
            f'5 {item_peach.emoji} {item_peach.name} ({5 * item_peach.weight / 1000:.2f} kg)\n'
            f'Time left: 1 day\n'
            f'Highest bid: {200!s} {EMOJI__HEART_CURRENCY}'
        ),
    )
    
    
    market_place_item_1 = MarketPlaceItem(
        item_peach,
        5,
        202512230005,
        50,
        DateTime(2016, 5, 15, tzinfo = TimeZone.utc),
        100,
    )
    
    yield (
        market_place_item_1,
        DateTime(2016, 5, 14, tzinfo = TimeZone.utc),
        (
            f'5 {item_peach.emoji} {item_peach.name} ({5 * item_peach.weight / 1000:.2f} kg)\n'
            f'Time left: 1 day\n'
            f'Starting price: {50!s} {EMOJI__HEART_CURRENCY}'
        ),
    )
    
    
    market_place_item_2 = MarketPlaceItem(
        item_peach,
        5,
        202512230006,
        0,
        DateTime(2016, 5, 15, tzinfo = TimeZone.utc),
        100,
    )
    
    yield (
        market_place_item_2,
        DateTime(2016, 5, 14, tzinfo = TimeZone.utc),
        (
            f'5 {item_peach.emoji} {item_peach.name} ({5 * item_peach.weight / 1000:.2f} kg)\n'
            f'Time left: 1 day\n'
            f'No bids yet...'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_offer_market_place_item_description(market_place_item, now):
    """
    Tests whether ``produce_offer_market_place_item_description`` works as intended.
    
    Parameters
    ----------
    market_place_item : ``MarketPlaceItem``
        The market place item to render.
    
    now : `DateTime`
        The current time.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_offer_market_place_item_description(market_place_item, now)]
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
