from .constants import *
from .icon import *
from .icon_helpers import *
from .info import *
from .info_helpers import *
from .welcome_screen import *


__all__ = (
    *constants.__all__,
    *icon.__all__,
    *icon_helpers.__all__,
    *info.__all__,
    *info_helpers.__all__,
    *welcome_screen.__all__,
)

# Construct command

from hata import Client

from. icon import guild_icon_command
from .info import guild_info_command
from .welcome_screen import welcome_screen_command

SLASH_CLIENT: Client

GUILD_COMMANDS = SLASH_CLIENT.interactions(
    None,
    name = 'guild',
    description = 'guild utility commands',
    is_global = True,
    allow_in_dm = False,
)

GUILD_COMMANDS.interactions(guild_icon_command, name = 'icon')
GUILD_COMMANDS.interactions(guild_info_command, name = 'info')
GUILD_COMMANDS.interactions(welcome_screen_command, name = 'welcome_screen')
