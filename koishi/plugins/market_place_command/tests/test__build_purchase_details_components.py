from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from hata import ButtonStyle, Component, create_button, create_row, create_separator, create_text_display

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ...item_core import ITEM_ID_PEACH, get_item
from ...market_place_core import MarketPlaceItem

from ..component_building import build_purchase_details_components
from ..constants import EMOJI_CLOSE


def _iter_options():
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    user_id_0 = 202512290000
    user_id_1 = 202512290001
    
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
        None,
        item_0.flags,
        now,
        1,
        10,
        True,
        market_place_item_0,
        [
            create_text_display(
                f'### 5 {item_0.emoji} {item_0.name} ({item_0.weight * 5 / 1000:.03f} kg)\n'
                f'Time left: 1 day\n'
                f'No bids yet...'
            ),
            create_separator(),
            create_text_display(
                f'One of the most popular temperate fruits. '
                f'Has yellow flesh and beautiful yellow to orange skin with a cute red blush towards the sun.\n'
                f'\n'
                f'Can be found at the gardens of **Hakugyokurou mansion**. '
                f'Not sure if they were planted intentionally, '
                f'or someone just mistake their pink blossom to cherry trees\'.\n'
                f'\n'
                f'### Trading information\n'
                f'Weight: 0.216 kg\n'
                f'Value: 40 {EMOJI__HEART_CURRENCY}\n'
                f'### Categories\n'
                f'- Edible'
            ),
            create_separator(),
            create_row(
                create_button(
                    'Back to offers',
                    custom_id = f'market_place.purchase.view.{user_id_0:x}.{0:x}.{item_0.flags:x}.{1:x}.{10:x}'
                ),
                create_button(
                    'Bid',
                    custom_id = 'market_place.bid.disabled',
                    enabled = False,
                    style = ButtonStyle.gray,
                ),
                create_button(
                    'Close',
                    EMOJI_CLOSE,
                    custom_id = f'market_place.close.{user_id_0:x}',
                ),
            ),
        ],
    )
    
    yield (
        user_id_1,
        None,
        0,
        now,
        0,
        10,
        False,
        market_place_item_0,
        [
            create_text_display(
                f'### 5 {item_0.emoji} {item_0.name} ({item_0.weight * 5 / 1000:.03f} kg)\n'
                f'Time left: 1 day\n'
                f'No bids yet...'
            ),
            create_separator(),
            create_text_display(
                f'One of the most popular temperate fruits. '
                f'Has yellow flesh and beautiful yellow to orange skin with a cute red blush towards the sun.\n'
                f'\n'
                f'Can be found at the gardens of **Hakugyokurou mansion**. '
                f'Not sure if they were planted intentionally, '
                f'or someone just mistake their pink blossom to cherry trees\'.\n'
                f'\n'
                f'### Trading information\n'
                f'Weight: 0.216 kg\n'
                f'Value: 40 {EMOJI__HEART_CURRENCY}\n'
                f'### Categories\n'
                f'- Edible'
            ),
            create_separator(),
            create_row(
                create_button(
                    'View other offers',
                    custom_id = f'market_place.purchase.view.{user_id_1:x}.{item_0.id:x}.{0:x}.{0:x}.{10:x}'
                ),
                create_button(
                    'Bid',
                    custom_id = (
                        f'market_place.bid.{user_id_1:x}.{item_0.id:x}.{0:x}.{0:x}.{10:x}.{False:x}.{entry_id_0:x}'
                    ),
                    enabled = True,
                    style = ButtonStyle.blue,
                ),
                create_button(
                    'Close',
                    EMOJI_CLOSE,
                    custom_id = f'market_place.close.{user_id_1:x}',
                ),
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_purchase_details_components(
    user_id,
    item,
    required_flags,
    now,
    page_index,
    page_size,
    internal_call,
    market_place_item,
):
    """
    Tests whether ``build_purchase_details_components`` works as intended.
    
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
    output = build_purchase_details_components(
        user_id,
        item,
        required_flags,
        now,
        page_index,
        page_size,
        internal_call,
        market_place_item,
    )
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    return output
