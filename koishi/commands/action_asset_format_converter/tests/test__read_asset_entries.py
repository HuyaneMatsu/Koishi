from os.path import join as join_paths

import vampytest

from ..asset_entry import AssetEntry
from ..grouping import read_asset_entries


def test__read_asset_entries():
    """
    Tests whether ``read_asset_entries`` works as intended.
    """
    notify_called = 0
    directory = '/orin/assets'
    
    
    def mock_notify(input_message):
        nonlocal notify_called
        notify_called += 1
    
    
    def mock_list_directory(input_directory):
        nonlocal directory
        vampytest.assert_eq(input_directory, directory)
        
        return [
            'hey-0000.jpg',
            'hey-0001.jpg',
            'mister-0000.png',
            'sister-0001.mp4',
            'sister-self_feed-0000.mp4',
            'README.md',
            'ayaya',
        ]
    
    
    def mock_is_file(path):
        nonlocal directory
        return (
            path in
            (
                join_paths(directory, 'hey-0000.jpg'),
                join_paths(directory, 'hey-0001.jpg'),
                join_paths(directory, 'mister-0000.png'),
                join_paths(directory, 'sister-0001.mp4'),
                join_paths(directory, 'sister-self_feed-0000.mp4'),
                join_paths(directory, 'README.md'),
            ),
        )
    
    
    mocked = vampytest.mock_globals(
        read_asset_entries,
        notify = mock_notify,
        list_directory = mock_list_directory,
        is_file = mock_is_file,
    )
    
    output = mocked(directory)
    vampytest.assert_instance(output, list)
    vampytest.assert_eq(
        output,
        [
            AssetEntry('hey', 0, None, 'jpg'),
            AssetEntry('hey', 1, None, 'jpg'),
            AssetEntry('mister', 0, None, 'png'),
            AssetEntry('sister', 1, None, 'mp4'),
            AssetEntry('sister-self_feed', 0, None, 'mp4'),
        ]
    )
    
    vampytest.assert_eq(notify_called, 2)
