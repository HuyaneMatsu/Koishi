__all__ = ('STATS_COMMAND',)

from .....bots import SLASH_CLIENT

from .show import *
from .upgrade import *


STATS_COMMAND = SLASH_CLIENT.interactions(
    None,
    name = 'stats',
    description = 'wanna know you waifu stats?',
    is_global = True,
)

STATS_COMMAND.interactions(command_show, name = 'show')
STATS_COMMAND.interactions(command_upgrade, name = 'upgrade')
