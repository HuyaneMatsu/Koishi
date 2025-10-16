__all__ = ()

from ...bots import FEATURE_CLIENTS

from .text_wall import command_test_wall


IMAGINARY_FRIEND_COMMANDS = FEATURE_CLIENTS.interactions(
    None,
    integration_types = ['guild_install', 'user_install'],
    is_global = True,
    name = 'imaginary-friend',
    description = 'Imaginary commands.'
)


IMAGINARY_FRIEND_COMMANDS.interactions(command_test_wall, name = 'text_wall',)
