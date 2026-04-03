import vampytest

from hata import Component, create_button, create_row, create_separator, create_text_display

from ...item_core import ITEM_ID_PEACH, get_item_nullable
from ...quest_core import AMOUNT_TYPE_COUNT

from ..component_building import build_linked_quest_submit_success
from ..constants import (
    EMOJI_BACK, BACK_DIRECT_LOCATION_QUEST, BACK_DIRECT_LOCATION_SELECT_ITEM_NESTED,
    BACK_DIRECT_LOCATION_SELECT_ITEM_TOP, BACK_DIRECT_LOCATION_SELECT_REQUIREMENT,
)

def _iter_options():
    item_id = ITEM_ID_PEACH
    item = get_item_nullable(item_id)
    assert item is not None
    
    user_id = 202509160004
    
    yield (
        user_id,
        1,
        999,
        0,
        0,
        BACK_DIRECT_LOCATION_QUEST,
        [
            (item, AMOUNT_TYPE_COUNT, 50, 20, 12),
        ],
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
                    'Back',
                    EMOJI_BACK,
                    custom_id = f'linked_quest.details.{user_id:x}.{1:x}.{999:x}',
                ),
            ),
        ],
    )
    
    yield (
        user_id,
        1,
        999,
        7,
        0,
        BACK_DIRECT_LOCATION_SELECT_REQUIREMENT,
        [
            (item, AMOUNT_TYPE_COUNT, 50, 20, 12),
        ],
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
                    'Back',
                    EMOJI_BACK,
                    custom_id = f'linked_quest.submit_select_requirement.{user_id:x}.{1:x}.{999:x}.{1:x}',
                ),
            ),
        ],
    )
    
    yield (
        user_id,
        1,
        999,
        0,
        2,
        BACK_DIRECT_LOCATION_SELECT_ITEM_TOP,
        [
            (item, AMOUNT_TYPE_COUNT, 50, 20, 12),
        ],
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
                    'Back',
                    EMOJI_BACK,
                    custom_id = f'linked_quest.submit_select_item_top.{user_id:x}.{1:x}.{999:x}.{2:x}',
                ),
            ),
        ],
    )
    
    yield (
        user_id,
        1,
        999,
        3,
        2,
        BACK_DIRECT_LOCATION_SELECT_ITEM_NESTED,
        [
            (item, AMOUNT_TYPE_COUNT, 50, 20, 12),
        ],
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
                    'Back',
                    EMOJI_BACK,
                    custom_id = f'linked_quest.submit_select_item_nested.{user_id:x}.{1:x}.{999:x}.{3:x}.{2:x}',
                ),
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_linked_quest_submit_success(
    user_id,
    page_index,
    linked_quest_entry_id,
    requirement_index,
    item_page_index,
    back_direct_location,
    submissions_normalised,
):
    """
    Tests whether ``build_linked_quest_submit_success`` works as intended.
    
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
    
    submissions_normalised : ``list<(Item, int, int, int, int)>``
        The submitted amounts normalised.
    
    Returns
    -------
    output : ``list<Component>``
    """
    output = build_linked_quest_submit_success(
        user_id,
        page_index,
        linked_quest_entry_id,
        requirement_index,
        item_page_index,
        back_direct_location,
        submissions_normalised,
    )
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
