from .constants import *
from .avatar import *
from .icon_helpers import *
from .info import *
from .info_helpers import *

__all__ = (
    *constants.__all__,
    *avatar.__all__,
    *icon_helpers.__all__,
    *info.__all__,
    *info_helpers.__all__,
)


# Construct command

from ...bots import SLASH_CLIENT

from .info import user_info_command
from .avatar import user_avatar_command


USER_COMMANDS = SLASH_CLIENT.interactions(
    None,
    name = 'user',
    description = 'User commands',
    is_global = True,
)

USER_COMMANDS.interactions(user_avatar_command, name = 'avatar')
USER_COMMANDS.interactions(user_info_command, name = 'info')
