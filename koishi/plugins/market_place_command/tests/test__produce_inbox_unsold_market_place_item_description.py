from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ...item_core import ITEM_ID_PEACH, get_item
from ...market_place_core import MarketPlaceItem

from ..content_building import produce_inbox_unsold_market_place_item_description


def _iter_options():
    item = get_item(ITEM_ID_PEACH)
    user_id = 202512250000
    
    market_place_item_0 = MarketPlaceItem(
        item,
        100,
        user_id,
        500,
        DateTime(2016, 5, 13, tzinfo = TimeZone.utc),
        100,
    )
    
    yield (
        market_place_item_0,
        DateTime(2016, 5, 14, tzinfo = TimeZone.utc),
        (
            f'Your 100 {item.emoji} {item.name} ({item.weight * 100 / 1000:.03f} kg) offer\n'
            f'Finalised: 1 day ago\n'
            f'Starting at 500 {EMOJI__HEART_CURRENCY} was not sold D:'
        )
    )
    
    market_place_item_1 = MarketPlaceItem(
        item,
        100,
        user_id,
        0,
        DateTime(2016, 5, 13, tzinfo = TimeZone.utc),
        100,
    )
    
    yield (
        market_place_item_1,
        DateTime(2016, 5, 14, tzinfo = TimeZone.utc),
        (
            f'Your 100 {item.emoji} {item.name} ({item.weight * 100 / 1000:.03f} kg) offer\n'
            f'Finalised: 1 day ago\n'
            f'Was not sold D:'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_inbox_unsold_market_place_item_description(market_place_item, now):
    """
    Tests whether ``produce_inbox_unsold_market_place_item_description`` works as intended.
    
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
    output = [*produce_inbox_unsold_market_place_item_description(market_place_item, now)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
