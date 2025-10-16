import vampytest

from ..font import TextWallFont


def _assert_fields_set(text_wall_font):
    """
    Asserts whether all fields are set of the given text wall font.
    
    Parameters
    ----------
    text_wall_font : ``TextWallFont``
        Instance to check.
    """
    vampytest.assert_instance(text_wall_font, TextWallFont)
    vampytest.assert_instance(text_wall_font.character_resolution_table, dict)
    vampytest.assert_instance(text_wall_font.size_height, int)
    vampytest.assert_instance(text_wall_font.size_width, int)
    vampytest.assert_instance(text_wall_font.name, str)


def test__TextWallFont__new():
    """
    Tests whether ``TextWallFont.__new__`` works as intended.
    """
    name = 'pudding'
    size_width = 1
    site_height = 2
    character_resolution_table = {
        'a': b'\x00\x00',
    }
    
    text_wall_font = TextWallFont(
        name,
        size_width,
        site_height,
        character_resolution_table,
    )
    _assert_fields_set(text_wall_font)
    
    vampytest.assert_eq(text_wall_font.character_resolution_table, character_resolution_table)
    vampytest.assert_eq(text_wall_font.size_height, site_height)
    vampytest.assert_eq(text_wall_font.size_width, size_width)
    vampytest.assert_eq(text_wall_font.name, name)


def test__TextWallFont__repr():
    """
    Tests whether ``TextWallFont.__repr__`` works as intended.
    """
    name = 'pudding'
    size_width = 1
    site_height = 2
    character_resolution_table = {
        'a': b'\x00\x00',
    }
    
    text_wall_font = TextWallFont(
        name,
        size_width,
        site_height,
        character_resolution_table,
    )
    
    output = repr(text_wall_font)
    vampytest.assert_instance(output, str)
