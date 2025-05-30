__all__ = (
    'CUSTOM_ID_RELATIONSHIP_DIVORCE_CANCEL_PATTERN', 'CUSTOM_ID_RELATIONSHIP_DIVORCE_CONFIRM_PATTERN',
    'CUSTOM_ID_RELATIONSHIP_PROPOSAL_ACCEPT_PATTERN', 'CUSTOM_ID_RELATIONSHIP_PROPOSAL_REJECT_PATTERN'
)

from collections import OrderedDict
from re import compile as re_compile, escape as re_escape

from hata import Emoji
from scarletio import WeakValueDictionary


RELATIONSHIP_REQUEST_CACHE = WeakValueDictionary()

RELATIONSHIP_REQUEST_CACHE_LISTING = OrderedDict()
RELATIONSHIP_REQUEST_CACHE_LISTING_SIZE_MAX = 100


RELATIONSHIP_CACHE = WeakValueDictionary()

RELATIONSHIP_LISTING_GET_QUERY_TASKS = {}
RELATIONSHIP_LISTING_CACHE = OrderedDict()
RELATIONSHIP_LISTING_CACHE_SIZE_MAX = 100


EMOJI_YES = Emoji.precreate(990558169963049041)
EMOJI_NO = Emoji.precreate(994540311990784041)

CUSTOM_ID_RELATIONSHIP_PROPOSAL_BASE = 'relationship_proposal'

CUSTOM_ID_RELATIONSHIP_PROPOSAL_ACCEPT_BUILDER = (
    lambda source_user_id, target_user_id:
    f'{CUSTOM_ID_RELATIONSHIP_PROPOSAL_BASE}.accept.{source_user_id:x}.{target_user_id:x}'
)
CUSTOM_ID_RELATIONSHIP_PROPOSAL_REJECT_BUILDER = (
    lambda source_user_id, target_user_id:
    f'{CUSTOM_ID_RELATIONSHIP_PROPOSAL_BASE}.reject.{source_user_id:x}.{target_user_id:x}'
)
CUSTOM_ID_RELATIONSHIP_PROPOSAL_ACCEPT_PATTERN = re_compile(
    f'{re_escape(CUSTOM_ID_RELATIONSHIP_PROPOSAL_BASE)}\\.accept\\.([0-9a-f]+)\\.([0-9a-f]+)'
)
CUSTOM_ID_RELATIONSHIP_PROPOSAL_REJECT_PATTERN = re_compile(
    f'{re_escape(CUSTOM_ID_RELATIONSHIP_PROPOSAL_BASE)}\\.reject\\.([0-9a-f]+)\\.([0-9a-f]+)'
)


CUSTOM_ID_RELATIONSHIP_DIVORCE_BASE = 'relationship_divorce'

CUSTOM_ID_RELATIONSHIP_DIVORCE_CONFIRM_BUILDER = (
    lambda source_user_id, target_user_id:
    f'{CUSTOM_ID_RELATIONSHIP_DIVORCE_BASE}.confirm.{source_user_id:x}.{target_user_id:x}'
)
CUSTOM_ID_RELATIONSHIP_DIVORCE_CANCEL_BUILDER = (
    lambda source_user_id, target_user_id:
    f'{CUSTOM_ID_RELATIONSHIP_DIVORCE_BASE}.cancel.{source_user_id:x}.{target_user_id:x}'
)
CUSTOM_ID_RELATIONSHIP_DIVORCE_CONFIRM_PATTERN = re_compile(
    f'{re_escape(CUSTOM_ID_RELATIONSHIP_DIVORCE_BASE)}\\.confirm\\.([0-9a-f]+)\\.([0-9a-f]+)'
)
CUSTOM_ID_RELATIONSHIP_DIVORCE_CANCEL_PATTERN = re_compile(
    f'{re_escape(CUSTOM_ID_RELATIONSHIP_DIVORCE_BASE)}\\.cancel\\.([0-9a-f]+)\\.([0-9a-f]+)'
)
