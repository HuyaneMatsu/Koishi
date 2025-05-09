__all__ = (
    'CUSTOM_ID_RELATIONSHIP_DIVORCES_DECREMENT_PURCHASE_CANCEL_SELF',
    'CUSTOM_ID_RELATIONSHIP_DIVORCES_DECREMENT_PURCHASE_CONFIRM_SELF',
    'CUSTOM_ID_RELATIONSHIP_DIVORCES_DECREMENT_PURCHASE_CONFIRM_OTHER_PATTERN',
    'CUSTOM_ID_RELATIONSHIP_DIVORCES_DECREMENT_PURCHASE_CANCEL_OTHER_PATTERN',
    'CUSTOM_ID_RELATIONSHIP_DIVORCES_DECREMENT_PURCHASE_INVOKE_OTHER_PATTERN',
    'CUSTOM_ID_RELATIONSHIP_DIVORCES_DECREMENT_PURCHASE_INVOKE_SELF',
)

from re import compile as re_compile, escape as re_escape

from hata import Emoji


EMOJI_YES = Emoji.precreate(990558169963049041)
EMOJI_NO = Emoji.precreate(994540311990784041)


CUSTOM_ID_RELATIONSHIP_DIVORCES_DECREMENT_PURCHASE_BASE = 'user_balance.relationship_divorces.decrement'

# invoke
CUSTOM_ID_RELATIONSHIP_DIVORCES_DECREMENT_PURCHASE_INVOKE_SELF = (
    f'{CUSTOM_ID_RELATIONSHIP_DIVORCES_DECREMENT_PURCHASE_BASE}.invoke.self'
)
CUSTOM_ID_RELATIONSHIP_DIVORCES_DECREMENT_PURCHASE_INVOKE_OTHER_BUILDER = (
    lambda user_id: f'{CUSTOM_ID_RELATIONSHIP_DIVORCES_DECREMENT_PURCHASE_BASE}.invoke.other.{user_id:x}'
)
CUSTOM_ID_RELATIONSHIP_DIVORCES_DECREMENT_PURCHASE_INVOKE_OTHER_PATTERN = re_compile(
    f'{re_escape(CUSTOM_ID_RELATIONSHIP_DIVORCES_DECREMENT_PURCHASE_BASE)}\\.invoke\\.other\\.([0-9a-f]+)'
)

# confirm
CUSTOM_ID_RELATIONSHIP_DIVORCES_DECREMENT_PURCHASE_CONFIRM_SELF = (
    f'{CUSTOM_ID_RELATIONSHIP_DIVORCES_DECREMENT_PURCHASE_BASE}.confirm.self'
)
CUSTOM_ID_RELATIONSHIP_DIVORCES_DECREMENT_PURCHASE_CONFIRM_OTHER_BUILDER = (
    lambda user_id: f'{CUSTOM_ID_RELATIONSHIP_DIVORCES_DECREMENT_PURCHASE_BASE}.confirm.other.{user_id:x}'
)
CUSTOM_ID_RELATIONSHIP_DIVORCES_DECREMENT_PURCHASE_CONFIRM_OTHER_PATTERN = re_compile(
    f'{re_escape(CUSTOM_ID_RELATIONSHIP_DIVORCES_DECREMENT_PURCHASE_BASE)}\\.confirm\\.other\\.([0-9a-f]+)'
)

# cancel
CUSTOM_ID_RELATIONSHIP_DIVORCES_DECREMENT_PURCHASE_CANCEL_SELF = (
    f'{CUSTOM_ID_RELATIONSHIP_DIVORCES_DECREMENT_PURCHASE_BASE}.cancel.self'
)
CUSTOM_ID_RELATIONSHIP_DIVORCES_DECREMENT_PURCHASE_CANCEL_OTHER_BUILDER = (
    lambda user_id: f'{CUSTOM_ID_RELATIONSHIP_DIVORCES_DECREMENT_PURCHASE_BASE}.cancel.other.{user_id:x}'
)
CUSTOM_ID_RELATIONSHIP_DIVORCES_DECREMENT_PURCHASE_CANCEL_OTHER_PATTERN = re_compile(
    f'{re_escape(CUSTOM_ID_RELATIONSHIP_DIVORCES_DECREMENT_PURCHASE_BASE)}\\.cancel\\.other\\.([0-9a-f]+)'
)
