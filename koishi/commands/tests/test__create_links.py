from os.path import join as join_paths

import vampytest

from ..link import _create_links


def test__create_links():
    """
    Tests whether ``_create_links`` works as intended.
    """
    source_path = '/projects/koishi'
    directory_path = '/project/koishi'
    
    paths_to_link = (
        (
            ('plugins', 'pudding', 'assets'),
            'pudding',
        ),
        (
            ('plugins', 'eater', 'assets'),
            'eater',
        ),
    )
    
    created_links = []
    
    
    def mock_create_link(source, target):
        nonlocal created_links
        created_links.append((source, target))
    
    
    mocked = vampytest.mock_globals(
        _create_links,
        SOURCE_PATH = source_path,
        PATHS_TO_LINK = paths_to_link,
        create_link = mock_create_link,
    )
    
    mocked(directory_path)
    
    vampytest.assert_eq(
        created_links,
        [
            (join_paths(source_path, *source_path_parts), join_paths(directory_path, target_name))
            for source_path_parts, target_name in paths_to_link
        ],
    )
