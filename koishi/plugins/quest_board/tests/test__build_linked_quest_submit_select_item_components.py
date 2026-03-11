import vampytest
from hata import ButtonStyle, Component, create_button, create_row, create_separator, create_text_display

from ...inventory_core import Inventory
from ...item_core import (
    ITEM_FLAG_EDIBLE, ITEM_GROUP_ID_KNIFE, ITEM_ID_BAMBOO_SHOOT, ITEM_ID_BLUEBERRY, ITEM_ID_BLUEFRANKISH,
    ITEM_ID_CARROT, ITEM_ID_DEVILCART_OYSTER, ITEM_ID_FLYKILLER_AMANITA, ITEM_ID_GARLIC, ITEM_ID_PEACH,
    ITEM_ID_SCARLET_ONION, ITEM_ID_STRAWBERRY, get_item_nullable
)
from ...quest_core import (
    AMOUNT_TYPE_COUNT, LinkedQuest, QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY, QuestRequirementSerialisableBase,
    QuestRequirementSerialisableItemCategory, QuestRequirementSerialisableItemExact,
    QuestRequirementSerialisableItemGroup
)

from ..component_building import build_linked_quest_submit_select_item_components
from ..constants import EMOJI_BACK, EMOJI_PAGE_NEXT, EMOJI_PAGE_PREVIOUS, EMOJI_REFRESH


