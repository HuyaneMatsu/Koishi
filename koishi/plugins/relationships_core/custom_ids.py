__all__ = ('CUSTOM_ID_RELATIONSHIPS_REQUEST_DETAILS_BUILDER', 'CUSTOM_ID_RELATIONSHIPS_REQUEST_DETAILS_RP')

from re import compile as re_compile


CUSTOM_ID_RELATIONSHIPS_REQUEST_DETAILS_BUILDER = (
    lambda user_id, outgoing, page_index, entry_id :
    f'relationships_request.details.{user_id:x}.{outgoing:x}.{page_index:x}.{entry_id:x}'
)
CUSTOM_ID_RELATIONSHIPS_REQUEST_DETAILS_RP = re_compile(
    'relationships_request\\.details\\.([0-9a-f]+)\\.([01])\\.([0-9a-f]+)\\.([0-9a-f]+)'
)
