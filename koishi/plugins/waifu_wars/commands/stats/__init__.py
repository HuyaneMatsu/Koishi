__all__ = ('STATS_COMMAND',)

from .....bots import FEATURE_CLIENTS

from .show import *
from .upgrade import *


STATS_COMMAND = FEATURE_CLIENTS.interactions(
    None,
    name = 'stats',
    description = 'wanna know you waifu stats?',
    is_global = True,
)

STATS_COMMAND.interactions(command_show, name = 'show')
STATS_COMMAND.interactions(command_upgrade, name = 'upgrade')
