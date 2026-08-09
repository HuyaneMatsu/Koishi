__all__ = ()

from re import compile as re_compile


CUSTOM_ID_TOP_LIST_PAGE_INDEX_INCREMENT_DISABLED = 'top_list.page.i.d'
CUSTOM_ID_TOP_LIST_PAGE_INDEX_DECREMENT_DISABLED = 'top_list.page.d.d'

CUSTOM_ID_TOP_LIST_PAGE_INDEX_BUILDER = (
    lambda user_id, top_list_type, page_index : f'top_list.page.{user_id:x}.{top_list_type:x}.{page_index:x}'
)
CUSTOM_ID_TOP_LIST_PAGE_INDEX_PATTERN = re_compile('top_list\\.page\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)')

CUSTOM_ID_TOP_LIST_CLOSE_BUILDER = lambda user_id : f'top_list.close.{user_id:x}'
CUSTOM_ID_TOP_LIST_CLOSE_PATTERN = re_compile('top_list\\.close\\.([0-9a-f]+)')
