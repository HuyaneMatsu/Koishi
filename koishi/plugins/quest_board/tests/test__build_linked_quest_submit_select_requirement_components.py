import vampytest
from hata import ButtonStyle, Component, create_button, create_row, create_separator, create_text_display

from ...inventory_core import Inventory
from ...item_core import (
    ITEM_FLAG_EDIBLE, ITEM_GROUP_ID_KNIFE, ITEM_ID_PEACH, get_item_group_nullable, get_item_nullable
)
from ...quest_core import (
    AMOUNT_TYPE_COUNT, LinkedQuest, QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY, QuestRequirementSerialisableBase,
    QuestRequirementSerialisableItemCategory, QuestRequirementSerialisableItemExact,
    QuestRequirementSerialisableItemGroup
)

from ..component_building import build_linked_quest_submit_select_requirement_components
from ..constants import EMOJI_BACK, EMOJI_PAGE_NEXT, EMOJI_PAGE_PREVIOUS, EMOJI_REFRESH


def _iter_options():
    item_peach = get_item_nullable(ITEM_ID_PEACH)
    assert item_peach is not None
    
    item_group_knife = get_item_group_nullable(ITEM_GROUP_ID_KNIFE)
    assert item_group_knife is not None
    
    user_id = 202603040000
    guild_id = 202603040001
    batch_id = 202603040002
    
    
    linked_quest_0 = LinkedQuest(
        user_id,
        guild_id,
        batch_id,
        QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
        None,
        None,
    )
    
    linked_quest_entry_id_0 = 56
    linked_quest_0.entry_id = linked_quest_entry_id_0
    
    inventory_0 = Inventory(user_id)
    
    yield (
        linked_quest_0,
        inventory_0,
        10,
        0,
        [
            create_text_display('### Select requirement to submit for'),
            create_separator(),
            create_row(
                create_button(
                    'Page 0',
                    EMOJI_PAGE_PREVIOUS,
                    custom_id = 'linked_quest.submit_select_requirement.page_decrement_disabled',
                    enabled = False,
                ),
                create_button(
                    'Page 2',
                    EMOJI_PAGE_NEXT,
                    custom_id = 'linked_quest.submit_select_requirement.page_increment_disabled',
                    enabled = False,
                ),
                create_button(
                    'Refresh',
                    EMOJI_REFRESH,
                    custom_id = (
                        f'linked_quest.submit_select_requirement.{user_id:x}.{10:x}.{linked_quest_entry_id_0:x}.'
                        f'{0:x}'
                    ),
                ),
                create_button(
                    'Back',
                    EMOJI_BACK,
                    custom_id = f'linked_quest.details.{user_id:x}.{10:x}.{linked_quest_entry_id_0:x}',
                ),
            ),
        ],
    )
    
    linked_quest_1 = LinkedQuest(
        user_id,
        guild_id,
        batch_id,
        QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
        [
            QuestRequirementSerialisableItemExact(ITEM_ID_PEACH, AMOUNT_TYPE_COUNT, 30, 0),
            QuestRequirementSerialisableItemExact(ITEM_ID_PEACH, AMOUNT_TYPE_COUNT, 30, 1),
            QuestRequirementSerialisableItemExact(ITEM_ID_PEACH, AMOUNT_TYPE_COUNT, 30, 2),
            QuestRequirementSerialisableItemExact(ITEM_ID_PEACH, AMOUNT_TYPE_COUNT, 30, 3),
            QuestRequirementSerialisableItemExact(ITEM_ID_PEACH, AMOUNT_TYPE_COUNT, 30, 4),
            QuestRequirementSerialisableItemExact(ITEM_ID_PEACH, AMOUNT_TYPE_COUNT, 30, 5),
            QuestRequirementSerialisableBase(),
            QuestRequirementSerialisableItemExact(ITEM_ID_PEACH, AMOUNT_TYPE_COUNT, 30, 0),
            QuestRequirementSerialisableItemExact(ITEM_ID_PEACH, AMOUNT_TYPE_COUNT, 30, 1),
            QuestRequirementSerialisableItemExact(ITEM_ID_PEACH, AMOUNT_TYPE_COUNT, 30, 2),
            QuestRequirementSerialisableItemExact(ITEM_ID_PEACH, AMOUNT_TYPE_COUNT, 30, 30),
            QuestRequirementSerialisableItemGroup(ITEM_GROUP_ID_KNIFE, AMOUNT_TYPE_COUNT, 1, 0),
            QuestRequirementSerialisableItemCategory(ITEM_FLAG_EDIBLE, AMOUNT_TYPE_COUNT, 60, 0),
            QuestRequirementSerialisableItemExact(ITEM_ID_PEACH, AMOUNT_TYPE_COUNT, 30, 0),
        ],
        None,
    )
    
    linked_quest_entry_id_1 = 56
    linked_quest_1.entry_id = linked_quest_entry_id_1
    
    inventory_1 = Inventory(user_id)
    inventory_1.modify_item_amount(item_peach, 40)
    
    yield (
        linked_quest_1,
        inventory_1,
        10,
        1,
        [
            create_text_display('### Select requirement to submit for'),
            create_separator(),
            create_text_display(f'0 / 30 {item_peach.emoji} {item_peach.name}, 40 on stock'),
            create_row(
                create_button(
                    'Submit items',
                    custom_id = (
                        f'linked_quest.submit_execute_requirement.{user_id:x}.{10:x}.{linked_quest_entry_id_1:x}.'
                        f'{6:x}.{item_peach.id:x}'
                    ),
                    enabled = True,
                    style = ButtonStyle.green,
                ),
                create_button(
                    'Item information',
                    custom_id = (
                        f'linked_quest.submit_info_item_requirement.{user_id:x}.{10:x}.{linked_quest_entry_id_1:x}.'
                        f'{6:x}.{item_peach.id:x}'
                    ),
                ),
            ),
            create_separator(),
            create_text_display(f'1 / 30 {item_peach.emoji} {item_peach.name}, 40 on stock'),
            create_row(
                create_button(
                    'Submit items',
                    custom_id = (
                        f'linked_quest.submit_execute_requirement.{user_id:x}.{10:x}.{linked_quest_entry_id_1:x}.'
                        f'{7:x}.{item_peach.id:x}'
                    ),
                    enabled = True,
                    style = ButtonStyle.green,
                ),
                create_button(
                    'Item information',
                    custom_id = (
                        f'linked_quest.submit_info_item_requirement.{user_id:x}.{10:x}.{linked_quest_entry_id_1:x}.'
                        f'{7:x}.{item_peach.id:x}'
                    ),
                ),
            ),
            create_separator(),
            create_text_display(f'2 / 30 {item_peach.emoji} {item_peach.name}, 40 on stock'),
            create_row(
                create_button(
                    'Submit items',
                    custom_id = (
                        f'linked_quest.submit_execute_requirement.{user_id:x}.{10:x}.{linked_quest_entry_id_1:x}.'
                        f'{8:x}.{item_peach.id:x}'
                    ),
                    enabled = True,
                    style = ButtonStyle.green,
                ),
                create_button(
                    'Item information',
                    custom_id = (
                        f'linked_quest.submit_info_item_requirement.{user_id:x}.{10:x}.{linked_quest_entry_id_1:x}.'
                        f'{8:x}.{item_peach.id:x}'
                    ),
                ),
            ),
            create_separator(),
            create_text_display(f'30 / 30 {item_peach.emoji} {item_peach.name}, 40 on stock'),
            create_row(
                create_button(
                    'Submit items',
                    custom_id = (
                        f'linked_quest.submit_execute_requirement.{user_id:x}.{10:x}.{linked_quest_entry_id_1:x}.'
                        f'{9:x}.{item_peach.id:x}'
                    ),
                    enabled = False,
                    style = ButtonStyle.gray,
                ),
                create_button(
                    'Item information',
                    custom_id = (
                        f'linked_quest.submit_info_item_requirement.{user_id:x}.{10:x}.{linked_quest_entry_id_1:x}.'
                        f'{9:x}.{item_peach.id:x}'
                    ),
                ),
            ),
            create_separator(),
            create_text_display(f'0 / 1 {item_group_knife.emoji} {item_group_knife.name}, none on stock'),
            create_row(
                create_button(
                    'Select item to submit',
                    custom_id = (
                        f'linked_quest.submit_select_item_nested.{user_id:x}.{10:x}.{linked_quest_entry_id_1:x}.'
                        f'{10:x}.{0:x}'
                    ),
                    enabled = False,
                    style = ButtonStyle.green,
                ),
                create_button(
                    'Item group information',
                    custom_id = (
                        f'linked_quest.submit_info_item_group_requirement.{user_id:x}.{10:x}.'
                        f'{linked_quest_entry_id_1:x}.{10:x}.{ITEM_GROUP_ID_KNIFE:x}'
                    ),
                ),
            ),
            create_separator(),
            create_text_display(f'0 / 60 edible, 40 on stock'),
            create_row(
                create_button(
                    'Select item to submit',
                    custom_id = (
                        f'linked_quest.submit_select_item_nested.{user_id:x}.{10:x}.{linked_quest_entry_id_1:x}.'
                        f'{11:x}.{0:x}'
                    ),
                    enabled = True,
                    style = ButtonStyle.green,
                ),
            ),
            create_separator(),
            create_row(
                create_button(
                    'Page 1',
                    EMOJI_PAGE_PREVIOUS,
                    custom_id = (
                        f'linked_quest.submit_select_requirement.{user_id:x}.{10:x}.{linked_quest_entry_id_1:x}.'
                        f'{0:x}'
                    ),
                    enabled = True,
                ),
                create_button(
                    'Page 3',
                    EMOJI_PAGE_NEXT,
                    custom_id = (
                        f'linked_quest.submit_select_requirement.{user_id:x}.{10:x}.{linked_quest_entry_id_1:x}.'
                        f'{2:x}'
                    ),
                    enabled = True,
                ),
                create_button(
                    'Refresh',
                    EMOJI_REFRESH,
                    custom_id = (
                        f'linked_quest.submit_select_requirement.{user_id:x}.{10:x}.{linked_quest_entry_id_1:x}.'
                        f'{1:x}'
                    ),
                ),
                create_button(
                    'Back',
                    EMOJI_BACK,
                    custom_id = f'linked_quest.details.{user_id:x}.{10:x}.{linked_quest_entry_id_1:x}',
                ),
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_linked_quest_submit_select_requirement_components(
    linked_quest, inventory, page_index, requirement_select_page_index
):
    """
    Tests whether ``build_linked_quest_submit_select_requirement_components`` works as intended.
    
    Parameters
    -----------
    linked_quest : ``LinkedQuest``
        Linked quest in context.
    
    inventory : ``Inventory``
        The user's inventory.
    
    page_index : `int`
        The page's index to back-direct to.
    
    requirement_select_page_index : `int`
        The requirement page index to display.
    
    Returns
    -------
    output : ``list<Component>``
    """
    output = build_linked_quest_submit_select_requirement_components(
       linked_quest, inventory, page_index, requirement_select_page_index
    )
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
