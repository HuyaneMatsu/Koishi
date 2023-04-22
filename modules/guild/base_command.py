__all__ = ()

from bots import SLASH_CLIENT


GUILD_COMMANDS = SLASH_CLIENT.interactions(
    None,
    name = 'guild',
    description = 'guild utility commands',
    is_global = True,
    allow_in_dm = False,
)
