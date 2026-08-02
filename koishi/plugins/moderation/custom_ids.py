__all__ = ()

from re import compile as re_compile


CUSTOM_ID_REASON = 'reason'
CUSTOM_ID_NOTIFY_USER = 'notify_user'
CUSTOM_ID_DELETE_MESSAGE_DURATION = 'delete_message_duration'
CUSTOM_ID_DURATION = 'duration'
CUSTOM_ID_USERS = 'users'


CUSTOM_ID_MOD_OTHER_BUILDER = lambda action_type, target_id : f'mod.other.{action_type:x}.{target_id:x}'
CUSTOM_ID_MOD_OTHER_PATTERN = re_compile('mod\\.other\\.([0-9a-f]+)\\.([0-9a-f]+)')

CUSTOM_ID_MOD_SELF_BUILDER = lambda action_type : f'mod.self.{action_type:x}'
CUSTOM_ID_MOD_SELF_PATTERN = re_compile('mod\\.self\\.([0-9a-f]+)')

CUSTOM_ID_MOD_TOP_LIST_PAGE_INDEX_DECREMENT_DISABLED = 'mod.top_list.page.disabled.d'
CUSTOM_ID_MOD_TOP_LIST_PAGE_INDEX_INCREMENT_DISABLED = 'mod.top_list.page.disabled.i'
CUSTOM_ID_MOD_TOP_LIST_PAGE_INDEX_BUILDER = (
    lambda user_id, page_index, sort_by, days : f'mod.top_list.page.{user_id:x}.{page_index:x}.{sort_by:x}.{days:x}'
)
CUSTOM_ID_MOD_TOP_LIST_PAGE_INDEX_PATTERN = re_compile(
    f'mod\\.top_list\\.page\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)'
)
CUSTOM_ID_MOD_TOP_LIST_CLOSE_BUILDER = lambda user_id : f'mod.top_list.close.{user_id:x}'
CUSTOM_ID_MOD_TOP_LIST_CLOSE_PATTERN = re_compile(f'mod\\.top_list\\.close\\.([0-9a-f]+)')
