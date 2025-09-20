__all__ = ()

from re import compile as re_compile, escape as re_escape

from hata import BUILTIN_EMOJIS


BROKEN_QUEST_DESCRIPTION = 'Broken quest'

EMOJI_PAGE_PREVIOUS = BUILTIN_EMOJIS['arrow_left']
EMOJI_PAGE_NEXT = BUILTIN_EMOJIS['arrow_right']

PAGE_SIZE = 10



CUSTOM_ID_QUEST_BOARD_BASE = 'quest_board'

CUSTOM_ID_QUEST_BOARD_QUEST_DETAILS_FACTORY = (
    lambda user_id, page_index, quest_template_id :
    f'{CUSTOM_ID_QUEST_BOARD_BASE}.details.{user_id:x}.{page_index:x}.{quest_template_id:x}'
)
CUSTOM_ID_QUEST_BOARD_QUEST_DETAILS_PATTERN = re_compile(
    f'{re_escape(CUSTOM_ID_QUEST_BOARD_BASE)}\\.details\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)'
)
CUSTOM_ID_QUEST_BOARD_PAGE_INDEX_NAVIGATE_FACTORY = (
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
CUSTOM_ID_QUEST_ACCEPT_FACTORY = (
    lambda user_id, page_index, quest_template_id :
    f'{CUSTOM_ID_QUEST_BOARD_BASE}.accept.{user_id:x}.{page_index:x}.{quest_template_id:x}'
)
CUSTOM_ID_QUEST_ACCEPT_DISABLED = f'{CUSTOM_ID_QUEST_BOARD_BASE}.accept_disabled'

CUSTOM_ID_QUEST_ACCEPT_PATTERN = re_compile(
    f'{re_escape(CUSTOM_ID_QUEST_BOARD_BASE)}\\.accept\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)'
)

CUSTOM_ID_QUEST_BOARD_ITEM_DISABLED = f'{CUSTOM_ID_QUEST_BOARD_BASE}.item_disabled'
CUSTOM_ID_QUEST_BOARD_ITEM_FACTORY = (
    lambda user_id, page_index, quest_template_id, item_id :
    f'{CUSTOM_ID_QUEST_BOARD_BASE}.item.{user_id:x}.{page_index:x}.{quest_template_id:x}.{item_id:x}'
)
CUSTOM_ID_QUEST_BOARD_ITEM_PATTERN = re_compile(
    f'{re_escape(CUSTOM_ID_QUEST_BOARD_BASE)}\\.item\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)'
)



CUSTOM_ID_LINKED_QUEST_BASE = 'linked_quest'

CUSTOM_ID_LINKED_QUEST_DETAILS_FACTORY = (
    lambda user_id, page_index, linked_quest_entry_id :
    f'{CUSTOM_ID_LINKED_QUEST_BASE}.details.{user_id:x}.{page_index:x}.{linked_quest_entry_id:x}'
)
CUSTOM_ID_LINKED_QUEST_DETAILS_PATTERN = re_compile(
    f'{re_escape(CUSTOM_ID_LINKED_QUEST_BASE)}\\.details\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)'
)
CUSTOM_ID_LINKED_QUEST_PAGE_INDEX_NAVIGATE_FACTORY = (
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
CUSTOM_ID_LINKED_QUEST_SUBMIT_FACTORY = (
    lambda user_id, page_index, linked_quest_entry_id : 
    f'{CUSTOM_ID_LINKED_QUEST_BASE}.submit.{user_id:x}.{page_index:x}.{linked_quest_entry_id:x}'
)
CUSTOM_ID_LINKED_QUEST_SUBMIT_PATTERN = re_compile(
    f'{re_escape(CUSTOM_ID_LINKED_QUEST_BASE)}\\.submit\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)'
)
CUSTOM_ID_LINKED_QUEST_ABANDON_FACTORY = (
    lambda user_id, page_index, linked_quest_entry_id :
    f'{CUSTOM_ID_LINKED_QUEST_BASE}.abandon.{user_id:x}.{page_index}.{linked_quest_entry_id:x}'
)
CUSTOM_ID_LINKED_QUEST_ABANDON_PATTERN = re_compile(
    f'{re_escape(CUSTOM_ID_LINKED_QUEST_BASE)}\\.abandon\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)'
)

CUSTOM_ID_LINKED_QUEST_ITEM_DISABLED = f'{CUSTOM_ID_LINKED_QUEST_BASE}.item_disabled'
CUSTOM_ID_LINKED_QUEST_ITEM_FACTORY = (
    lambda user_id, page_index, linked_quest_entry_id, item_id :
    f'{CUSTOM_ID_LINKED_QUEST_BASE}.item.{user_id:x}.{page_index:x}.{linked_quest_entry_id:x}.{item_id:x}'
)
CUSTOM_ID_LINKED_QUEST_ITEM_PATTERN = re_compile(
    f'{re_escape(CUSTOM_ID_LINKED_QUEST_BASE)}\\.item\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)'
)
