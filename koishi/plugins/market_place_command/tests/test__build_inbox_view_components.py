from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from hata import (
    ButtonStyle, Component, Icon, IconType, User, create_button, create_row, create_section, create_separator,
    create_text_display, create_thumbnail_media
)

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ...item_core import ITEM_ID_PEACH, get_item
from ...market_place_core import (
    MARKET_PLACE_ITEM_FLAG_BUYER_RETRIEVED, MARKET_PLACE_ITEM_FLAG_SELLER_RETRIEVED, MarketPlaceItem
)
from ..component_building import build_inbox_view_components
from ..constants import EMOJI_CLOSE, EMOJI_LEFT, EMOJI_RIGHT


def _iter_options():
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    user_id_0 = 202512260000
    user_id_1 = 202512260001
    user = User.precreate(
        user_id_0,
        avatar = Icon(IconType.static, 2),
        name = 'Nue',
    )
    
    item = get_item(ITEM_ID_PEACH)
    
    market_place_item_0 = MarketPlaceItem(
        item,
        5,
        user_id_0,
        0,
        DateTime(2016, 5, 15, tzinfo = TimeZone.utc),
        100,
    )
    market_place_item_0.entry_id = 20
    
    market_place_item_1 = MarketPlaceItem(
        item,
        6,
        user_id_0,
        0,
        DateTime(2016, 5, 15, tzinfo = TimeZone.utc),
        100,
    )
    market_place_item_1.purchaser_user_id = user_id_1
    market_place_item_1.purchaser_balance_amount = 529
    market_place_item_1.entry_id = 21
    
    market_place_item_2 = MarketPlaceItem(
        item,
        7,
        user_id_1,
        0,
        DateTime(2016, 5, 15, tzinfo = TimeZone.utc),
        100,
    )
    market_place_item_2.purchaser_user_id = user_id_0
    market_place_item_2.purchaser_balance_amount = 530
    market_place_item_2.entry_id = 22
    
    
    market_place_item_3 = MarketPlaceItem(
        item,
        8,
        user_id_0,
        0,
        DateTime(2016, 5, 15, tzinfo = TimeZone.utc),
        100,
    )
    market_place_item_3.flags = MARKET_PLACE_ITEM_FLAG_SELLER_RETRIEVED
    market_place_item_3.purchaser_balance_amount = 531
    market_place_item_3.entry_id = 23
    
    market_place_item_4 = MarketPlaceItem(
        item,
        9,
        user_id_0,
        0,
        DateTime(2016, 5, 15, tzinfo = TimeZone.utc),
        100,
    )
    market_place_item_4.purchaser_user_id = user_id_1
    market_place_item_4.purchaser_balance_amount = 532
    market_place_item_4.flags = MARKET_PLACE_ITEM_FLAG_SELLER_RETRIEVED
    market_place_item_4.entry_id = 24
    
    market_place_item_5 = MarketPlaceItem(
        item,
        10,
        user_id_1,
        0,
        DateTime(2016, 5, 15, tzinfo = TimeZone.utc),
        100,
    )
    market_place_item_5.purchaser_user_id = user_id_0
    market_place_item_5.purchaser_balance_amount = 533
    market_place_item_5.flags = MARKET_PLACE_ITEM_FLAG_BUYER_RETRIEVED
    market_place_item_5.entry_id = 25
    
    yield (
        user,
        0,
        now,
        1,
        10,
        [],
        False,
        [
            create_section(
                create_text_display(
                    '# Nue\'s inbox\n'
                    '\n'
                    'Page: 2'
                ),
                thumbnail = create_thumbnail_media(
                    f'https://cdn.discordapp.com/avatars/{user_id_0!s}/00000000000000000000000000000002.png'
                ),
            ),
            create_separator(),
            create_row(
                create_button(
                    'Page 1',
                    EMOJI_LEFT,
                    custom_id = f'market_place.inbox.view.{user_id_0:x}.{0:x}.{10:x}',
                    enabled = True,
                ),
                create_button(
                    'Page 3',
                    EMOJI_RIGHT,
                    custom_id = 'market_place.inbox.disabled.i',
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
        user,
        0,
        now,
        0,
        10,
        [
            market_place_item_0,
            market_place_item_1,
            market_place_item_2,
            market_place_item_3,
            market_place_item_4,
            market_place_item_5,
        ],
        True,
        [
            create_section(
                create_text_display(
                    '# Nue\'s inbox\n'
                    '\n'
                    'Page: 1'
                ),
                thumbnail = create_thumbnail_media(
                    f'https://cdn.discordapp.com/avatars/{user_id_0!s}/00000000000000000000000000000002.png'
                ),
            ),
            create_separator(),
            create_section(
                create_text_display(
                    f'Your 5 {item.emoji} {item.name} ({item.weight * 5 / 1000:.03f} kg) offer\n'
                    f'Finalised: 1 day ago\n'
                    f'Was not sold D:'
                ),
                thumbnail = create_button(
                    'Claim',
                    custom_id = f'market_place.inbox.claim.{user_id_0:x}.{0:x}.{10:x}.{20:x}',
                    enabled = True,
                    style = ButtonStyle.green,
                ),
            ),
            create_section(
                create_text_display(
                    f'Your 6 {item.emoji} {item.name} ({item.weight * 6 / 1000:.03f} kg) offer\n'
                    f'Finalised: 1 day ago\n'
                    f'Was sold for 529 {EMOJI__HEART_CURRENCY} :D'
                ),
                thumbnail = create_button(
                    'Claim',
                    custom_id = f'market_place.inbox.claim.{user_id_0:x}.{0:x}.{10:x}.{21:x}',
                    enabled = True,
                    style = ButtonStyle.green,
                ),
            ),
            create_section(
                create_text_display(
                    f'You purchased 7 {item.emoji} {item.name} ({item.weight * 7 / 1000:.03f} kg)\n'
                    f'Finalised: 1 day ago\n'
                    f'For 530 {EMOJI__HEART_CURRENCY} :3'
                ),
                thumbnail = create_button(
                    'Claim',
                    custom_id = f'market_place.inbox.claim.{user_id_0:x}.{0:x}.{10:x}.{22:x}',
                    enabled = True,
                    style = ButtonStyle.green,
                ),
            ),
            create_section(
                create_text_display(
                    f'Your 8 {item.emoji} {item.name} ({item.weight * 8 / 1000:.03f} kg) offer\n'
                    f'Finalised: 1 day ago\n'
                    f'Was not sold D:'
                ),
                thumbnail = create_button(
                    'Claim',
                    custom_id = f'market_place.inbox.claim.{user_id_0:x}.{0:x}.{10:x}.{23:x}',
                    enabled = False,
                    style = ButtonStyle.gray,
                ),
            ),
            create_section(
                create_text_display(
                    f'Your 9 {item.emoji} {item.name} ({item.weight * 9 / 1000:.03f} kg) offer\n'
                    f'Finalised: 1 day ago\n'
                    f'Was sold for 532 {EMOJI__HEART_CURRENCY} :D'
                ),
                thumbnail = create_button(
                    'Claim',
                    custom_id = f'market_place.inbox.claim.{user_id_0:x}.{0:x}.{10:x}.{24:x}',
                    enabled = False,
                    style = ButtonStyle.gray,
                ),
            ),
            create_section(
                create_text_display(
                    f'You purchased 10 {item.emoji} {item.name} ({item.weight * 10 / 1000:.03f} kg)\n'
                    f'Finalised: 1 day ago\n'
                    f'For 533 {EMOJI__HEART_CURRENCY} :3'
                ),
                thumbnail = create_button(
                    'Claim',
                    custom_id = f'market_place.inbox.claim.{user_id_0:x}.{0:x}.{10:x}.{25:x}',
                    enabled = False,
                    style = ButtonStyle.gray,
                ),
            ),
            create_separator(),
            create_row(
                create_button(
                    'Page 0',
                    EMOJI_LEFT,
                    custom_id = 'market_place.inbox.disabled.d',
                    enabled = False,
                ),
                create_button(
                    'Page 2',
                    EMOJI_RIGHT,
                    custom_id = f'market_place.inbox.view.{user_id_0:x}.{1:x}.{10:x}',
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
def test__build_inbox_view_components(
    user,
    guild_id,
    now,
    page_index,
    page_size,
    market_place_item_listing,
    has_more,
):
    """
    Tests whether ``build_inbox_view_components`` works as intended.
    
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
    
    market_place_item_listing : ``list<MarketPlaceItem>````
        Market place items to display.
    
    has_more : `bool`
        Whether there are more items to show.
    
    Returns
    -------
    output : ``list<Component>``
    """
    output = build_inbox_view_components(
        user,
        guild_id,
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
