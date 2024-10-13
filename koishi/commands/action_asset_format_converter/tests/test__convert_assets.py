from os.path import join as join_paths

import vampytest

from ..asset_entry import AssetEntry
from ..asset_group import AssetGroup
from ..grouping import convert_assets



def test__convert_assets():
    """
    Tests whether ``convert_assets`` works as intended.
    """
    notify_called = 0
    deleted_files = []
    directory = '/orin/assets'
    modified_files = []
    
    def mock_notify(input_message):
        nonlocal notify_called
        notify_called += 1
    
    
    def mock_delete_file(path):
        nonlocal deleted_files
        deleted_files.append(path)
    
    
    class mock_Image:
        __slots__ = ('open_path',)
        
        @classmethod
        def open(cls, path):
            self = object.__new__(cls)
            self.open_path = path
            return self
        
        def save(self, path, *, format = None):
            nonlocal modified_files
            vampytest.assert_eq(format, 'png')
            modified_files.append((self.open_path, path))
    
    
    asset_entry_0 = AssetEntry('hey', 0, None, 'jpg')
    asset_entry_1 = AssetEntry('hey', 1, None, 'jpg')
    asset_entry_2 = AssetEntry('mister', 0, None, 'png')
    
    asset_group_0 = AssetGroup('hey')
    asset_group_0.add_entry(asset_entry_0)
    asset_group_0.add_entry(asset_entry_1)
    asset_group_1 = AssetGroup('mister')
    asset_group_1.add_entry(asset_entry_2)
    
    
    asset_groups = {
        'hey': asset_group_0,
        'mister': asset_group_1,
    }
    
    asset_entry_3 = AssetEntry('hey', 0, None, 'png')
    asset_entry_4 = AssetEntry('hey', 1, None, 'png')
    asset_entry_5 = AssetEntry('mister', 0, None, 'png')
    
    asset_group_2 = AssetGroup('hey')
    asset_group_2.add_entry(asset_entry_3)
    asset_group_2.add_entry(asset_entry_4)
    asset_group_3 = AssetGroup('mister')
    asset_group_3.add_entry(asset_entry_5)
    
    after_asset_groups = {
        'hey': asset_group_2,
        'mister': asset_group_3,
    }
    
    mocked = vampytest.mock_globals(
        convert_assets,
        notify = mock_notify,
        delete_file = mock_delete_file,
        Image = mock_Image
    )
    
    mocked(directory, asset_groups)
    
    vampytest.assert_eq(asset_groups, after_asset_groups)
    vampytest.assert_eq(notify_called, 4)
    vampytest.assert_eq(len(deleted_files), 2)
    vampytest.assert_eq(
        {*deleted_files},
        {
            join_paths(directory, 'hey-0000.jpg'),
            join_paths(directory, 'hey-0001.jpg'),
        },
    )
    vampytest.assert_eq(len(modified_files), 2)
    vampytest.assert_eq(
        {item[0] for item in modified_files},
        {
            join_paths(directory, 'hey-0000.jpg'),
            join_paths(directory, 'hey-0001.jpg'),
        },
    )
    vampytest.assert_eq(
        {item[1] for item in modified_files},
        {
            join_paths(directory, 'hey-0000.png'),
            join_paths(directory, 'hey-0001.png'),
        },
    )
