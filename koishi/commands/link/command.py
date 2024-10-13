__all__ = ()

from os import listdir as list_directory, mkdir as create_directory
from os.path import exists, isdir as is_directory, join as join_paths

from hata.main import register

from .constants import TARGET_DIRECTORY
from .helpers import _build_non_links_error, _create_links, _filter_non_links, _unlink_links


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
