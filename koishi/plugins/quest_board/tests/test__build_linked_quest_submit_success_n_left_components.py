import vampytest

from hata import Component, create_text_display

from ...item_core import ITEM_ID_PEACH, get_item_nullable
from ...quest_core import AMOUNT_TYPE_COUNT

from ..component_building import build_linked_quest_submit_success_n_left_components


def _iter_options():
    item_id = ITEM_ID_PEACH
    item = get_item_nullable(item_id)
    assert item is not None
    
    yield (
        item,
        AMOUNT_TYPE_COUNT,
        20,
        50,
        12,
        [
            create_text_display(
                f'You have submitted **12** {item.name} {item.emoji}.\n'
                f'**18** more to submit.'
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_linked_quest_submit_success_n_left_components(
    item, amount_type, amount_submitted, amount_required, amount_used,
):
    """
    Tests whether ``build_linked_quest_submit_success_n_left_components`` works as intended.
    
    Parameters
    ----------
    item : ``None | Item``
        The submitted item.
    
    amount_type : `int`
        The amount's type.
    
    amount_submitted : `int`
        Already submitted amount.
    
    amount_required : `int`
        The amount of required items.
    
    amount_used : `int`
        The used up amount.
    
    Returns
    -------
    output : ``list<Component>``
    """
    output = build_linked_quest_submit_success_n_left_components(
        item, amount_type, amount_submitted, amount_required, amount_used,
    )
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
