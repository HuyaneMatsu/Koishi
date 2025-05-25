__all__ = (
    'CUSTOM_ID_STAT_UPGRADE_PURCHASE_CANCEL_OTHER_PATTERN', 'CUSTOM_ID_STAT_UPGRADE_PURCHASE_CANCEL_SELF_PATTERN',
    'CUSTOM_ID_STAT_UPGRADE_PURCHASE_CONFIRM_OTHER_PATTERN', 'CUSTOM_ID_STAT_UPGRADE_PURCHASE_CONFIRM_SELF_PATTERN'
)

from re import compile as re_compile, escape as re_escape

from hata import Emoji


EMOJI_YES = Emoji.precreate(990558169963049041)
EMOJI_NO = Emoji.precreate(994540311990784041)


CUSTOM_ID_STAT_UPGRADE_PURCHASE_BASE = 'stats.upgrade'


# confirm
CUSTOM_ID_STAT_UPGRADE_PURCHASE_CONFIRM_SELF_BUILDER = (
    lambda stat_index : f'{CUSTOM_ID_STAT_UPGRADE_PURCHASE_BASE}.confirm.self.{stat_index:x}'
)
CUSTOM_ID_STAT_UPGRADE_PURCHASE_CONFIRM_SELF_PATTERN = re_compile(
    f'{re_escape(CUSTOM_ID_STAT_UPGRADE_PURCHASE_BASE)}\\.confirm\\.self\\.([0-9a-f]+)'
)

CUSTOM_ID_STAT_UPGRADE_PURCHASE_CONFIRM_OTHER_BUILDER = (
    lambda user_id, stat_index: f'{CUSTOM_ID_STAT_UPGRADE_PURCHASE_BASE}.confirm.other.{user_id:x}.{stat_index:x}'
)
CUSTOM_ID_STAT_UPGRADE_PURCHASE_CONFIRM_OTHER_PATTERN = re_compile(
    f'{re_escape(CUSTOM_ID_STAT_UPGRADE_PURCHASE_BASE)}\\.confirm\\.other\\.([0-9a-f]+)\\.([0-9a-f]+)'
)

# cancel
CUSTOM_ID_STAT_UPGRADE_PURCHASE_CANCEL_SELF_BUILDER = (
    lambda stat_index : f'{CUSTOM_ID_STAT_UPGRADE_PURCHASE_BASE}.cancel.self.{stat_index:x}'
)
CUSTOM_ID_STAT_UPGRADE_PURCHASE_CANCEL_SELF_PATTERN = re_compile(
    f'{re_escape(CUSTOM_ID_STAT_UPGRADE_PURCHASE_BASE)}\\.cancel\\.self\\.([0-9a-f]+)'
)

CUSTOM_ID_STAT_UPGRADE_PURCHASE_CANCEL_OTHER_BUILDER = (
    lambda user_id, stat_index : f'{CUSTOM_ID_STAT_UPGRADE_PURCHASE_BASE}.cancel.other.{user_id:x}.{stat_index:x}'
)
CUSTOM_ID_STAT_UPGRADE_PURCHASE_CANCEL_OTHER_PATTERN = re_compile(
    f'{re_escape(CUSTOM_ID_STAT_UPGRADE_PURCHASE_BASE)}\\.cancel\\.other\\.([0-9a-f]+)\\.([0-9a-f]+)'
)
