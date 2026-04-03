import vampytest

from ...action_asset_format_converter.asset_entry import AssetEntry

from ..filtering import filter_new_asset_entries


def test__filter_new_asset_entries():
    """
    Tests whether ``filter_new_asset_entries`` works as intended.
    """
    asset_entry_0 = AssetEntry('hey', 0, None, 'jpg')
    asset_entry_1 = AssetEntry('hey', 1, None, 'jpg')
    asset_entry_2 = AssetEntry('mister', 0, None, 'png')
    asset_entry_3 = AssetEntry('mister', 0, 'original', 'png')
    asset_entry_4 = AssetEntry('chiruno-feed', 0, None, 'png')
    asset_entry_5 = AssetEntry('sister', 0, None, 'gif')
    asset_entry_6 = AssetEntry('flandre-remilia-kiss', 0, None, 'png')
    
    output = filter_new_asset_entries(
        [
            asset_entry_0,
            asset_entry_1,
            asset_entry_2,
            asset_entry_3,
            asset_entry_4,
            asset_entry_5,
            asset_entry_6,
        ],
        {
            'chiruno-feed-0000',
            'flandre-remilia-kiss-0000',
        },
    )
    vampytest.assert_instance(output, list)
    vampytest.assert_eq(
        output,
        [
            asset_entry_2,
            asset_entry_5,
        ],
    )
