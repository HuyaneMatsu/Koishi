from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from hata import ButtonStyle, Component, create_button, create_row, create_separator, create_text_display

from ...item_core import ITEM_ID_PEACH, get_item
from ...market_place_core import MarketPlaceItem

from ..component_building_market_place import build_market_place_detailed_components


class DateTimeMock(DateTime):
    __slots__ = ()
    current_date_time = None
    
    @classmethod
    def set_current(cls, value):
        cls.current_date_time = value
    
    @classmethod
    def now(cls, time_zone):
        value = cls.current_date_time
        if value is None:
            value = DateTime.now(time_zone)
        return value


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
        market_place_item,
        None,
        0,
        DateTime(2016, 5, 15, tzinfo = TimeZone.utc),
        [
            create_text_display(
                '# `/market-place` allocating 200'
            ),
            create_text_display(
                f'Purchasing: 30 {item.emoji} {item.name} ({item.weight * 30 / 1000 :.03f} kg)\n'
                f'Time left: 1 day'
            ),
            create_separator(),
            create_row(
                create_button(
                    'Back to allocations',
                    custom_id = f'allocations.view.{user_id_1:x}.{page_index:x}'
                ),
                create_button(
                    'Get me there',
                    custom_id = f'market_place.offer.{user_id_1:x}.{entry_id:x}.{True:x}',
                ),
            ),
        ],
    )
    
    yield (
        user_id_0,
        page_index,
        entry_id,
        balance_amount,
        None,
        None,
        0,
        DateTime(2016, 5, 15, tzinfo = TimeZone.utc),
        [
            create_text_display(
                '# `/market-place` allocating 200'
            ),
            create_separator(),
            create_row(
                create_button(
                    'Back to allocations',
                    custom_id = f'allocations.view.{user_id_0:x}.{page_index:x}'
                ),
                create_button(
                    'Get me there',
                    custom_id =  'allocations.link.disabled',
                    enabled = False,
                    style = ButtonStyle.gray,
                ),
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_market_place_detailed_components(
    user_id, page_index, session_id, amount, session, extra, guild_id, current_date_time
):
    """
    Tests whether ``build_market_place_detailed_components`` works as intended.
    
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
    
    session : ``NoneType | MarketPlaceItem``
        The session.
    
    extra : `None`
        Additionally requested fields.
    
    guild_id : `int`
        The local guild's identifier.
    
    current_date_time : `DateTime`
        Current datetime to use for patching.
    
    Returns
    -------
    output : ``list<Component>``
    """
    DateTimeMock.set_current(current_date_time)
    mocked = vampytest.mock_globals(
        build_market_place_detailed_components,
        2,
        DateTime = DateTimeMock,
    )
    output = mocked(user_id, page_index, session_id, amount, session, extra, guild_id)
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    return output
