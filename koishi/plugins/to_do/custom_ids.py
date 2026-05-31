__all__ = ()

from re import compile as re_compile
from base64 import b64encode as base64_encode

CUSTOM_ID_NAME = 'name'
CUSTOM_ID_DESCRIPTION = 'description'


CUSTOM_ID_TO_DO_CREATE = 'to_do.create'

CUSTOM_ID_TO_DO_DELETE_BUILDER = lambda entry_id : f'to_do.delete.{entry_id:x}'
CUSTOM_ID_TO_DO_EDIT_BUILDER = lambda entry_id : f'to_do.edit.{entry_id:x}'

CUSTOM_ID_TO_DO_EDIT_PATTERN = re_compile('to_do\\.edit\\.([0-9a-f]+)')
CUSTOM_ID_TO_DO_DELETE_PATTERN = re_compile('to_do\\.delete\\.([0-9a-f]+)')


CUSTOM_ID_TO_DO_LISTING_CLOSE = 'to_do_listing.close'
CUSTOM_ID_TO_DO_LISTING_PAGE_BUILDER = (
    lambda page_index, query :
    f'to_do_listing.page.{page_index:x}.{"" if query is None else base64_encode(query.encode()).decode()}'
)
CUSTOM_ID_TO_DO_LISTING_PAGE_DECREMENT_DISABLED = 'to_do_listing.page_decrement_disabled'
CUSTOM_ID_TO_DO_LISTING_PAGE_INCREMENT_DISABLED = 'to_do_listing.page_increment_disabled'

CUSTOM_ID_TO_DO_LISTING_PAGE_PATTERN = re_compile('to_do_listing\\.page\\.([0-9a-f]+)\\.([A-Za-z0-9\\+\\/\\=]+)?')
