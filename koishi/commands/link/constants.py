__all__ = ()

from os.path import dirname as get_parent_directory_path


PATHS_TO_LINK = (
    (
        ('plugins', 'automation_chat_interaction', 'assets'),
        'automation_chat_interaction',
    ),
    (
        ('plugins', 'automation_logging', 'assets'),
        'automation_logging',
    ),
    (
        ('plugins', 'automation_welcome', 'assets'),
        'automation_welcome',
    ),
    (
        ('plugins', 'daily_reminder', 'assets'),
        'daily_reminder',
    ),
    (
        ('plugins', 'image_commands_actions', 'assets'),
        'image_commands_actions',
    ),
    (
        ('plugins', 'memes', 'assets'),
        'memes',
    ),
    (
        ('plugins', 'moderation', 'assets'),
        'moderation',
    ),
    (
        ('plugins', 'sex', 'assets'),
        'sex',
    ),
    (
        ('plugins', 'error_messages', 'assets'),
        'error_messages',
    ),
    (
        ('plugins', 'hyaku_percent_orange_juice', 'assets'),
        'hyaku_percent_orange_juice',
    ),
)


SOURCE_PATH = get_parent_directory_path(get_parent_directory_path(get_parent_directory_path((__file__))))
TARGET_DIRECTORY = 'koishi_assets'
