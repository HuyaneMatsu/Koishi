__all__ = ()

from re import compile as re_compile


CUSTOM_ID_RELATIONSHIPS_BREAK_UP_BUILDER = lambda user_id : f'relationships.break_up.{user_id:x}'
CUSTOM_ID_RELATIONSHIPS_BREAK_UP_RP = re_compile('relationships\\.break_up\\.([0-9a-f]+)')


CUSTOM_ID_RELATIONSHIPS_REQUEST_VIEW_BUILDER = (
    lambda user_id, outgoing, page_index : f'relationships_request.view.{user_id:x}.{outgoing:x}.{page_index:x}'
)
CUSTOM_ID_RELATIONSHIPS_REQUEST_VIEW_RP = re_compile(
    'relationships_request\\.view\\.([0-9a-f]+)\\.([01])\\.([0-9a-f]+)'
)
CUSTOM_ID_RELATIONSHIPS_REQUEST_VIEW_DECREMENT_DISABLED = 'relationships_request.view.decrement.disabled'
CUSTOM_ID_RELATIONSHIPS_REQUEST_VIEW_INCREMENT_DISABLED = 'relationships_request.view.increment.disabled'

CUSTOM_ID_RELATIONSHIPS_REQUEST_CLOSE_BUILDER = (
    lambda user_id : f'relationships_request.close.{user_id:x}'
)
CUSTOM_ID_RELATIONSHIPS_REQUEST_VIEW_CLOSE_RP = re_compile(
    'relationships_request\\.close\\.([0-9a-f]+)'
)

CUSTOM_ID_RELATIONSHIP_REQUEST_ACCEPT_BUILDER = (
    lambda user_id, outgoing, page_index, entry_id :
    f'relationships_request.accept.{user_id:x}.{outgoing:x}.{page_index:x}.{entry_id:x}'
)
CUSTOM_ID_RELATIONSHIP_REQUEST_ACCEPT_RP = re_compile(
    'relationships_request\\.accept\\.([0-9a-f]+)\\.([01])\\.([0-9a-f]+)\\.([0-9a-f]+)'
)

CUSTOM_ID_RELATIONSHIP_REQUEST_REJECT_BUILDER = (
    lambda user_id, outgoing, page_index, entry_id :
    f'relationships_request.reject.{user_id:x}.{outgoing:x}.{page_index:x}.{entry_id:x}'
)
CUSTOM_ID_RELATIONSHIP_REQUEST_REJECT_RP = re_compile(
    'relationships_request\\.reject\\.([0-9a-f]+)\\.([01])\\.([0-9a-f]+)\\.([0-9a-f]+)'
)

CUSTOM_ID_RELATIONSHIP_REQUEST_CANCEL_BUILDER = (
    lambda user_id, outgoing, page_index, entry_id :
    f'relationships_request.cancel.{user_id:x}.{outgoing:x}.{page_index:x}.{entry_id:x}'
)
CUSTOM_ID_RELATIONSHIP_REQUEST_CANCEL_RP = re_compile(
    'relationships_request\\.cancel\\.([0-9a-f]+)\\.([01])\\.([0-9a-f]+)\\.([0-9a-f]+)'
)


CUSTOM_ID_RELATIONSHIPS_VIEW_BUILDER = (
    lambda source_user_id, target_user_id, relationship_listing_mode, page_index :
    f'relationships.view.{source_user_id:x}.{target_user_id:x}.{relationship_listing_mode:x}.{page_index:x}'
)
CUSTOM_ID_RELATIONSHIPS_VIEW_RP = re_compile(
    'relationships\\.view\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)'
)
CUSTOM_ID_RELATIONSHIPS_VIEW_DECREMENT_DISABLED = 'relationships.view.decrement.disabled'
CUSTOM_ID_RELATIONSHIPS_VIEW_INCREMENT_DISABLED = 'relationships.view.increment.disabled'

CUSTOM_ID_RELATIONSHIPS_CLOSE_BUILDER = (
    lambda source_user_id : f'relationships.close.{source_user_id:x}'
)
CUSTOM_ID_RELATIONSHIPS_VIEW_CLOSE_RP = re_compile(
    'relationships\\.close\\.([0-9a-f]+)'
)
CUSTOM_ID_RELATIONSHIPS_MODE_BUILDER = (
    lambda source_user_id, target_user_id, page_index :
    f'relationships.mode.{source_user_id:x}.{target_user_id:x}.{page_index:x}'
)
CUSTOM_ID_RELATIONSHIPS_MODE_RP = re_compile(
    'relationships\\.mode\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)'
)
