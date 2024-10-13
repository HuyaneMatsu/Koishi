__all__ = ()

from os import symlink as create_link, unlink as remove_link
from os.path import islink as is_link, join as join_paths

from .constants import PATHS_TO_LINK, SOURCE_PATH


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
