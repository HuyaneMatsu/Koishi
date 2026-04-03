__all__ = ()

import re

from hata import ID_RP, Permission

from collections import namedtuple as NamedTuple


REASON_ALLOWED_LENGTH_MAX = 400


WordConfig = NamedTuple('WordConfig', ('permission', 'name', 'to_be', 'connector'))


WORD_CONFIG__BAN = WordConfig(
    'ban users',
    'ban',
    'banned',
    'from',
)

WORD_CONFIG__KICK = WordConfig(
    'kick users',
    'kick',
    'kicked',
    'from',
)

WORD_CONFIG__MUTE = WordConfig(
    'moderate users',
    'mute',
    'muted',
    'in',
)

WORD_CONFIG__TOP_LIST = WordConfig(
    'ban, kick and moderate',
    'top-list',
    'top-listed',
    'in',
)

WORD_CONFIG__UN_BAN = WordConfig(
    'ban users',
    'un-ban',
    'un-banned',
    'from',
)

WORD_CONFIG__UN_MUTE = WordConfig(
    'moderate users',
    'un-mute',
    'un-muted',
    'in',
)

WORD_CONFIG__REGRET_UN_BAN = WordConfig(
    'ban users',
    'regret un-ban',
    'regret un-banned',
    'in',
)

WORD_CONFIG__REGRET_UN_KICK = WordConfig(
    'ban users',
    'regret un-kick',
    'regret un-kicked',
    'in',
)


PERMISSIONS__BAN = Permission().update_by_keys(ban_users = True)
PERMISSIONS__KICK = Permission().update_by_keys(kick_users = True)
PERMISSIONS__MUTE = Permission().update_by_keys(moderate_users = True)


REASON_RP = re.compile(f'[\\s\\S]*\\[{ID_RP.pattern}\\]', re.M | re.U)
