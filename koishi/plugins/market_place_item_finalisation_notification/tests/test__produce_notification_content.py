import vampytest

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ...item_core import ITEM_ID_PEACH, get_item_nullable

from ..component_building import produce_notification_content


def _iter_options():
    item_peach = get_item_nullable(ITEM_ID_PEACH)
    assert item_peach is not None
    
    user_id_0 = 202604280000
    user_id_1 = 202604280001
    
    yield (
        'Purchaser',
        user_id_0,
        user_id_1,
        user_id_0,
        item_peach.id,
        5,
        0,
        1000,
        'Hey mister',
        (
            f'Hey mister, you purchased {5} {item_peach.emoji} '
            f'{item_peach.name} ({item_peach.weight * 5 / 1000:.03f} kg) for 1000 {EMOJI__HEART_CURRENCY}.'
        ),
    )
    
    yield (
        'Seller',
        user_id_0,
        user_id_0,
        user_id_1,
        item_peach.id,
        5,
        0,
        1000,
        'Hey mister',
        (
            f'Hey mister, your offer {5} {item_peach.emoji} '
            f'{item_peach.name} ({item_peach.weight * 5 / 1000:.03f} kg) was sold for 1000 {EMOJI__HEART_CURRENCY}.'
        ),
    )
    
    yield (
        'Seller, not sold',
        user_id_0,
        user_id_0,
        0,
        item_peach.id,
        5,
        0,
        0,
        'Hey mister',
        (
            f'Hey mister, your offer {5} {item_peach.emoji} '
            f'{item_peach.name} ({item_peach.weight * 5 / 1000:.03f} kg) was not sold.'
        ),
    )
    
    yield (
        'Seller, not sold, with starting amount',
        user_id_0,
        user_id_0,
        0,
        item_peach.id,
        5,
        1000,
        0,
        'Hey mister',
        (
            f'Hey mister, your offer {5} {item_peach.emoji} '
            f'{item_peach.name} ({item_peach.weight * 5 / 1000:.03f} kg) starting at 1000 {EMOJI__HEART_CURRENCY} '
            f'was not sold.'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).named_first().returning_last())
def test__produce_notification_content(
    user_id,
    seller_user_id,
    purchaser_user_id,
    item_id,
    item_amount,
    seller_balance_amount,
    purchaser_balance_amount,
    notification_content_prefix,
):
    """
    Tests whether ``produce_notification_content`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        The point of view user's identifier.
    
    seller_user_id : `int`
        The seller user's identifier.
    
    purchaser_user_id : `int`
        The purchaser user's identifier.
    
    item_id : `int`
        The item's identifier.
    
    item_amount : ``int`
        The sold items' amount.
    
    seller_balance_amount : `int`
        The minimal amount of balance the seller requested.
    
    purchaser_balance_amount : `int`
        The amount of balance the purchaser bid with.
    
    notification_content_prefix : `str`
        Value to prefix notification content with.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_notification_content(
        user_id,
        seller_user_id,
        purchaser_user_id,
        item_id,
        item_amount,
        seller_balance_amount,
        purchaser_balance_amount,
        notification_content_prefix,
    )]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
