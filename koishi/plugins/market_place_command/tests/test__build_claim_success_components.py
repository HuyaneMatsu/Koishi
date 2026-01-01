import vampytest
from hata import Component, create_button, create_row, create_separator, create_text_display

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ...item_core import ITEM_ID_PEACH, get_item

from ..component_building import build_claim_success_components
from ..constants import EMOJI_CLOSE


def _iter_options():
    user_id = 202512260004
    item = get_item(ITEM_ID_PEACH)
    
    yield (
        user_id,
        True,
        item,
        56,
        1000,
        0,
        2,
        10,
        [
            create_text_display(
                f'You received the 56 {item.emoji} {item.name} ({item.weight * 56 / 1000:.03f} kg), '
                f'that you purchased for 1000 {EMOJI__HEART_CURRENCY}.'
            ),
            create_separator(),
            create_row(
                create_button(
                    'View inbox',
                    custom_id = f'market_place.inbox.view.{user_id:x}.{2:x}.{10:x}',
                ),
                create_button(
                    'Close',
                    EMOJI_CLOSE,
                    custom_id = f'market_place.close.{user_id:x}',
                ),
            ),
        ]
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_claim_success_components(
    user_id,
    receive_items,
    item,
    item_amount,
    reward_balance,
    fee,
    page_index,
    page_size,
):
    """
    Tests whether ``build_claim_success_components`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        The invoking user's identifier.
    
    receive_items : `bool`
        Whether the user received items.
    
    item : ``Item``
        Item to be sold.
    
    item_amount : `int`
        The amount of items to be sold.
    
    reward_balance : `int`
        The reward balance.
    
    fee : `int`
        Fee payed.
    
    page_index : `int`
        Page identifier to redirect back to.
    
    page_size : `int`
        Page size to redirect back to.
    
    Returns
    -------
    output : ``list<Component>``
    """
    output = build_claim_success_components(
        user_id,
        receive_items,
        item,
        item_amount,
        reward_balance,
        fee,
        page_index,
        page_size,
    )
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    return output
