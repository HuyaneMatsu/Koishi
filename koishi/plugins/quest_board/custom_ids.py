__all__ = ()

from re import compile as re_compile, escape as re_escape


CUSTOM_ID_QUEST_BOARD_BASE = 'quest_board'

CUSTOM_ID_QUEST_BOARD_QUEST_DETAILS_BUILDER = (
    lambda user_id, guild_id, page_index, quest_template_id :
    f'{CUSTOM_ID_QUEST_BOARD_BASE}.details.{user_id:x}.{guild_id:x}.{page_index:x}.{quest_template_id:x}'
)
CUSTOM_ID_QUEST_BOARD_QUEST_DETAILS_PATTERN = re_compile(
    f'{re_escape(CUSTOM_ID_QUEST_BOARD_BASE)}\\.details\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)'
)
CUSTOM_ID_QUEST_BOARD_PAGE_INDEX_NAVIGATE_BUILDER = (
    lambda user_id, page_index :
    f'{CUSTOM_ID_QUEST_BOARD_BASE}.page.{user_id:x}.{page_index:x}'
)
CUSTOM_ID_QUEST_BOARD_PAGE_INDEX_DECREMENT_DISABLED = (
    f'{CUSTOM_ID_QUEST_BOARD_BASE}.page_decrement_disabled'
)
CUSTOM_ID_QUEST_BOARD_PAGE_INDEX_INCREMENT_DISABLED = (
    f'{CUSTOM_ID_QUEST_BOARD_BASE}.page_increment_disabled'
)
CUSTOM_ID_QUEST_BOARD_PAGE_INDEX_NAVIGATE_PATTERN = re_compile(
    f'{re_escape(CUSTOM_ID_QUEST_BOARD_BASE)}\\.page\\.([0-9a-f]+)\\.([0-9a-f]+)'
)
CUSTOM_ID_QUEST_ACCEPT_BUILDER = (
    lambda user_id, guild_id, page_index, quest_template_id :
    f'{CUSTOM_ID_QUEST_BOARD_BASE}.accept.{user_id:x}.{guild_id:x}.{page_index:x}.{quest_template_id:x}'
)
CUSTOM_ID_QUEST_ACCEPT_DISABLED = f'{CUSTOM_ID_QUEST_BOARD_BASE}.accept_disabled'

CUSTOM_ID_QUEST_ACCEPT_PATTERN = re_compile(
    f'{re_escape(CUSTOM_ID_QUEST_BOARD_BASE)}\\.accept\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)'
)

CUSTOM_ID_QUEST_BOARD_ITEM_DISABLED = f'{CUSTOM_ID_QUEST_BOARD_BASE}.item_disabled'
CUSTOM_ID_QUEST_BOARD_ITEM_BUILDER = (
    lambda user_id, guild_id, page_index, quest_template_id, item_id :
    f'{CUSTOM_ID_QUEST_BOARD_BASE}.item.{user_id:x}.{guild_id:x}.{page_index:x}.{quest_template_id:x}.{item_id:x}'
)
CUSTOM_ID_QUEST_BOARD_ITEM_PATTERN = re_compile(
    f'{re_escape(CUSTOM_ID_QUEST_BOARD_BASE)}\\.item\\.'
    f'([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)'
)


CUSTOM_ID_LINKED_QUEST_BASE = 'linked_quest'

CUSTOM_ID_LINKED_QUEST_ITEM_INFO_BUILDER = (
    lambda user_id, page_index, linked_quest_entry_id :
    f'{CUSTOM_ID_LINKED_QUEST_BASE}.details.{user_id:x}.{page_index:x}.{linked_quest_entry_id:x}'
)
CUSTOM_ID_LINKED_QUEST_ITEM_INFO_PATTERN = re_compile(
    f'{re_escape(CUSTOM_ID_LINKED_QUEST_BASE)}\\.details\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)'
)
CUSTOM_ID_LINKED_QUEST_PAGE_INDEX_NAVIGATE_BUILDER = (
    lambda user_id, page_index :
    f'{CUSTOM_ID_LINKED_QUEST_BASE}.page.{user_id:x}.{page_index:x}'
)
CUSTOM_ID_LINKED_QUEST_PAGE_INDEX_DECREMENT_DISABLED = (
    f'{CUSTOM_ID_LINKED_QUEST_BASE}.page_decrement_disabled'
)
CUSTOM_ID_LINKED_QUEST_PAGE_INDEX_INCREMENT_DISABLED = (
    f'{CUSTOM_ID_LINKED_QUEST_BASE}.page_increment_disabled'
)
CUSTOM_ID_LINKED_QUEST_PAGE_INDEX_NAVIGATE_PATTERN = re_compile(
    f'{re_escape(CUSTOM_ID_LINKED_QUEST_BASE)}\\.page\\.([0-9a-f]+)\\.([0-9a-f]+)'
)
CUSTOM_ID_LINKED_QUEST_SUBMIT_DISABLED = (
    f'{CUSTOM_ID_LINKED_QUEST_BASE}.submit_disabled'
)
CUSTOM_ID_LINKED_QUEST_SUBMIT_AUTO_BUILDER = (
    lambda user_id, page_index, linked_quest_entry_id : 
    f'{CUSTOM_ID_LINKED_QUEST_BASE}.submit_auto.{user_id:x}.{page_index:x}.{linked_quest_entry_id:x}'
)
CUSTOM_ID_LINKED_QUEST_SUBMIT_AUTO_PATTERN = re_compile(
    f'{re_escape(CUSTOM_ID_LINKED_QUEST_BASE)}\\.submit_auto\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)'
)

