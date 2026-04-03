import vampytest

from hata import Component, create_button, create_row, create_separator, create_text_display

from ...item_core import ITEM_GROUP_ID_KNIFE, get_item_group_nullable

from ..component_building import build_linked_quest_item_group_components
from ..constants import (
    EMOJI_BACK, BACK_DIRECT_LOCATION_QUEST, BACK_DIRECT_LOCATION_SELECT_ITEM_NESTED,
    BACK_DIRECT_LOCATION_SELECT_ITEM_TOP, BACK_DIRECT_LOCATION_SELECT_REQUIREMENT
)


def _iter_options():
    page_index = 1
    linked_quest_entry_id = 333
    item_group_id = ITEM_GROUP_ID_KNIFE
    item_group = get_item_group_nullable(item_group_id)
    assert item_group is not None
    
    user_id = 202603280000
    
    yield (
        user_id,
        page_index,
        linked_quest_entry_id,
        0,
        0,
        BACK_DIRECT_LOCATION_QUEST,
        item_group_id,
        [
            create_text_display(
                f'**Item group information: {item_group.emoji} {item_group.name}**\n'
                f'\n'
                f'{item_group.description}\n'
                f'\n'
                f'**Items:**\n'
                f'- Aching affection\'s Heart-piercer\n'
                f'- Kitchen knife\n'
                f'- Poking knife'
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
        BACK_DIRECT_LOCATION_SELECT_REQUIREMENT,
        item_group_id,
        [
            create_text_display(
                f'**Item group information: {item_group.emoji} {item_group.name}**\n'
                f'\n'
                f'{item_group.description}\n'
                f'\n'
                f'**Items:**\n'
                f'- Aching affection\'s Heart-piercer\n'
                f'- Kitchen knife\n'
                f'- Poking knife'
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
        BACK_DIRECT_LOCATION_SELECT_ITEM_TOP,
        item_group_id,
        [
            create_text_display(
                f'**Item group information: {item_group.emoji} {item_group.name}**\n'
                f'\n'
                f'{item_group.description}\n'
                f'\n'
                f'**Items:**\n'
                f'- Aching affection\'s Heart-piercer\n'
                f'- Kitchen knife\n'
                f'- Poking knife'
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
        BACK_DIRECT_LOCATION_SELECT_ITEM_NESTED,
        item_group_id,
        [
            create_text_display(
                f'**Item group information: {item_group.emoji} {item_group.name}**\n'
                f'\n'
                f'{item_group.description}\n'
                f'\n'
                f'**Items:**\n'
                f'- Aching affection\'s Heart-piercer\n'
                f'- Kitchen knife\n'
                f'- Poking knife'
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
def test__build_linked_quest_item_group_components(
    user_id,
    page_index,
    linked_quest_entry_id,
    requirement_index,
    item_group_page_index,
    back_direct_location,
    item_group_id,
):
    """
    Tests whether ``build_linked_quest_item_group_components`` works as intended.
    
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
    
    item_group_page_index : `int`
        The item_groups' page's index to back-direct to.
    
    back_direct_location : `int`
        Where to back-direct to.
    
    item_group_id : `int`
        The item group's identifier.
    
    Returns
    -------
    output : ``list<Component>``
    """
    output = build_linked_quest_item_group_components(
        user_id,
        page_index,
        linked_quest_entry_id,
        requirement_index,
        item_group_page_index,
        back_direct_location,
        item_group_id,
    )
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
