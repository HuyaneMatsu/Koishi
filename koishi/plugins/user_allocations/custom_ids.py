__all__ = ()

from re import compile as re_compile


USER_ALLOCATIONS_CUSTOM_ID_VIEW_PAGE_BUILDER = (
    lambda user_id, page_index: f'allocations.view.{user_id:x}.{page_index:x}'
)
USER_ALLOCATIONS_CUSTOM_ID_VIEW_PAGE_PATTERN = re_compile('allocations\\.view\\.([0-9a-z]+)\\.([0-9a-z]+)')

USER_ALLOCATIONS_CUSTOM_ID_VIEW_PAGE_INDEX_DECREMENT_DISABLED = 'allocations.view.disabled.d'
USER_ALLOCATIONS_CUSTOM_ID_VIEW_PAGE_INDEX_INCREMENT_DISABLED = 'allocations.view.disabled.i'

USER_ALLOCATIONS_CUSTOM_ID_DETAILS_BUILDER = (
    lambda user_id, page_index, allocation_feature_id, allocation_session_id:
    f'allocations.details.{user_id:x}.{page_index:x}.{allocation_feature_id:x}.{allocation_session_id:x}'
)

USER_ALLOCATIONS_CUSTOM_ID_DETAILS_PATTERN = re_compile(
    'allocations\\.details\\.([0-9a-z]+)\\.([0-9a-z]+)\\.([0-9a-z]+)\\.([0-9a-z]+)'
)

USER_ALLOCATION_CUSTOM_ID_LINK_DISABLED = 'allocations.link.disabled'
