from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from hata import Component, create_button, create_row, create_separator, create_text_display

from ...item_core import ITEM_ID_PEACH, get_item
from ...market_place_core import MarketPlaceItem

from ..component_building import build_bid_success_components
from ..constants import EMOJI_CLOSE


def _iter_options():
    user_id_0 = 202512300002
    
    item_0 = get_item(ITEM_ID_PEACH)
    
    entry_id_0 = 120
    
    market_place_item_0 = MarketPlaceItem(
        item_0,
        5,
        user_id_0,
        0,
        DateTime(2016, 5, 15, tzinfo = TimeZone.utc),
        100,
    )
    market_place_item_0.entry_id = entry_id_0
    
    
    yield (
        user_id_0,
        item_0.id,
        item_0.flags,
        1,
        10,
        True,
        [
            create_text_display(
                'You successfully placed your bid.\n'
                '\n'
                'Keep a keen eye on it, it is up to you to see whether others up you.\n'
                'In case you win the bid, make sure to claim it within 7 days!'
            ),
            create_separator(),
            create_row(
                create_button(
                    'Back to offers',
                    custom_id = f'market_place.purchase.view.{user_id_0:x}.{item_0.id:x}.{item_0.flags:x}.{1:x}.{10:x}'
                ),
                create_button(
                    'Close',
                    EMOJI_CLOSE,
                    custom_id = f'market_place.close.{user_id_0:x}',
                ),
            )
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_bid_success_components(
    user_id,
    item,
    required_flags,
    page_index,
    page_size,
    internal_call,
):
    """
    Tests whether ``build_bid_success_components`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        The invoking user's identifier.
    
    item : ``None | Item``
        Item the user is filtering for.
    
    required_flags : `int`
        Item flags the user is filtering for.
    
    now : `DateTime`
        The current time.
    
    page_index : `int`
        The page's index.
    
    page_size : `int`
        The page's size.
    
    internal_call : `bool`
        Whether the offer is shown from an internal source.
    
    market_place_item : ``MarketPlaceItem``
        The market place item to display.
    
    Returns
    -------
    output : ``list<Component>``
    """
    output = build_bid_success_components(
        user_id,
        item,
        required_flags,
        page_index,
        page_size,
        internal_call,
    )
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    return output
