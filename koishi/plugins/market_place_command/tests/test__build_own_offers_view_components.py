from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from hata import (
    Component, Icon, IconType, User, create_button, create_row, create_section, create_separator, create_text_display,
    create_thumbnail_media
)

from ...item_core import ITEM_ID_PEACH, get_item
from ...market_place_core import MarketPlaceItem

from ..component_building import build_own_offers_view_components
from ..constants import EMOJI_CLOSE, EMOJI_LEFT, EMOJI_RIGHT


def _iter_options():
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    user_id = 202512230010
    user = User.precreate(
        user_id,
        avatar = Icon(IconType.static, 2),
        name = 'Nue',
    )
    
    item = get_item(ITEM_ID_PEACH)
    
    
    market_place_item_0 = MarketPlaceItem(
        item,
        5,
        user_id,
        0,
        DateTime(2016, 5, 15, tzinfo = TimeZone.utc),
        100,
    )
    
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
                    '# Nue\'s offers\n'
                    '\n'
                    'Page: 2'
                ),
                thumbnail = create_thumbnail_media(
                    f'https://cdn.discordapp.com/avatars/{user_id!s}/00000000000000000000000000000002.png'
                ),
            ),
            create_separator(),
            create_row(
                create_button(
                    'Page 1',
                    EMOJI_LEFT,
                    custom_id = f'market_place.own_offers.view.{user_id:x}.{0:x}.{10:x}',
                    enabled = True,
                ),
                create_button(
                    'Page 3',
                    EMOJI_RIGHT,
                    custom_id = 'market_place.own_offers.disabled.i',
                    enabled = False,
                ),
                create_button(
                    'Close',
                    EMOJI_CLOSE,
                    custom_id = f'market_place.close.{user_id:x}',
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
        ],
        True,
        [
            create_section(
                create_text_display(
                    '# Nue\'s offers\n'
                    '\n'
                    'Page: 1'
                ),
                thumbnail = create_thumbnail_media(
                    f'https://cdn.discordapp.com/avatars/{user_id!s}/00000000000000000000000000000002.png'
                ),
            ),
            create_separator(),
            create_text_display
            (
                f'5 {item.emoji} {item.name} ({item.weight * 5 / 1000:.3f} kg)\n'
                f'Time left: 1 day\n'
                f'No bids yet...'
            ),
            create_separator(),
            create_row(
                create_button(
                    'Page 0',
                    EMOJI_LEFT,
                    custom_id = 'market_place.own_offers.disabled.d',
                    enabled = False,
                ),
                create_button(
                    'Page 2',
                    EMOJI_RIGHT,
                    custom_id = f'market_place.own_offers.view.{user_id:x}.{1:x}.{10:x}',
                    enabled = True,
                ),
                create_button(
                    'Close',
                    EMOJI_CLOSE,
                    custom_id = f'market_place.close.{user_id:x}',
                ),
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_own_offers_view_components(
    user,
    guild_id,
    now,
    page_index,
    page_size,
    market_place_item_listing,
    has_more,
):
    """
    Tests whether ``build_own_offers_view_components`` works as intended.
    
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
    output = build_own_offers_view_components(
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
