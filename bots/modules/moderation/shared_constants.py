__all__ = ()

from hata import Permission

from collections import namedtuple as NamedTuple


WordConfig = NamedTuple('WordConfig', ('permission', 'name', 'to_be', 'connector'))


WORD_CONFIG__BAN = WordConfig(
    'ban',
    'ban',
    'banned',
    'from',
)

WORD_CONFIG__KICK = WordConfig(
    'kick',
    'kick',
    'kicked',
    'from',
)

WORD_CONFIG__MUTE = WordConfig(
    'moderate',
    'mute',
    'muted',
    'in',
)

WORD_CONFIG__UN_BAN = WordConfig(
    'ban',
    'un-ban',
    'un-banned',
    'from',
)

WORD_CONFIG__UN_MUTE = WordConfig(
    'moderate',
    'un-mute',
    'un-muted',
    'in',
)


WORD_CONFIG__REGRET_UN_BAN = WordConfig(
    'ban',
    'regret un-ban',
    'regret un-banned',
    'in',
)

WORD_CONFIG__REGRET_UN_KICK = WordConfig(
    'ban',
    'regret un-kick',
    'regret un-kicked',
    'in',
)

PERMISSIONS__BAN = Permission().update_by_keys(ban_users = True)
PERMISSIONS__KICK = Permission().update_by_keys(kick_users = True)
PERMISSIONS__MUTE = Permission().update_by_keys(moderate_users = True)
