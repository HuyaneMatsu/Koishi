import vampytest

from hata import Component, create_button, create_row, create_separator, create_text_display

from ...item_core import ITEM_ID_PEACH, get_item_nullable
from ...quest_core import AMOUNT_TYPE_COUNT

from ..component_building import build_linked_quest_submit_success_n_left_components


def _iter_options():
    item_id = ITEM_ID_PEACH
    item = get_item_nullable(item_id)
    assert item is not None
    
    user_id = 202509160004
    
    yield (
        user_id,
        1,
        999,
        item,
        AMOUNT_TYPE_COUNT,
        20,
        50,
        12,
        [
            create_text_display(
                f'You have submitted **12** {item.emoji} {item.name}.\n'
                f'**18** more to submit.'
            ),
            create_separator(),
            create_row(
                create_button(
                    'View my quests',
                    custom_id = f'linked_quest.page.{user_id:x}.{1:x}',
                ),
                create_button(
                    'Back to the quest',
                    custom_id = f'linked_quest.details.{user_id:x}.{1:x}.{999:x}',
                ),
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_linked_quest_submit_success_n_left_components(
    user_id, page_index, linked_quest_entry_id, item, amount_type, amount_submitted, amount_required, amount_used,
):
    """
    Tests whether ``build_linked_quest_submit_success_n_left_components`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        The invoking user's identifier.
    
    page_index : `int`
        The linked quests' current page's index.
    
    linked_quest_entry_id : `int`
        The currently selected quest's entry's identifier.
    
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
        user_id, page_index, linked_quest_entry_id, item, amount_type, amount_submitted, amount_required, amount_used,
    )
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
