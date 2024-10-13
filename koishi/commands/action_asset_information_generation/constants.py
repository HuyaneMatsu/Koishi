__all__ = ()

from os.path import dirname as get_parent_directory_path


BREAK_LINE = '\n---\n\n'
SOURCE_PATH = get_parent_directory_path(get_parent_directory_path(get_parent_directory_path(__file__)))
