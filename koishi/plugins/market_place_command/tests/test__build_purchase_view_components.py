from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from hata import (
    ButtonStyle, Component, create_button, create_row, create_section, create_separator, create_text_display
)

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ...item_core import ITEM_ID_GARLIC, ITEM_ID_PEACH, get_item
from ...market_place_core import MarketPlaceItem

from ..component_building import build_purchase_view_components
from ..constants import EMOJI_CLOSE, EMOJI_LEFT, EMOJI_RIGHT


def _iter_options():
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    user_id_0 = 202512260011
    user_id_1 = 202512260012
    
    item_0 = get_item(ITEM_ID_PEACH)
    item_1 = get_item(ITEM_ID_GARLIC)
    
    entry_id_0 = 120
    entry_id_1 = 121
    entry_id_2 = 122
    entry_id_3 = 123
    
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
        item_1,
        6,
        user_id_0,
        0,
        DateTime(2016, 5, 15, tzinfo = TimeZone.utc),
        100,
    )
    market_place_item_1.entry_id = entry_id_1
    market_place_item_1.purchaser_user_id = user_id_1
    market_place_item_1.purchaser_balance_amount = 1000
    
    market_place_item_2 = MarketPlaceItem(
        item_0,
        7,
        user_id_1,
        0,
        DateTime(2016, 5, 15, tzinfo = TimeZone.utc),
        100,
    )
    market_place_item_2.entry_id = entry_id_2
    
    market_place_item_3 = MarketPlaceItem(
        item_1,
        8,
        user_id_1,
        0,
        DateTime(2016, 5, 15, tzinfo = TimeZone.utc),
        100,
    )
    market_place_item_3.entry_id = entry_id_3
    market_place_item_3.purchaser_user_id = user_id_0
    market_place_item_3.purchaser_balance_amount = 1000
    
    yield (
        user_id_0,
        None,
        0,
        now,
        1,
        10,
        [],
        False,
        [
            create_text_display(
                f'# Market place\n'
                f'Page: 2'
            ),
            create_separator(),
            create_row(
                create_button(
                    'Page 1',
                    EMOJI_LEFT,
                    custom_id = f'market_place.purchase.view.{user_id_0:x}.{0:x}.{0:x}.{0:x}.{10:x}',
                    enabled = True,
                ),
                create_button(
                    'Page 3',
                    EMOJI_RIGHT,
                    custom_id = 'market_place.purchase.disabled.i',
                    enabled = False,
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
        user_id_0,
        None,
        item_0.flags,
        now,
        0,
        10,
        [
            market_place_item_0,
            market_place_item_1,
            market_place_item_2,
            market_place_item_3,
        ],
        True,
        [
            create_text_display(
                f'# Market place\n'
                f'Page: 1; filtered for category: edible'
            ),
            create_separator(),
            create_section(
                create_text_display(
                    f'5 {item_0.emoji} {item_0.name} ({item_0.weight * 5 / 1000:.03f} kg)\n'
                    f'Time left: 1 day\n'
                    f'No bids yet...'
                ),
                thumbnail = create_button(
                    'Details',
                    custom_id = (
                        f'market_place.purchase.details.{user_id_0:x}.{0:x}.{item_0.flags:x}.{0:x}.{10:x}.{entry_id_0:x}'
                    ),
                    style = ButtonStyle.gray,
                )
            ),
            create_section(
                create_text_display(
                    f'6 {item_1.emoji} {item_1.name} ({item_1.weight * 6 / 1000:.03f} kg)\n'
                    f'Time left: 1 day\n'
                    f'Highest bid: 1000 {EMOJI__HEART_CURRENCY}'
                ),
                thumbnail = create_button(
                    'Details',
                    custom_id = (
                        f'market_place.purchase.details.{user_id_0:x}.{0:x}.{item_0.flags:x}.{0:x}.{10:x}.{entry_id_1:x}'
                    ),
                    style = ButtonStyle.gray,
                )
            ),
            create_section(
                create_text_display(
                    f'7 {item_0.emoji} {item_0.name} ({item_0.weight * 7 / 1000:.03f} kg)\n'
                    f'Time left: 1 day\n'
                    f'No bids yet...'
                ),
                thumbnail = create_button(
                    'Details',
                    custom_id = (
                        f'market_place.purchase.details.{user_id_0:x}.{0:x}.{item_0.flags:x}.{0:x}.{10:x}.{entry_id_2:x}'
                    ),
                    style = ButtonStyle.blue,
                )
            ),
            create_section(
                create_text_display(
                    f'8 {item_1.emoji} {item_1.name} ({item_1.weight * 8 / 1000:.03f} kg)\n'
                    f'Time left: 1 day\n'
                    f'Highest bid: 1000 {EMOJI__HEART_CURRENCY}'
                ),
                thumbnail = create_button(
                    'Details',
                    custom_id = (
                        f'market_place.purchase.details.{user_id_0:x}.{0:x}.{item_0.flags:x}.{0:x}.{10:x}.{entry_id_3:x}'
                    ),
                    style = ButtonStyle.green,
                )
            ),
            create_separator(),
            create_row(
                create_button(
                    'Page 0',
                    EMOJI_LEFT,
                    custom_id = 'market_place.purchase.disabled.d',
                    enabled = False,
                ),
                create_button(
                    'Page 2',
                    EMOJI_RIGHT,
                    custom_id = f'market_place.purchase.view.{user_id_0:x}.{0:x}.{item_0.flags:x}.{1:x}.{10:x}',
                    enabled = True,
                ),
                create_button(
                    'Close',
                    EMOJI_CLOSE,
                    custom_id = f'market_place.close.{user_id_0:x}',
                ),
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_purchase_view_components(
    user_id,
    item,
    required_flags,
    now,
    page_index,
    page_size,
    market_place_item_listing,
    has_more,
):
    """
    Tests whether ``build_purchase_view_components`` works as intended.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The owner user.
    
    guild_id : `int`
        The local guild's identifier.
    
    now : `DateTime`
        The current time.
    
    page_index : `int`
        The page's index.
    
    page_size : `int`
        The page's size.
    
    market_place_item_listing : ``list<MarketPlaceItem>``
        Market place items to display.
    
    has_more : `bool`
        Whether there are more items to show.
    
    Returns
    -------
    output : ``list<Component>``
    """
    output = build_purchase_view_components(
        user_id,
        item,
        required_flags,
        now,
        page_index,
        page_size,
        market_place_item_listing,
        has_more,
    )
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    return output
