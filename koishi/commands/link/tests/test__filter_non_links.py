import vampytest

from os.path import join as join_paths

from ..helpers import _filter_non_links


def test__filter_non_links__has_non_link():
    """
    Tests whether ``_filter_non_links`` works as intended.
    
    Case: has non links.
    """
    directory_path = '/root/koishi'
    names = ['hey', 'mister', 'sister']
    non_links = ['hey', 'mister']
    
    def mock_is_link(input_value):
        nonlocal directory_path
        nonlocal non_links
        
        if input_value in (join_paths(directory_path, non_link) for non_link in non_links):
            return False
        
        return True
    
    mocked = vampytest.mock_globals(
        _filter_non_links,
        is_link = mock_is_link,
    )
    output = mocked(directory_path, names)
    vampytest.assert_eq(output, non_links)
    


def test__filter_non_links__only_link():
    """
    Tests whether ``_filter_non_links`` works as intended.
    
    Case: only links.
    """
    directory_path = '/root/koishi'
    names = ['hey', 'mister', 'sister']
    
    def mock_is_link(input_value):
        return True
    
    mocked = vampytest.mock_globals(
        _filter_non_links,
        is_link = mock_is_link,
    )
    
    output = mocked(directory_path, names)
    vampytest.assert_is(output, None)
    