CUSTOM_ID_LINKED_QUEST_SUBMIT_SELECT_REQUIREMENT_BUILDER = (
    lambda user_id, page_index, linked_quest_entry_id, requirement_select_page_index : (
        f'{CUSTOM_ID_LINKED_QUEST_BASE}.submit_select_requirement.{user_id:x}.{page_index:x}.'
        f'{linked_quest_entry_id:x}.{requirement_select_page_index:x}'
    )
)
CUSTOM_ID_LINKED_QUEST_SUBMIT_SELECT_REQUIREMENT_PATTERN = re_compile(
    f'{re_escape(CUSTOM_ID_LINKED_QUEST_BASE)}\\.submit_select_requirement\\.'
    f'([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)'
)

CUSTOM_ID_LINKED_QUEST_SUBMIT_SELECT_REQUIREMENT_PAGE_INDEX_DECREMENT_DISABLED = (
    f'{CUSTOM_ID_LINKED_QUEST_BASE}.submit_select_requirement.page_decrement_disabled'
)

CUSTOM_ID_LINKED_QUEST_SUBMIT_SELECT_REQUIREMENT_PAGE_INDEX_INCREMENT_DISABLED = (
    f'{CUSTOM_ID_LINKED_QUEST_BASE}.submit_select_requirement.page_increment_disabled'
)

CUSTOM_ID_LINKED_QUEST_SUBMIT_SELECT_ITEM_TOP_BUILDER = (
    lambda user_id, page_index, linked_quest_entry_id, item_select_page_index : (
        f'{CUSTOM_ID_LINKED_QUEST_BASE}.submit_select_item_top.{user_id:x}.{page_index:x}.{linked_quest_entry_id:x}.'
        f'{item_select_page_index:x}'
    )
)

CUSTOM_ID_LINKED_QUEST_SUBMIT_SELECT_ITEM_TOP_PATTERN = re_compile(
    f'{re_escape(CUSTOM_ID_LINKED_QUEST_BASE)}\\.submit_select_item_top\\.'
    f'([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)'
)

CUSTOM_ID_LINKED_QUEST_SUBMIT_SELECT_ITEM_NESTED_BUILDER = (
    lambda 
        user_id, page_index, linked_quest_entry_id, requirement_index, item_page_index
    : (
        f'{CUSTOM_ID_LINKED_QUEST_BASE}.submit_select_item_nested.{user_id:x}.{page_index:x}.{linked_quest_entry_id:x}.'
        f'{requirement_index:x}.{item_page_index:x}'
    )
)
CUSTOM_ID_LINKED_QUEST_SUBMIT_SELECT_ITEM_NESTED_PATTERN = re_compile(
    f'{re_escape(CUSTOM_ID_LINKED_QUEST_BASE)}\\.submit_select_item_nested\\.'
    f'([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)'
)

CUSTOM_ID_LINKED_QUEST_SUBMIT_SELECT_ITEM_PAGE_INDEX_DECREMENT_DISABLED = (
    f'{CUSTOM_ID_LINKED_QUEST_BASE}.submit_select_item.page_decrement_disabled'
)

CUSTOM_ID_LINKED_QUEST_SUBMIT_SELECT_ITEM_PAGE_INDEX_INCREMENT_DISABLED = (
    f'{CUSTOM_ID_LINKED_QUEST_BASE}.submit_select_item.page_increment_disabled'
)

CUSTOM_ID_LINKED_QUEST_SUBMIT_EXECUTE_REQUIREMENT_BUILDER = (
    lambda user_id, page_index, linked_quest_entry_id, requirement_index, item_id : (
        f'{CUSTOM_ID_LINKED_QUEST_BASE}.submit_execute_requirement.{user_id:x}.{page_index:x}.{linked_quest_entry_id:x}.'
        f'{requirement_index:x}.{item_id:x}'
    )
)

CUSTOM_ID_LINKED_QUEST_SUBMIT_EXECUTE_REQUIREMENT_PATTERN = re_compile(
    f'{re_escape(CUSTOM_ID_LINKED_QUEST_BASE)}\\.submit_execute_requirement\\.'
    f'([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)'
)

