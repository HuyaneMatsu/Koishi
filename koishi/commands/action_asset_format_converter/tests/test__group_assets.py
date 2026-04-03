import vampytest

from ..asset_entry import AssetEntry
from ..asset_group import AssetGroup
from ..grouping import group_assets


def test__group_assets():
    """
    Tests whether ``group_assets`` works as intended.
    """
    asset_entry_0 = AssetEntry('hey', 0, None, 'jpg')
    asset_entry_1 = AssetEntry('hey', 1, None, 'jpg')
    asset_entry_2 = AssetEntry('mister', 0, None, 'png')
    
    asset_entries = [
        asset_entry_0,
        asset_entry_1,
        asset_entry_2,
    ]
    
    output = group_assets(asset_entries)
    
    asset_group_0 = AssetGroup('hey')
    asset_group_0.add_entry(asset_entry_0)
    asset_group_0.add_entry(asset_entry_1)
    asset_group_1 = AssetGroup('mister')
    asset_group_1.add_entry(asset_entry_2)
    
    vampytest.assert_instance(output, dict)
    vampytest.assert_eq(
        output,
        {
            'hey': asset_group_0,
            'mister': asset_group_1,
        },
    )
