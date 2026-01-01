import vampytest

from hata import Component, create_button, create_row, create_separator, create_text_display

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ...item_core import ITEM_ID_PEACH, get_item

from ..component_building import build_sell_success_components
from ..constants import EMOJI_CLOSE


def _iter_options():
    item = get_item(ITEM_ID_PEACH)
    user_id = 202512230007
    
    yield (
        user_id,
        item,
        100,
        4,
        1000,
        30,
        [
            create_text_display(
                f'You put 100 {item.emoji} {item.name} ({item.weight * 100 / 1000:.03f} kg) '
                f'on the market for 4 days, starting at 1000 {EMOJI__HEART_CURRENCY}.\n'
                f'You payed 30 {EMOJI__HEART_CURRENCY} initial fee.'
            ),
            create_separator(),
            create_row(
                create_button(
                    'View own offers',
                    custom_id = f'market_place.own_offers.view.{user_id:x}.{0:x}.{10:x}',
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
def test__build_sell_success_components(
    user_id,
    item,
    item_amount,
    duration_days,
    starting_sell_price,
    initial_sell_fee,
):
    """
    Tests whether ``build_sell_success_components`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        The invoking user's identifier.
    
    item : ``Item``
        Item to be sold.
    
    item_amount : `int`
        The amount of items to be sold.
    
    duration_days : `int` = `8`
        The amount of days the item will be auctioned for.
    
    starting_sell_price : `int`
        Starting sell price.
    
    initial_sell_fee : `int`
        The amount of balance the user has to pay to put the item(s) on the market place.
    
    Returns
    -------
    output : ```list<Component>``
    """
    output = build_sell_success_components(
        user_id,
        item,
        item_amount,
        duration_days,
        starting_sell_price,
        initial_sell_fee,
    )
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    return output
