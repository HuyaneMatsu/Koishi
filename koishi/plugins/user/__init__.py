from .constants import *
from .avatar import *
from .icon_helpers import *
from .info import *


__all__ = (
    *constants.__all__,
    *avatar.__all__,
    *icon_helpers.__all__,
    *info.__all__,
)


# Construct command

from ...bots import FEATURE_CLIENTS

from .info import user_info_command
from .avatar import user_avatar_command


USER_COMMANDS = FEATURE_CLIENTS.interactions(
    None,
    name = 'user',
    description = 'User commands',
    is_global = True,
)

USER_COMMANDS.interactions(user_avatar_command, name = 'avatar')
USER_COMMANDS.interactions(user_info_command, name = 'info')
