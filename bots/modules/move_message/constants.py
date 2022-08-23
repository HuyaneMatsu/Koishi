__all__ = ()

from hata import Guild, Role

from bot_utils.constants import GUILD__SUPPORT


GUILD__KOISHI_CLAN = Guild.precreate(866746184990720020)
ROLE__MEDIA_SORTER = Role.precreate(1010087924773167124)

ALLOWED_GUILDS = [GUILD__KOISHI_CLAN, GUILD__SUPPORT]
