import vampytest

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ...item_core import ITEM_ID_PEACH, get_item_nullable

from ..content_building import produce_sell_success_description


def _iter_options():
    item_peach = get_item_nullable(ITEM_ID_PEACH)
    assert item_peach is not None
    
    yield (
        item_peach,
        100,
        4,
        1000,
        30,
        (
            f'You put 100 {item_peach.emoji} {item_peach.name} ({100 * item_peach.weight / 1000:.01f} kg) '
            f'on the market for 4 days, starting at 1000 {EMOJI__HEART_CURRENCY}.\n'
            f'You paid 30 {EMOJI__HEART_CURRENCY} initial fee.'
        )
    )
    
    yield (
        item_peach,
        100,
        4,
        0,
        30,
        (
            f'You put 100 {item_peach.emoji} {item_peach.name} ({100 * item_peach.weight / 1000:.01f} kg) '
            f'on the market for 4 days.\n'
            f'You paid 30 {EMOJI__HEART_CURRENCY} initial fee.'
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_sell_success_description(
    item,
    item_amount,
    duration_days,
    starting_sell_price,
    initial_sell_fee,
):
    """
    Tests whether ``produce_sell_success_description`` works as intended.
    
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
    output : `str`
    """
    output = [*produce_sell_success_description(
        item,
        item_amount,
        duration_days,
        starting_sell_price,
        initial_sell_fee,
    )]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
