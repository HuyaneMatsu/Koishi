__all__ = ()

from os.path import dirname as get_parent_directory_path, join as join_paths
from re import compile as re_compile


ASSET_NAME_PATTERN = re_compile('([a-z\\-_]+)\\-(\\d{4})(?:\\-([a-z\\-_]+))?\\.([a-z0-9]+)')
SOURCE_PATH = get_parent_directory_path(get_parent_directory_path(get_parent_directory_path(__file__)))
ASSETS_DIRECTORY = join_paths(SOURCE_PATH, 'plugins', 'image_commands_actions', 'assets')
EXTENSIONS_TO_CONVERT = ('jpeg', 'jpg', 'webp')
