import vampytest
from hata import Component, create_button, create_row, create_text_display

from config import FLANDRE_ID

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ...item_core import ITEM_ID_PEACH, get_item_nullable

from ..component_building import build_notification_components


def _iter_options():
    item_peach = get_item_nullable(ITEM_ID_PEACH)
    assert item_peach is not None
    
    user_id_0 = 202605090000
    user_id_1 = 202605090001
    
    yield (
        0,
        user_id_0,
        user_id_1,
        user_id_0,
        item_peach.id,
        5,
        0,
        1000,
        [
            create_text_display(
                f'Hey mister, you purchased {5} {item_peach.emoji} '
                f'{item_peach.name} ({item_peach.weight * 5 / 1000:.03f} kg) for 1000 {EMOJI__HEART_CURRENCY}.'
            ),
            create_row(
                create_button(
                    'I don\'t want notifs, nya!!',
                    custom_id = 'user_settings.market_place_item_finalisation.disable',
                ),
            ),
        ],
    )
    
    yield (
        FLANDRE_ID,
        user_id_0,
        user_id_1,
        user_id_0,
        item_peach.id,
        5,
        0,
        1000,
        [
            create_text_display(
                f'Nee-sama, you purchased {5} {item_peach.emoji} '
                f'{item_peach.name} ({item_peach.weight * 5 / 1000:.03f} kg) for 1000 {EMOJI__HEART_CURRENCY}.'
            ),
            create_row(
                create_button(
                    'Go back to your basement!!',
                    custom_id = 'user_settings.market_place_item_finalisation.disable',
                ),
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_notification_components(
    preferred_client_id,
    user_id,
    seller_user_id,
    purchaser_user_id,
    item_id,
    item_amount,
    seller_balance_amount,
    purchaser_balance_amount,
):
    """
    Tests whether ``build_notification_components`` works as intended.
    
    Parameters
    ----------
    preferred_client_id : `int`
        The notifier client's identifier to select style for.
    
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
    
    Returns
    -------
    output : ``list<Component>``
    """
    output = build_notification_components(
        preferred_client_id,
        user_id,
        seller_user_id,
        purchaser_user_id,
        item_id,
        item_amount,
        seller_balance_amount,
        purchaser_balance_amount,
    )
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
