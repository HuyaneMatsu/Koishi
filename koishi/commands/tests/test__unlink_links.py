from os.path import join as join_paths

import vampytest

from ..link import _unlink_links


def test__unlink_links():
    """
    Tests whether ``_unlink_links`` works as intended.
    """
    directory_path = '/root/koishi'
    names = ['hey', 'mister', 'sister']
    removed_links = []
    
    def mock_remove_link(path):
        nonlocal removed_links
        removed_links.append(path)
    
    
    mocked = vampytest.mock_globals(
        _unlink_links,
        remove_link = mock_remove_link,
    )
    
    mocked(directory_path, names)
    
    vampytest.assert_eq(
        removed_links,
        [join_paths(directory_path, name) for name in names],
    )
    
    