CUSTOM_ID_LINKED_QUEST_SUBMIT_EXECUTE_ITEM_TOP_BUILDER = (
    lambda user_id, page_index, linked_quest_entry_id, item_page_index, item_id : (
        f'{CUSTOM_ID_LINKED_QUEST_BASE}.submit_execute_item_top.{user_id:x}.{page_index:x}.{linked_quest_entry_id:x}.'
        f'{item_page_index:x}.{item_id:x}'
    )
)

CUSTOM_ID_LINKED_QUEST_SUBMIT_EXECUTE_ITEM_TOP_PATTERN = re_compile(
    f'{re_escape(CUSTOM_ID_LINKED_QUEST_BASE)}\\.submit_execute_item_top\\.'
    f'([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)'
)

CUSTOM_ID_LINKED_QUEST_SUBMIT_EXECUTE_ITEM_NESTED_BUILDER = (
    lambda user_id, page_index, linked_quest_entry_id, requirement_index, item_page_index, item_id : (
        f'{CUSTOM_ID_LINKED_QUEST_BASE}.submit_execute_item_nested.{user_id:x}.{page_index:x}.{linked_quest_entry_id:x}.'
        f'{requirement_index:x}.{item_page_index:x}.{item_id:x}'
    )
)
CUSTOM_ID_LINKED_QUEST_SUBMIT_EXECUTE_ITEM_NESTED_PATTERN = re_compile(
    f'{re_escape(CUSTOM_ID_LINKED_QUEST_BASE)}\\.submit_execute_item_nested\\.'
    f'([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)'
)


CUSTOM_ID_LINKED_QUEST_SUBMIT_INFO_REQUIREMENT_BUILDER = (
    lambda user_id, page_index, linked_quest_entry_id, requirement_index, item_id : (
        f'{CUSTOM_ID_LINKED_QUEST_BASE}.submit_info_requirement.{user_id:x}.{page_index:x}.{linked_quest_entry_id:x}.'
        f'{requirement_index:x}.{item_id:x}'
    )
)

CUSTOM_ID_LINKED_QUEST_SUBMIT_INFO_REQUIREMENT_PATTERN = re_compile(
    f'{re_escape(CUSTOM_ID_LINKED_QUEST_BASE)}\\.submit_info_requirement\\.'
    f'([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)'
)

CUSTOM_ID_LINKED_QUEST_SUBMIT_INFO_ITEM_TOP_BUILDER = (
    lambda user_id, page_index, linked_quest_entry_id, item_page_index, item_id : (
        f'{CUSTOM_ID_LINKED_QUEST_BASE}.submit_info_item_top.{user_id:x}.{page_index:x}.{linked_quest_entry_id:x}.'
        f'{item_page_index:x}.{item_id:x}'
    )
)

CUSTOM_ID_LINKED_QUEST_SUBMIT_INFO_ITEM_TOP_PATTERN = re_compile(
    f'{re_escape(CUSTOM_ID_LINKED_QUEST_BASE)}\\.submit_info_item_top\\.'
    f'([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)'
)

CUSTOM_ID_LINKED_QUEST_SUBMIT_INFO_ITEM_NESTED_BUILDER = (
    lambda user_id, page_index, linked_quest_entry_id, requirement_index, item_page_index, item_id : (
        f'{CUSTOM_ID_LINKED_QUEST_BASE}.submit_info_item_nested.{user_id:x}.{page_index:x}.{linked_quest_entry_id:x}.'
        f'{requirement_index:x}.{item_page_index:x}.{item_id:x}'
    )
)

CUSTOM_ID_LINKED_QUEST_SUBMIT_INFO_ITEM_NESTED_PATTERN = re_compile(
    f'{re_escape(CUSTOM_ID_LINKED_QUEST_BASE)}\\.submit_info_item_nested\\.'
    f'([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)'
)

CUSTOM_ID_LINKED_QUEST_ABANDON_BUILDER = (
    lambda user_id, page_index, linked_quest_entry_id :
    f'{CUSTOM_ID_LINKED_QUEST_BASE}.abandon.{user_id:x}.{page_index}.{linked_quest_entry_id:x}'
)
CUSTOM_ID_LINKED_QUEST_ABANDON_PATTERN = re_compile(
    f'{re_escape(CUSTOM_ID_LINKED_QUEST_BASE)}\\.abandon\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)'
)

CUSTOM_ID_LINKED_QUEST_INFO_ITEM_DISABLED = f'{CUSTOM_ID_LINKED_QUEST_BASE}.item_disabled'
CUSTOM_ID_LINKED_QUEST_INFO_ITEM_BUILDER = (
    lambda user_id, page_index, linked_quest_entry_id, item_id :
    f'{CUSTOM_ID_LINKED_QUEST_BASE}.item.{user_id:x}.{page_index:x}.{linked_quest_entry_id:x}.{item_id:x}'
)
CUSTOM_ID_LINKED_QUEST_INFO_ITEM_PATTERN = re_compile(
    f'{re_escape(CUSTOM_ID_LINKED_QUEST_BASE)}\\.item\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)'
)
