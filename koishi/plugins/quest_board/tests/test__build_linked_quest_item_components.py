import vampytest

from hata import Component, create_button, create_row, create_separator, create_text_display

from ...item_core import ITEM_ID_PEACH, get_item_nullable

from ..component_building import build_linked_quest_item_components


def _iter_options():
    page_index = 1
    linked_quest_entry_id = 333
    item_id = ITEM_ID_PEACH
    item = get_item_nullable(item_id)
    assert item is not None
    
    user_id = 202509160004
    
    yield (
        user_id,
        page_index,
        linked_quest_entry_id,
        item_id,
        [
            create_text_display(
                f'**Item information: {item.emoji} {item.name}**\n'
                f'\n'
                f'{item.description}'
            ),
            create_separator(),
            create_row(
                create_button(
                    'View my quests',
                    custom_id = f'linked_quest.page.{user_id:x}.{page_index:x}',
                ),
                create_button(
                    'Back to the quest',
                    custom_id = f'linked_quest.details.{user_id:x}.{page_index:x}.{linked_quest_entry_id:x}',
                ),
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_linked_quest_item_components(user_id, page_index, linked_quest_entry_id, item_id):
    """
    Tests whether ``build_linked_quest_item_components`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        The invoking user's identifier.
    
    page_index : `int`
        The linked quests's current page's index.
    
    linked_quest_entry_id : `int`
        The currently selected quest's entry's identifier.
    
    item_id : `int`
        The item's identifier.
    
    Returns
    -------
    output : ``list<Component>``
    """
    output = build_linked_quest_item_components(user_id, page_index, linked_quest_entry_id, item_id)
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