def _iter_options():
    item_carrot = get_item_nullable(ITEM_ID_CARROT)
    assert item_carrot is not None
    
    item_bamboo_shoot = get_item_nullable(ITEM_ID_BAMBOO_SHOOT)
    assert item_bamboo_shoot is not None
    
    item_blueberry = get_item_nullable(ITEM_ID_BLUEBERRY)
    assert item_blueberry is not None
    
    item_bluefrankish = get_item_nullable(ITEM_ID_BLUEFRANKISH)
    assert item_bluefrankish is not None
    
    item_devilcart_oyster = get_item_nullable(ITEM_ID_DEVILCART_OYSTER)
    assert item_devilcart_oyster is not None
    
    item_flykiller_amanita = get_item_nullable(ITEM_ID_FLYKILLER_AMANITA)
    assert item_flykiller_amanita is not None
    
    item_garlic = get_item_nullable(ITEM_ID_GARLIC)
    assert item_garlic is not None
    
    item_peach = get_item_nullable(ITEM_ID_PEACH)
    assert item_peach is not None
    
    item_scarlet_onion = get_item_nullable(ITEM_ID_SCARLET_ONION)
    assert item_scarlet_onion is not None
    
    item_strawberry = get_item_nullable(ITEM_ID_STRAWBERRY)
    assert item_strawberry is not None
    
    
    user_id = 202603060000
    guild_id = 202603060001
    batch_id = 202603060002
    
    
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
        1,
        0,
        False,
        [
            create_text_display(
                '### Select item to submit'
            ),
            create_separator(),
            create_row(
                create_button(
                    'Page 0',
                    EMOJI_PAGE_PREVIOUS,
                    custom_id = 'linked_quest.submit_select_item.page_decrement_disabled',
                    enabled = False,
                ),
                create_button(
                    'Page 2',
                    EMOJI_PAGE_NEXT,
                    custom_id = 'linked_quest.submit_select_item.page_increment_disabled',
                    enabled = False,
                ),
                create_button(
                    'Refresh',
                    EMOJI_REFRESH,
                    custom_id = (
                        f'linked_quest.submit_select_item_nested.{user_id:x}.{10:x}.{linked_quest_entry_id_0:x}.'
                        f'{1:x}.{0:x}'
                    ),
                ),
                create_button(
                    'Back',
                    EMOJI_BACK,
                    custom_id = (
                        f'linked_quest.submit_select_requirement.{user_id:x}.{10:x}.{linked_quest_entry_id_0:x}.'
                        f'{0:x}'
                    ),
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
    
    linked_quest_entry_id_1 = 78
    linked_quest_1.entry_id = linked_quest_entry_id_1
    
    inventory_1 = Inventory(user_id)
    inventory_1.modify_item_amount(item_carrot, 40)
    inventory_1.modify_item_amount(item_bamboo_shoot, 41)
    inventory_1.modify_item_amount(item_blueberry, 42)
    inventory_1.modify_item_amount(item_bluefrankish, 43)
    inventory_1.modify_item_amount(item_devilcart_oyster, 44)
    inventory_1.modify_item_amount(item_flykiller_amanita, 45)
    inventory_1.modify_item_amount(item_garlic, 46)
    inventory_1.modify_item_amount(item_peach, 47)
    inventory_1.modify_item_amount(item_scarlet_onion, 48)
    inventory_1.modify_item_amount(item_strawberry, 49)
    
    yield (
        linked_quest_1,
        inventory_1,
        10,
        11,
        1,
        False,
        [
            create_text_display(
                '### Select item to submit\n'
                '\n'
                '0 / 60 edible, 445 on stock'
            ),
            create_separator(),
            create_text_display(f'46 {item_garlic.emoji} {item_garlic.name}'),
            create_row(
                create_button(
                    'Submit items',
                    custom_id = (
                        f'linked_quest.submit_execute_item_nested.{user_id:x}.{10:x}.{linked_quest_entry_id_1:x}.'
                        f'{11:x}.{1:x}.{item_garlic.id:x}'
                    ),
                    enabled = True,
                    style = ButtonStyle.green,
                ),
                create_button(
                    'Item information',
                    custom_id = (
                        f'linked_quest.submit_info_item_nested.{user_id:x}.{10:x}.{linked_quest_entry_id_1:x}.'
                        f'{11:x}.{1:x}.{item_garlic.id:x}'
                    ),
                ),
            ),
            create_separator(),
            create_text_display(f'47 {item_peach.emoji} {item_peach.name}'),
            create_row(
                create_button(
                    'Submit items',
                    custom_id = (
                        f'linked_quest.submit_execute_item_nested.{user_id:x}.{10:x}.{linked_quest_entry_id_1:x}.'
                        f'{11:x}.{1:x}.{item_peach.id:x}'
                    ),
                    enabled = True,
                    style = ButtonStyle.green,
                ),
                create_button(
                    'Item information',
                    custom_id = (
                        f'linked_quest.submit_info_item_nested.{user_id:x}.{10:x}.{linked_quest_entry_id_1:x}.'
                        f'{11:x}.{1:x}.{item_peach.id:x}'
                    ),
                ),
            ),
            create_separator(),
            create_text_display(f'48 {item_scarlet_onion.emoji} {item_scarlet_onion.name}'),
            create_row(
                create_button(
                    'Submit items',
                    custom_id = (
                        f'linked_quest.submit_execute_item_nested.{user_id:x}.{10:x}.{linked_quest_entry_id_1:x}.'
                        f'{11:x}.{1:x}.{item_scarlet_onion.id:x}'
                    ),
                    enabled = True,
                    style = ButtonStyle.green,
                ),
                create_button(
                    'Item information',
                    custom_id = (
                        f'linked_quest.submit_info_item_nested.{user_id:x}.{10:x}.{linked_quest_entry_id_1:x}.'
                        f'{11:x}.{1:x}.{item_scarlet_onion.id:x}'
                    ),
                ),
            ),
            create_separator(),
            create_text_display(f'49 {item_strawberry.emoji} {item_strawberry.name}'),
            create_row(
                create_button(
                    'Submit items',
                    custom_id = (
                        f'linked_quest.submit_execute_item_nested.{user_id:x}.{10:x}.{linked_quest_entry_id_1:x}.'
                        f'{11:x}.{1:x}.{item_strawberry.id:x}'
                    ),
                    enabled = True,
                    style = ButtonStyle.green,
                ),
                create_button(
                    'Item information',
                    custom_id = (
                        f'linked_quest.submit_info_item_nested.{user_id:x}.{10:x}.{linked_quest_entry_id_1:x}.'
                        f'{11:x}.{1:x}.{item_strawberry.id:x}'
                    ),
                ),
            ),
            create_separator(),
            create_row(
                create_button(
                    'Page 1',
                    EMOJI_PAGE_PREVIOUS,
                    custom_id = (
                        f'linked_quest.submit_select_item_nested.{user_id:x}.{10:x}.{linked_quest_entry_id_1:x}.'
                        f'{11:x}.{0:x}'
                    ),
                    enabled = True,
                ),
                create_button(
                    'Page 3',
                    EMOJI_PAGE_NEXT,
                    custom_id = 'linked_quest.submit_select_item.page_increment_disabled',
                    enabled = False,
                ),
                create_button(
                    'Refresh',
                    EMOJI_REFRESH,
                    custom_id = (
                        f'linked_quest.submit_select_item_nested.{user_id:x}.{10:x}.{linked_quest_entry_id_1:x}.'
                        f'{11:x}.{1:x}'
                    ),
                ),
                create_button(
                    'Back',
                    EMOJI_BACK,
                    custom_id = (
                        f'linked_quest.submit_select_requirement.{user_id:x}.{10:x}.{linked_quest_entry_id_1:x}.'
                        f'{1:x}'
                    ),
                ),
            ),
        ],
    )
    
    linked_quest_2 = LinkedQuest(
        user_id,
        guild_id,
        batch_id,
        QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
        None,
        None,
    )
    
    linked_quest_entry_id_2 = 58
    linked_quest_2.entry_id = linked_quest_entry_id_2
    
    inventory_2 = Inventory(user_id)
    
    yield (
        linked_quest_2,
        inventory_2,
        10,
        0,
        0,
        True,
        [
            create_text_display(
                '### Select item to submit'
            ),
            create_separator(),
            create_row(
                create_button(
                    'Page 0',
                    EMOJI_PAGE_PREVIOUS,
                    custom_id = 'linked_quest.submit_select_item.page_decrement_disabled',
                    enabled = False,
                ),
                create_button(
                    'Page 2',
                    EMOJI_PAGE_NEXT,
                    custom_id = 'linked_quest.submit_select_item.page_increment_disabled',
                    enabled = False,
                ),
                create_button(
                    'Refresh',
                    EMOJI_REFRESH,
                    custom_id = (
                        f'linked_quest.submit_select_item_top.{user_id:x}.{10:x}.{linked_quest_entry_id_2:x}.'
                        f'{0:x}'
                    ),
                ),
                create_button(
                    'Back',
                    EMOJI_BACK,
                    custom_id = (
                        f'linked_quest.details.{user_id:x}.{10:x}.{linked_quest_entry_id_2:x}'
                    ),
                ),
            ),
        ],
    )
    
    linked_quest_3 = LinkedQuest(
        user_id,
        guild_id,
        batch_id,
        QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
        [
            QuestRequirementSerialisableItemCategory(ITEM_FLAG_EDIBLE, AMOUNT_TYPE_COUNT, 60, 0),
        ],
        None,
    )
    
    linked_quest_entry_id_3 = 61222
    linked_quest_3.entry_id = linked_quest_entry_id_3
    
    inventory_3 = Inventory(user_id)
    inventory_3.modify_item_amount(item_carrot, 40)
    inventory_3.modify_item_amount(item_bamboo_shoot, 41)
    inventory_3.modify_item_amount(item_blueberry, 42)
    inventory_3.modify_item_amount(item_bluefrankish, 43)
    inventory_3.modify_item_amount(item_devilcart_oyster, 44)
    inventory_3.modify_item_amount(item_flykiller_amanita, 45)
    inventory_3.modify_item_amount(item_garlic, 46)
    inventory_3.modify_item_amount(item_peach, 47)
    inventory_3.modify_item_amount(item_scarlet_onion, 48)
    inventory_3.modify_item_amount(item_strawberry, 49)
    
    yield (
        linked_quest_3,
        inventory_3,
        10,
        0,
        1,
        True,
        [
            create_text_display(
                '### Select item to submit\n'
                '\n'
                '0 / 60 edible, 445 on stock'
            ),
            create_separator(),
            create_text_display(f'46 {item_garlic.emoji} {item_garlic.name}'),
            create_row(
                create_button(
                    'Submit items',
                    custom_id = (
                        f'linked_quest.submit_execute_item_top.{user_id:x}.{10:x}.{linked_quest_entry_id_3:x}.'
                        f'{1:x}.{item_garlic.id:x}'
                    ),
                    enabled = True,
                    style = ButtonStyle.green,
                ),
                create_button(
                    'Item information',
                    custom_id = (
                        f'linked_quest.submit_info_item_top.{user_id:x}.{10:x}.{linked_quest_entry_id_3:x}.'
                        f'{1:x}.{item_garlic.id:x}'
                    ),
                ),
            ),
            create_separator(),
            create_text_display(f'47 {item_peach.emoji} {item_peach.name}'),
            create_row(
                create_button(
                    'Submit items',
                    custom_id = (
                        f'linked_quest.submit_execute_item_top.{user_id:x}.{10:x}.{linked_quest_entry_id_3:x}.'
                        f'{1:x}.{item_peach.id:x}'
                    ),
                    enabled = True,
                    style = ButtonStyle.green,
                ),
                create_button(
                    'Item information',
                    custom_id = (
                        f'linked_quest.submit_info_item_top.{user_id:x}.{10:x}.{linked_quest_entry_id_3:x}.'
                        f'{1:x}.{item_peach.id:x}'
                    ),
                ),
            ),
            create_separator(),
            create_text_display(f'48 {item_scarlet_onion.emoji} {item_scarlet_onion.name}'),
            create_row(
                create_button(
                    'Submit items',
                    custom_id = (
                        f'linked_quest.submit_execute_item_top.{user_id:x}.{10:x}.{linked_quest_entry_id_3:x}.'
                        f'{1:x}.{item_scarlet_onion.id:x}'
                    ),
                    enabled = True,
                    style = ButtonStyle.green,
                ),
                create_button(
                    'Item information',
                    custom_id = (
                        f'linked_quest.submit_info_item_top.{user_id:x}.{10:x}.{linked_quest_entry_id_3:x}.'
                        f'{1:x}.{item_scarlet_onion.id:x}'
                    ),
                ),
            ),
            create_separator(),
            create_text_display(f'49 {item_strawberry.emoji} {item_strawberry.name}'),
            create_row(
                create_button(
                    'Submit items',
                    custom_id = (
                        f'linked_quest.submit_execute_item_top.{user_id:x}.{10:x}.{linked_quest_entry_id_3:x}.'
                        f'{1:x}.{item_strawberry.id:x}'
                    ),
                    enabled = True,
                    style = ButtonStyle.green,
                ),
                create_button(
                    'Item information',
                    custom_id = (
                        f'linked_quest.submit_info_item_top.{user_id:x}.{10:x}.{linked_quest_entry_id_3:x}.'
                        f'{1:x}.{item_strawberry.id:x}'
                    ),
                ),
            ),
            create_separator(),
            create_row(
                create_button(
                    'Page 1',
                    EMOJI_PAGE_PREVIOUS,
                    custom_id = (
                        f'linked_quest.submit_select_item_top.{user_id:x}.{10:x}.{linked_quest_entry_id_3:x}.'
                        f'{0:x}'
                    ),
                    enabled = True,
                ),
                create_button(
                    'Page 3',
                    EMOJI_PAGE_NEXT,
                    custom_id = 'linked_quest.submit_select_item.page_increment_disabled',
                    enabled = False,
                ),
                create_button(
                    'Refresh',
                    EMOJI_REFRESH,
                    custom_id = (
                        f'linked_quest.submit_select_item_top.{user_id:x}.{10:x}.{linked_quest_entry_id_3:x}.'
                        f'{1:x}'
                    ),
                ),
                create_button(
                    'Back',
                    EMOJI_BACK,
                    custom_id = (
                        f'linked_quest.details.{user_id:x}.{10:x}.{linked_quest_entry_id_3:x}'
                    ),
                ),
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_linked_quest_submit_select_item_components(
    linked_quest, inventory, page_index, requirement_index, item_page_index, top
):
    """
    Builds linked quest submission select requirement components.
    
    Parameters
    -----------
    linked_quest : ``LinkedQuest``
        Linked quest in context.
    
    inventory : ``Inventory``
        The user's inventory.
    
    page_index : `int`
        The page's index to back-direct to.
    
    requirement_index : `int`
        The requirement's page index to display.
    
    item_page_index : `int`
        The current local page index.
    
    top : `int`
        Whether to use top custom identifiers.
    
    Returns
    -------
    output : ``list<Component>``
    """
    output = build_linked_quest_submit_select_item_components(
       linked_quest, inventory, page_index, requirement_index, item_page_index, top
    )
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
