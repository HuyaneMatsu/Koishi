import vampytest

from ...item_core import ITEM_ID_PEACH, get_item

from ..helpers import calculate_initial_sell_fee


def _iter_options():
    item = get_item(ITEM_ID_PEACH)
    
    yield (
        item,
        1,
        2,
        0,
        50,
    )
    
    yield (
        item,
        100,
        2,
        0,
        108,
    )
    
    yield (
        item,
        1,
        8,
        0,
        65,
    )
    
    yield (
        item,
        1,
        2,
        1000,
        93,
    )
    
    yield (
        item,
        100,
        8,
        100000,
        199,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__calculate_initial_sell_fee(item, item_amount, duration_days, starting_sell_price):
    """
    Tests whether ``calculate_initial_sell_fee`` works as intended.
    
    Parameters
    ----------
    item : ``Item``
        Item to get tax for.
    
    item_amount : `int`
        Item amount.
    
    duration_days : `int`
        The amount of days the item will be auctioned for.
    
    starting_sell_price : `int`
        Starting sell price.
    
    Returns
    -------
    output : `int`
    """
    output = calculate_initial_sell_fee(item, item_amount, duration_days, starting_sell_price)
    vampytest.assert_instance(output, int)
    return output
