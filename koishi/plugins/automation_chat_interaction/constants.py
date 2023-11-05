__all__ = ()

from os.path import dirname as get_directory_path, join as join_paths

from hata import Guild

from ...bot_utils.constants import GUILD__SUPPORT 


GUILD__KOISHI_CLAN = Guild.precreate(866746184990720020)


PATH_ASSETS = join_paths(get_directory_path(__file__), 'assets')
ALLOWED_GUILD_IDS = (GUILD__SUPPORT.id, GUILD__KOISHI_CLAN.id)
TRIGGER_CHANCE = 0.20
