import vampytest

from hata import InteractionForm, create_text_display

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ...item_core import ITEM_ID_PEACH, get_item

from ..component_building import build_sell_confirmation_form


def _iter_options():
    item = get_item(ITEM_ID_PEACH)
    yield (
        item,
        100,
        4,
        1000,
        30,
        InteractionForm(
            'Sell confirmation',
            [
                create_text_display(
                    f'Are you sure to put 100 {item.emoji} {item.name} ({item.weight * 100 / 1000:.03f} kg) '
                    f'on the market for 4 days, starting at 1000 {EMOJI__HEART_CURRENCY}?\n'
                    f'You will have to pay 30 {EMOJI__HEART_CURRENCY} initial fee.'
                ),
            ],
            f'market_place.sell.{item.id:x}.{100:x}.{4:x}.{1000:x}'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_sell_confirmation_form(
    item,
    item_amount,
    duration_days,
    starting_sell_price,
    initial_sell_fee,
):
    """
    Tests whether ``build_sell_confirmation_form`` works as intended.
    
    Parameters
    ----------
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
    output : ``InteractionForm``
    """
    output = build_sell_confirmation_form(
        item,
        item_amount,
        duration_days,
        starting_sell_price,
        initial_sell_fee,
    )
    vampytest.assert_instance(output, InteractionForm)
    return output
