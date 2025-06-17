import vampytest
from hata import Component, ComponentType

from ..chapter_styles import CHAPTER_STYLE_REIMU
from ..tile_bit_masks import BIT_FLAG_NORTH, BIT_MASK_CHARACTER, BIT_MASK_FLOOR, BIT_MASK_WALL

from ..component_building import build_component_tiles


def test__build_component_tiles__small():
    """
    Tests whether ``build_component_tiles`` works as intended.
    
    Case: small sized map.
    """
    wall = BIT_MASK_WALL | BIT_FLAG_NORTH
    character = BIT_MASK_FLOOR | BIT_MASK_CHARACTER | BIT_FLAG_NORTH
    floor = BIT_MASK_FLOOR
    
    style = CHAPTER_STYLE_REIMU
    
    map_ = [
        wall    , wall  , wall      , wall  , wall  ,
        wall    , floor , floor     , floor , wall  ,
        wall    , floor , character , floor , wall  ,
        wall    , floor , floor     , floor , wall  ,
        wall    , wall  , wall      , wall  , wall  ,
    ]
    
    size_x = 5
    
    
    output = build_component_tiles(style, map_, size_x)
    vampytest.assert_instance(output, Component)
    vampytest.assert_is(output.type, ComponentType.text_display)
    
    vampytest.assert_eq(
        output.content,
        ''.join([
            *(style.tile_resolution_table[map_[index]] for index in range(0, 5)), '\n',
            *(style.tile_resolution_table[map_[index]] for index in range(5, 10)), '\n',
            *(style.tile_resolution_table[map_[index]] for index in range(10, 15)), '\n',
            *(style.tile_resolution_table[map_[index]] for index in range(15, 20)), '\n',
            *(style.tile_resolution_table[map_[index]] for index in range(20, 25)),
        ])
    )


def test__build_component_tiles__big():
    """
    Tests whether ``build_component_tiles`` works as intended.
    
    Case: big sized map.
    """
    wall = BIT_MASK_WALL | BIT_FLAG_NORTH
    character = BIT_MASK_FLOOR | BIT_MASK_CHARACTER | BIT_FLAG_NORTH
    floor = BIT_MASK_FLOOR
    
    style = CHAPTER_STYLE_REIMU
    
    map_ = [
        *(wall for _ in range(14)),
        wall, *(floor for _ in range(12)), wall,
        wall, *(floor for _ in range(12)), wall,
        wall, *(floor for _ in range(12)), wall,
        wall, *(floor for _ in range(12)), wall,
        wall, *(floor for _ in range(12)), wall,
        wall, *(floor for _ in range(12)), wall,
        wall, *(floor for _ in range(11)), character, wall,
        wall, *(floor for _ in range(12)), wall,
        wall, *(floor for _ in range(12)), wall,
        wall, *(floor for _ in range(12)), wall,
        wall, *(floor for _ in range(12)), wall,
        wall, *(floor for _ in range(12)), wall,
        *(wall for _ in range(14)),
    ]
    
    size_x = 14
    
    
    output = build_component_tiles(style, map_, size_x)
    vampytest.assert_instance(output, Component)
    vampytest.assert_is(output.type, ComponentType.text_display)
    
    vampytest.assert_eq(
        output.content,
        ''.join([
            *(style.tile_resolution_table[map_[index]] for index in range( 1 * 14 + 1,  2 * 14 - 1)), '\n',
            *(style.tile_resolution_table[map_[index]] for index in range( 2 * 14 + 1,  3 * 14 - 1)), '\n',
            *(style.tile_resolution_table[map_[index]] for index in range( 3 * 14 + 1,  4 * 14 - 1)), '\n',
            *(style.tile_resolution_table[map_[index]] for index in range( 4 * 14 + 1,  5 * 14 - 1)), '\n',
            *(style.tile_resolution_table[map_[index]] for index in range( 5 * 14 + 1,  6 * 14 - 1)), '\n',
            *(style.tile_resolution_table[map_[index]] for index in range( 6 * 14 + 1,  7 * 14 - 1)), '\n',
            *(style.tile_resolution_table[map_[index]] for index in range( 7 * 14 + 1,  8 * 14 - 1)), '\n',
            *(style.tile_resolution_table[map_[index]] for index in range( 8 * 14 + 1,  9 * 14 - 1)), '\n',
            *(style.tile_resolution_table[map_[index]] for index in range( 9 * 14 + 1, 10 * 14 - 1)), '\n',
            *(style.tile_resolution_table[map_[index]] for index in range(10 * 14 + 1, 11 * 14 - 1)), '\n',
            *(style.tile_resolution_table[map_[index]] for index in range(11 * 14 + 1, 12 * 14 - 1)), '\n',
            *(style.tile_resolution_table[map_[index]] for index in range(12 * 14 + 1, 13 * 14 - 1)),
        ])
    )
