__all__ = ()

from os import listdir as list_directory, mkdir as create_directory, symlink as create_link, unlink as remove_link
from os.path import (
    dirname as get_parent_directory_path, exists, isdir as is_directory, islink as is_link, join as join_paths
)

from hata.main import register


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
)


SOURCE_PATH = get_parent_directory_path(get_parent_directory_path(__file__))
TARGET_DIRECTORY = 'koishi_assets'


def _filter_non_links(directory_path, names):
    """
    Filters out the names from the directory that arent links.
    
    Parameters
    ----------
    directory_path : `str`
        Path to the directory.
    names : `list<str>`
        The name of the nodes in the directory.
    
    Returns
    -------
    non_links : `None | list<str>`
    """
    non_links = None
    
    for name in names:
        if is_link(join_paths(directory_path, name)):
            continue
        
        if non_links is None:
            non_links = []
        
        non_links.append(name)
    
    return non_links


def _build_non_links_error(directory_path, non_links):
    """
    Builds error message for case when non-all nodes in a directory are links.
    
    Parameters
    ----------
    directory_path : `str`
        Path to the directory.
    names : `list<str>`
        The name of non-link nodes.
    
    Returns
    -------
    error_message : `str`
    """
    output_parts = ['Directory: ', repr(directory_path), ' contains not only links:']
    
    for name in non_links:
        output_parts.append('\n- ')
        output_parts.append(repr(name))
    
    return ''.join(output_parts)


def _unlink_links(directory_path, names):
    """
    Unlinks the given links in the directory.
    
    Parameters
    ----------
    directory_path : `str`
        Path to the directory.
    names : `list<str>`
        The name of the nodes in the directory.
    """
    for name in names:
        remove_link(join_paths(directory_path, name))


def _create_links(directory_path):
    """
    Creates link into the directory based on the pre-definition.
    
    
    Parameters
    ----------
    directory_path : `str`
        Path to the directory.
    """
    for source_path_parts, target_name in PATHS_TO_LINK:
        create_link(join_paths(SOURCE_PATH, *source_path_parts), join_paths(directory_path, target_name))


@register
def link_assets(
    location : str,
):
    """
    Links koishi's assets (only images) to the given location.
    """
    if not is_directory(location):
        return f'Directory: {location!r} does not exists.'
    
    directory_path = join_paths(location, TARGET_DIRECTORY)
    if exists(directory_path):
        if not is_directory(directory_path):
            return (
                f'The directory\'s path where the assets would be linked already exists but is not a directory.\n'
                f'path = {directory_path!r}.'
            )
        
        names = list_directory(directory_path)
        non_links = _filter_non_links(directory_path, names)
        if (non_links is not None):
            return _build_non_links_error(directory_path, non_links)
        
        _unlink_links(directory_path, names)
        
    else:
        create_directory(directory_path)
    
    _create_links(directory_path)
    return 'Links created.'
