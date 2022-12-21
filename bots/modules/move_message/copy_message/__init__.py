from .about import *
from .action import *
from .list_channels import *

__all__ = (
    *about.__all__,
    *action.__all__,
    *list_channels.__all__,
)

# Construct command

from hata import Client, Permission

from ..constants import ALLOWED_GUILDS

from .about import copy_message_about
from .list_channels import copy_message_list_channels


SLASH_CLIENT: Client


COPY_MESSAGE_COMMANDS = SLASH_CLIENT.interactions(
    None,
    guild = ALLOWED_GUILDS,
    name = 'copy-message',
    description = 'Utility for copying messages over channels.',
    required_permissions = Permission().update_by_keys(manage_messages = True),
)

COPY_MESSAGE_COMMANDS.interactions(copy_message_about, name = 'about')
COPY_MESSAGE_COMMANDS.interactions(copy_message_list_channels, name = 'list-channels')
