import vampytest

from hata import Component, create_button, create_row, create_separator, create_text_display

from ...item_core import ITEM_ID_PEACH, get_item_nullable

from ..component_building import build_linked_quest_item_components
from ..constants import (
    EMOJI_BACK, LINKED_QUEST_BACK_DIRECT_LOCATION_QUEST, LINKED_QUEST_BACK_DIRECT_LOCATION_SELECT_ITEM_NESTED,
    LINKED_QUEST_BACK_DIRECT_LOCATION_SELECT_ITEM_TOP, LINKED_QUEST_BACK_DIRECT_LOCATION_SELECT_REQUIREMENT
)


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
        0,
        0,
        LINKED_QUEST_BACK_DIRECT_LOCATION_QUEST,
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
                    'Back',
                    EMOJI_BACK,
                    custom_id = f'linked_quest.details.{user_id:x}.{page_index:x}.{linked_quest_entry_id:x}',
                ),
            ),
        ],
    )
    
    yield (
        user_id,
        page_index,
        linked_quest_entry_id,
        7,
        0,
        LINKED_QUEST_BACK_DIRECT_LOCATION_SELECT_REQUIREMENT,
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
                    'Back',
                    EMOJI_BACK,
                    custom_id = (
                        f'linked_quest.submit_select_requirement.{user_id:x}.{page_index:x}.'
                        f'{linked_quest_entry_id:x}.{1:x}'
                    ),
                ),
            ),
        ],
    )
    
    yield (
        user_id,
        page_index,
        linked_quest_entry_id,
        0,
        5,
        LINKED_QUEST_BACK_DIRECT_LOCATION_SELECT_ITEM_TOP,
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
                    'Back',
                    EMOJI_BACK,
                    custom_id = (
                        f'linked_quest.submit_select_item_top.{user_id:x}.{page_index:x}.'
                        f'{linked_quest_entry_id:x}.{5:x}'
                    ),
                ),
            ),
        ],
    )
    
    yield (
        user_id,
        page_index,
        linked_quest_entry_id,
        3,
        5,
        LINKED_QUEST_BACK_DIRECT_LOCATION_SELECT_ITEM_NESTED,
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
                    'Back',
                    EMOJI_BACK,
                    custom_id = (
                        f'linked_quest.submit_select_item_nested.{user_id:x}.{page_index:x}.'
                        f'{linked_quest_entry_id:x}.{3:x}.{5:x}'
                    ),
                ),
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_linked_quest_item_components(
    user_id,
    page_index,
    linked_quest_entry_id,
    requirement_index,
    item_page_index,
    back_direct_location,
    item_id,
):
    """
    Tests whether ``build_linked_quest_item_components`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        The invoking user's identifier.
    
    page_index : `int`
        The linked quests' current page's index.
    
    linked_quest_entry_id : `int`
        The currently selected quest's entry's identifier.
    
    requirement_index : `int`
        The submitted requirement's index to back-direct to.
    
    item_page_index : `int`
        The items' page's index to back-direct to.
    
    back_direct_location : `int`
        Where to back-direct to.
    
    item_id : `int`
        The item's identifier.
    
    Returns
    -------
    output : ``list<Component>``
    """
    output = build_linked_quest_item_components(
        user_id,
        page_index,
        linked_quest_entry_id,
        requirement_index,
        item_page_index,
        back_direct_location,
        item_id,
    )
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
