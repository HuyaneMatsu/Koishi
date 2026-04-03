import vampytest

from ..chapter_style import build_tile_resolution_table
from ..styles.default import TILE_EMOJI_MAPPING_DEFAULT


def test__build_tile_resolution_table():
    """
    Tests whether ``build_tile_resolution_table`` works as intended.
    """
    tile_emoji_mapping = TILE_EMOJI_MAPPING_DEFAULT
    
    output = build_tile_resolution_table(tile_emoji_mapping)
    
    vampytest.assert_instance(output, dict)
    
    for key, value in output.items():
        vampytest.assert_instance(key, int)
        vampytest.assert_instance(value, str)
