import vampytest
from hata import Component, create_button, create_row, create_separator, create_text_display

from ...inventory_core import Inventory
from ...item_core import (
    ITEM_FLAG_EDIBLE, ITEM_GROUP_ID_KNIFE, ITEM_ID_PEACH, get_item_group_nullable, get_item_nullable
)
from ...quest_core import (
    AMOUNT_TYPE_COUNT, Quest, QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY, QuestRequirementInstantiableBase,
    QuestRequirementInstantiableItemCategory, QuestRequirementInstantiableItemExact,
    QuestRequirementInstantiableItemGroup
)

from ..component_building import build_quest_select_requirement_components
from ..constants import EMOJI_BACK, EMOJI_PAGE_NEXT, EMOJI_PAGE_PREVIOUS


def _iter_options():
    item_peach = get_item_nullable(ITEM_ID_PEACH)
    assert item_peach is not None
    
    item_group_knife = get_item_group_nullable(ITEM_GROUP_ID_KNIFE)
    assert item_group_knife is not None
    
    user_id = 202603290000
    guild_id = 202603290001
    
    
    quest_0 = Quest(
        QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
        None,
        None,
    )
    
    inventory_0 = Inventory(user_id)
    
    yield (
        user_id,
        guild_id,
        quest_0,
        inventory_0,
        10,
        0,
        [
            create_text_display('### Select requirement to inspect'),
            create_separator(),
            create_row(
                create_button(
                    'Page 0',
                    EMOJI_PAGE_PREVIOUS,
                    custom_id = 'quest_board.select_requirement.page_decrement_disabled',
                    enabled = False,
                ),
                create_button(
                    'Page 2',
                    EMOJI_PAGE_NEXT,
                    custom_id = 'quest_board.select_requirement.page_increment_disabled',
                    enabled = False,
                ),
                create_button(
                    'Back',
                    EMOJI_BACK,
                    custom_id = (
                        f'quest_board.details.{user_id:x}.{guild_id:x}.{10:x}.{QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY:x}'
                    ),
                ),
            ),
        ],
    )
    
    quest_1 = Quest(
        QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
        [
            QuestRequirementInstantiableItemExact(ITEM_ID_PEACH, AMOUNT_TYPE_COUNT, 30),
            QuestRequirementInstantiableItemExact(ITEM_ID_PEACH, AMOUNT_TYPE_COUNT, 31),
            QuestRequirementInstantiableItemExact(ITEM_ID_PEACH, AMOUNT_TYPE_COUNT, 32),
            QuestRequirementInstantiableItemExact(ITEM_ID_PEACH, AMOUNT_TYPE_COUNT, 33),
            QuestRequirementInstantiableItemExact(ITEM_ID_PEACH, AMOUNT_TYPE_COUNT, 37),
            QuestRequirementInstantiableItemExact(ITEM_ID_PEACH, AMOUNT_TYPE_COUNT, 35),
            QuestRequirementInstantiableBase(),
            QuestRequirementInstantiableItemExact(ITEM_ID_PEACH, AMOUNT_TYPE_COUNT, 36),
            QuestRequirementInstantiableItemExact(ITEM_ID_PEACH, AMOUNT_TYPE_COUNT, 37),
            QuestRequirementInstantiableItemExact(ITEM_ID_PEACH, AMOUNT_TYPE_COUNT, 38),
            QuestRequirementInstantiableItemExact(ITEM_ID_PEACH, AMOUNT_TYPE_COUNT, 39),
            QuestRequirementInstantiableItemGroup(ITEM_GROUP_ID_KNIFE, AMOUNT_TYPE_COUNT, 1),
            QuestRequirementInstantiableItemCategory(ITEM_FLAG_EDIBLE, AMOUNT_TYPE_COUNT, 60),
            QuestRequirementInstantiableItemExact(ITEM_ID_PEACH, AMOUNT_TYPE_COUNT, 40),
        ],
        None,
    )
    
    inventory_1 = Inventory(user_id)
    inventory_1.modify_item_amount(item_peach, 40)
    
    yield (
        user_id,
        guild_id,
        quest_1,
        inventory_1,
        10,
        1,
        [
            create_text_display('### Select requirement to inspect'),
            create_separator(),
            create_text_display(f'36 {item_peach.emoji} {item_peach.name}, 40 on stock'),
            create_row(
                create_button(
                    'Item information',
                    custom_id = (
                        f'quest_board.select_item_requirement.{user_id:x}.{guild_id:x}.{10:x}.'
                        f'{QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY:x}.{6:x}.{item_peach.id:x}'
                    ),
                ),
            ),
            create_separator(),
            create_text_display(f'37 {item_peach.emoji} {item_peach.name}, 40 on stock'),
            create_row(
                create_button(
                    'Item information',
                    custom_id = (
                        f'quest_board.select_item_requirement.{user_id:x}.{guild_id:x}.{10:x}.'
                        f'{QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY:x}.{7:x}.{item_peach.id:x}'
                    ),
                ),
            ),
            create_separator(),
            create_text_display(f'38 {item_peach.emoji} {item_peach.name}, 40 on stock'),
            create_row(
                create_button(
                    'Item information',
                    custom_id = (
                        f'quest_board.select_item_requirement.{user_id:x}.{guild_id:x}.{10:x}.'
                        f'{QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY:x}.{8:x}.{item_peach.id:x}'
                    ),
                ),
            ),
            create_separator(),
            create_text_display(f'39 {item_peach.emoji} {item_peach.name}, 40 on stock'),
            create_row(
                create_button(
                    'Item information',
                    custom_id = (
                        f'quest_board.select_item_requirement.{user_id:x}.{guild_id:x}.{10:x}.'
                        f'{QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY:x}.{9:x}.{item_peach.id:x}'
                    ),
                ),
            ),
            create_separator(),
            create_text_display(f'1 {item_group_knife.emoji} {item_group_knife.name}, none on stock'),
            create_row(
                create_button(
                    'Item group information',
                    custom_id = (
                        f'quest_board.select_item_group_requirement.{user_id:x}.{guild_id:x}.{10:x}.'
                        f'{QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY:x}.{10:x}.{ITEM_GROUP_ID_KNIFE:x}'
                    ),
                ),
            ),
            create_separator(),
            create_text_display(f'60 edible, 40 on stock'),
            create_separator(),
            create_row(
                create_button(
                    'Page 1',
                    EMOJI_PAGE_PREVIOUS,
                    custom_id = (
                        f'quest_board.select_requirement.{user_id:x}.{guild_id:x}.{10:x}.'
                        f'{QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY:x}.{0:x}'
                    ),
                    enabled = True,
                ),
                create_button(
                    'Page 3',
                    EMOJI_PAGE_NEXT,
                    custom_id = (
                        f'quest_board.select_requirement.{user_id:x}.{guild_id:x}.{10:x}.'
                        f'{QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY:x}.{2:x}'
                    ),
                    enabled = True,
                ),
                create_button(
                    'Back',
                    EMOJI_BACK,
                    custom_id = (
                        f'quest_board.details.{user_id:x}.{guild_id:x}.{10:x}.{QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY:x}'
                    ),
                ),
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_quest_select_requirement_components(
    user_id, guild_id, quest, inventory, page_index, requirement_select_page_index
):
    """
    Tests whether ``build_quest_select_requirement_components`` works as intended.
    
    Parameters
    -----------
    user_id : `int`
        The invoking user's identifier.
    
    guild_id : `int`
        The parent quest's guild's identifier.
    
    quest : ``Quest``
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
    output = build_quest_select_requirement_components(
       user_id, guild_id, quest, inventory, page_index, requirement_select_page_index
    )
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
