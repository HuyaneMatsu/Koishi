import vampytest

from ....plugins.touhou_core import KOMEIJI_KOISHI, KOMEIJI_SATORI, get_touhou_character_like

from ...action_asset_format_converter.asset_entry import AssetEntry

from ..filtering import classify_asset_entry_parts


def test__classify_asset_entry_parts():
    """
    Tests whether ``classify_asset_entry_parts`` works as intended.
    """
    asset_entry = AssetEntry('nyanner-koishi-satori-feed-hug', 0, None, 'png')
    
    output = classify_asset_entry_parts(asset_entry, {'feed', 'hug', 'kiss'}, get_touhou_character_like)
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(len(output), 3)
    vampytest.assert_eq(
        output,
        (
            {KOMEIJI_KOISHI, KOMEIJI_SATORI},
            {'feed', 'hug'},
            {'nyanner'},
        )
    )
