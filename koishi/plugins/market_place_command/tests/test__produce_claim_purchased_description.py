import vampytest

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ...item_core import ITEM_ID_PEACH, get_item_nullable

from ..content_building import produce_claim_purchased_description


def _iter_options():
    item_peach = get_item_nullable(ITEM_ID_PEACH)
    assert item_peach is not None
    
    yield (
        item_peach,
        5,
        1000,
        0,
        (
            f'You received the 5 {item_peach.emoji} {item_peach.name} ({5 * item_peach.weight / 1000:.02f} kg), '
            f'that you purchased for 1000 {EMOJI__HEART_CURRENCY}.'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_claim_purchased_description(
    item,
    item_amount,
    reward_balance,
    fee,
):
    """
    Tests whether ``produce_claim_purchased_description`` works as intended.
    
    Parameters
    ----------
    item : ``Item``
        Item to be sold.
    
    item_amount : `int`
        The amount of items to be sold.
    
    reward_balance : `int`
        The reward balance.
    
    fee : `int`
        Fee paid.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_claim_purchased_description(
        item,
        item_amount,
        reward_balance,
        fee,
    )]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
