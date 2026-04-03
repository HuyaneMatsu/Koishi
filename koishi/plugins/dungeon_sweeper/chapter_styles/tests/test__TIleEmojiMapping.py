import vampytest
from hata import EMOJIS, Emoji

from ..tile_emoji_mapping import TileEmojiMapping


def _assert_fields_set(tile_emoji_mapping):
    """
    Checks whether the given tile emoji mapping has all of its fields set.
    
    Parameters
    ----------
    tile_emoji_mapping : ``TileEmojiMapping``
        The instance to test.
    """
    vampytest.assert_instance(tile_emoji_mapping, TileEmojiMapping)
    
    vampytest.assert_instance(tile_emoji_mapping.character_east_on_floor, Emoji)
    vampytest.assert_instance(tile_emoji_mapping.character_east_on_hole_filled, Emoji)
    vampytest.assert_instance(tile_emoji_mapping.character_east_on_obstacle_destroyed, Emoji)
    vampytest.assert_instance(tile_emoji_mapping.character_east_on_target_on_floor, Emoji)
    vampytest.assert_instance(tile_emoji_mapping.character_north_on_floor, Emoji)
    vampytest.assert_instance(tile_emoji_mapping.character_north_on_hole_filled, Emoji)
    vampytest.assert_instance(tile_emoji_mapping.character_north_on_obstacle_destroyed, Emoji)
    vampytest.assert_instance(tile_emoji_mapping.character_north_on_target_on_floor, Emoji)
    vampytest.assert_instance(tile_emoji_mapping.character_south_on_floor, Emoji)
    vampytest.assert_instance(tile_emoji_mapping.character_south_on_hole_filled, Emoji)
    vampytest.assert_instance(tile_emoji_mapping.character_south_on_obstacle_destroyed, Emoji)
    vampytest.assert_instance(tile_emoji_mapping.character_south_on_target_on_floor, Emoji)
    vampytest.assert_instance(tile_emoji_mapping.character_west_on_floor, Emoji)
    vampytest.assert_instance(tile_emoji_mapping.character_west_on_hole_filled, Emoji)
    vampytest.assert_instance(tile_emoji_mapping.character_west_on_obstacle_destroyed, Emoji)
    vampytest.assert_instance(tile_emoji_mapping.character_west_on_target_on_floor, Emoji)
    
    vampytest.assert_instance(tile_emoji_mapping.other_box_on_floor, Emoji)
    vampytest.assert_instance(tile_emoji_mapping.other_box_on_hole_filled, Emoji)
    vampytest.assert_instance(tile_emoji_mapping.other_box_on_obstacle_destroyed, Emoji)
    vampytest.assert_instance(tile_emoji_mapping.other_box_on_target, Emoji)
    vampytest.assert_instance(tile_emoji_mapping.other_floor, Emoji)
    vampytest.assert_instance(tile_emoji_mapping.other_hole, Emoji)
    vampytest.assert_instance(tile_emoji_mapping.other_hole_filled, Emoji)
    vampytest.assert_instance(tile_emoji_mapping.other_obstacle, Emoji)
    vampytest.assert_instance(tile_emoji_mapping.other_obstacle_destroyed, Emoji)
    vampytest.assert_instance(tile_emoji_mapping.other_target_on_floor, Emoji)
    
    vampytest.assert_instance(tile_emoji_mapping.wall, Emoji)
    vampytest.assert_instance(tile_emoji_mapping.wall_east, Emoji)
    vampytest.assert_instance(tile_emoji_mapping.wall_east_south, Emoji)
    vampytest.assert_instance(tile_emoji_mapping.wall_east_south_west, Emoji)
    vampytest.assert_instance(tile_emoji_mapping.wall_east_west, Emoji)
    vampytest.assert_instance(tile_emoji_mapping.wall_north, Emoji)
    vampytest.assert_instance(tile_emoji_mapping.wall_north_east, Emoji)
    vampytest.assert_instance(tile_emoji_mapping.wall_north_east_south, Emoji)
    vampytest.assert_instance(tile_emoji_mapping.wall_north_east_south_west, Emoji)
    vampytest.assert_instance(tile_emoji_mapping.wall_north_east_west, Emoji)
    vampytest.assert_instance(tile_emoji_mapping.wall_north_south, Emoji)
    vampytest.assert_instance(tile_emoji_mapping.wall_north_south_west, Emoji)
    vampytest.assert_instance(tile_emoji_mapping.wall_north_west, Emoji)
    vampytest.assert_instance(tile_emoji_mapping.wall_south, Emoji)
    vampytest.assert_instance(tile_emoji_mapping.wall_south_west, Emoji)
    vampytest.assert_instance(tile_emoji_mapping.wall_west, Emoji)


def test__tile_emoji_mapping__new():
    """
    Tests whether ``TileEmojiMapping.__new__`` works as intended.
    """
    character_east_on_floor = EMOJIS[1]
    character_east_on_hole_filled = EMOJIS[2]
    character_east_on_obstacle_destroyed = EMOJIS[3]
    character_east_on_target_on_floor = EMOJIS[4]
    character_north_on_floor = EMOJIS[5]
    character_north_on_hole_filled = EMOJIS[6]
    character_north_on_obstacle_destroyed = EMOJIS[7]
    character_north_on_target_on_floor = EMOJIS[8]
    character_south_on_floor = EMOJIS[9]
    character_south_on_hole_filled = EMOJIS[10]
    character_south_on_obstacle_destroyed = EMOJIS[11]
    character_south_on_target_on_floor = EMOJIS[12]
    character_west_on_floor = EMOJIS[13]
    character_west_on_hole_filled = EMOJIS[14]
    character_west_on_obstacle_destroyed = EMOJIS[15]
    character_west_on_target_on_floor = EMOJIS[16]
        
    other_box_on_floor = EMOJIS[17]
    other_box_on_hole_filled = EMOJIS[18]
    other_box_on_obstacle_destroyed = EMOJIS[19]
    other_box_on_target = EMOJIS[20]
    other_floor = EMOJIS[21]
    other_hole = EMOJIS[22]
    other_hole_filled = EMOJIS[23]
    other_obstacle = EMOJIS[24]
    other_obstacle_destroyed = EMOJIS[25]
    other_target_on_floor = EMOJIS[26]
        
    wall = EMOJIS[27]
    wall_east = EMOJIS[28]
    wall_east_south = EMOJIS[29]
    wall_east_south_west = EMOJIS[30]
    wall_east_west = EMOJIS[31]
    wall_north = EMOJIS[32]
    wall_north_east = EMOJIS[33]
    wall_north_east_south = EMOJIS[33]
    wall_north_east_south_west = EMOJIS[34]
    wall_north_east_west = EMOJIS[35]
    wall_north_south = EMOJIS[36]
    wall_north_south_west = EMOJIS[37]
    wall_north_west = EMOJIS[38]
    wall_south = EMOJIS[39]
    wall_south_west = EMOJIS[40]
    wall_west = EMOJIS[41]
    
    tile_emoji_mapping = TileEmojiMapping(
        character_east_on_floor = character_east_on_floor,
        character_east_on_hole_filled = character_east_on_hole_filled,
        character_east_on_obstacle_destroyed = character_east_on_obstacle_destroyed,
        character_east_on_target_on_floor = character_east_on_target_on_floor,
        character_north_on_floor = character_north_on_floor,
        character_north_on_hole_filled = character_north_on_hole_filled,
        character_north_on_obstacle_destroyed = character_north_on_obstacle_destroyed,
        character_north_on_target_on_floor = character_north_on_target_on_floor,
        character_south_on_floor = character_south_on_floor,
        character_south_on_hole_filled = character_south_on_hole_filled,
        character_south_on_obstacle_destroyed = character_south_on_obstacle_destroyed,
        character_south_on_target_on_floor = character_south_on_target_on_floor,
        character_west_on_floor = character_west_on_floor,
        character_west_on_hole_filled = character_west_on_hole_filled,
        character_west_on_obstacle_destroyed = character_west_on_obstacle_destroyed,
        character_west_on_target_on_floor = character_west_on_target_on_floor,
        
        other_box_on_floor = other_box_on_floor,
        other_box_on_hole_filled = other_box_on_hole_filled,
        other_box_on_obstacle_destroyed = other_box_on_obstacle_destroyed,
        other_box_on_target = other_box_on_target,
        other_floor = other_floor,
        other_hole = other_hole,
        other_hole_filled = other_hole_filled,
        other_obstacle = other_obstacle,
        other_obstacle_destroyed = other_obstacle_destroyed,
        other_target_on_floor = other_target_on_floor,
        
        wall = wall,
        wall_east = wall_east,
        wall_east_south = wall_east_south,
        wall_east_south_west = wall_east_south_west,
        wall_east_west = wall_east_west,
        wall_north = wall_north,
        wall_north_east = wall_north_east,
        wall_north_east_south = wall_north_east_south,
        wall_north_east_south_west = wall_north_east_south_west,
        wall_north_east_west = wall_north_east_west,
        wall_north_south = wall_north_south,
        wall_north_south_west = wall_north_south_west,
        wall_north_west = wall_north_west,
        wall_south = wall_south,
        wall_south_west = wall_south_west,
        wall_west = wall_west,
    )
    _assert_fields_set(tile_emoji_mapping)
    
    vampytest.assert_is(tile_emoji_mapping.character_east_on_floor, character_east_on_floor)
    vampytest.assert_is(tile_emoji_mapping.character_east_on_hole_filled, character_east_on_hole_filled)
    vampytest.assert_is(tile_emoji_mapping.character_east_on_obstacle_destroyed, character_east_on_obstacle_destroyed)
    vampytest.assert_is(tile_emoji_mapping.character_east_on_target_on_floor, character_east_on_target_on_floor)
    vampytest.assert_is(tile_emoji_mapping.character_north_on_floor, character_north_on_floor)
    vampytest.assert_is(tile_emoji_mapping.character_north_on_hole_filled, character_north_on_hole_filled)
    vampytest.assert_is(tile_emoji_mapping.character_north_on_obstacle_destroyed, character_north_on_obstacle_destroyed)
    vampytest.assert_is(tile_emoji_mapping.character_north_on_target_on_floor, character_north_on_target_on_floor)
    vampytest.assert_is(tile_emoji_mapping.character_south_on_floor, character_south_on_floor)
    vampytest.assert_is(tile_emoji_mapping.character_south_on_hole_filled, character_south_on_hole_filled)
    vampytest.assert_is(tile_emoji_mapping.character_south_on_obstacle_destroyed, character_south_on_obstacle_destroyed)
    vampytest.assert_is(tile_emoji_mapping.character_south_on_target_on_floor, character_south_on_target_on_floor)
    vampytest.assert_is(tile_emoji_mapping.character_west_on_floor, character_west_on_floor)
    vampytest.assert_is(tile_emoji_mapping.character_west_on_hole_filled, character_west_on_hole_filled)
    vampytest.assert_is(tile_emoji_mapping.character_west_on_obstacle_destroyed, character_west_on_obstacle_destroyed)
    vampytest.assert_is(tile_emoji_mapping.character_west_on_target_on_floor, character_west_on_target_on_floor)
        
    vampytest.assert_is(tile_emoji_mapping.other_box_on_floor, other_box_on_floor)
    vampytest.assert_is(tile_emoji_mapping.other_box_on_hole_filled, other_box_on_hole_filled)
    vampytest.assert_is(tile_emoji_mapping.other_box_on_obstacle_destroyed, other_box_on_obstacle_destroyed)
    vampytest.assert_is(tile_emoji_mapping.other_box_on_target, other_box_on_target)
    vampytest.assert_is(tile_emoji_mapping.other_floor, other_floor)
    vampytest.assert_is(tile_emoji_mapping.other_hole, other_hole)
    vampytest.assert_is(tile_emoji_mapping.other_hole_filled, other_hole_filled)
    vampytest.assert_is(tile_emoji_mapping.other_obstacle, other_obstacle)
    vampytest.assert_is(tile_emoji_mapping.other_obstacle_destroyed, other_obstacle_destroyed)
    vampytest.assert_is(tile_emoji_mapping.other_target_on_floor, other_target_on_floor)
        
    vampytest.assert_is(tile_emoji_mapping.wall, wall)
    vampytest.assert_is(tile_emoji_mapping.wall_east, wall_east)
    vampytest.assert_is(tile_emoji_mapping.wall_east_south, wall_east_south)
    vampytest.assert_is(tile_emoji_mapping.wall_east_south_west, wall_east_south_west)
    vampytest.assert_is(tile_emoji_mapping.wall_east_west, wall_east_west)
    vampytest.assert_is(tile_emoji_mapping.wall_north, wall_north)
    vampytest.assert_is(tile_emoji_mapping.wall_north_east, wall_north_east)
    vampytest.assert_is(tile_emoji_mapping.wall_north_east_south, wall_north_east_south)
    vampytest.assert_is(tile_emoji_mapping.wall_north_east_south_west, wall_north_east_south_west)
    vampytest.assert_is(tile_emoji_mapping.wall_north_east_west, wall_north_east_west)
    vampytest.assert_is(tile_emoji_mapping.wall_north_south, wall_north_south)
    vampytest.assert_is(tile_emoji_mapping.wall_north_south_west, wall_north_south_west)
    vampytest.assert_is(tile_emoji_mapping.wall_north_west, wall_north_west)
    vampytest.assert_is(tile_emoji_mapping.wall_south, wall_south)
    vampytest.assert_is(tile_emoji_mapping.wall_south_west, wall_south_west)
    vampytest.assert_is(tile_emoji_mapping.wall_west, wall_west)


def test__tile_emoji_mapping__repr():
    """
    Tests whether ``TileEmojiMapping.__repr__`` works as intended.
    """
    character_east_on_floor = EMOJIS[1]
    character_east_on_hole_filled = EMOJIS[2]
    character_east_on_obstacle_destroyed = EMOJIS[3]
    character_east_on_target_on_floor = EMOJIS[4]
    character_north_on_floor = EMOJIS[5]
    character_north_on_hole_filled = EMOJIS[6]
    character_north_on_obstacle_destroyed = EMOJIS[7]
    character_north_on_target_on_floor = EMOJIS[8]
    character_south_on_floor = EMOJIS[9]
    character_south_on_hole_filled = EMOJIS[10]
    character_south_on_obstacle_destroyed = EMOJIS[11]
    character_south_on_target_on_floor = EMOJIS[12]
    character_west_on_floor = EMOJIS[13]
    character_west_on_hole_filled = EMOJIS[14]
    character_west_on_obstacle_destroyed = EMOJIS[15]
    character_west_on_target_on_floor = EMOJIS[16]
        
    other_box_on_floor = EMOJIS[17]
    other_box_on_hole_filled = EMOJIS[18]
    other_box_on_obstacle_destroyed = EMOJIS[19]
    other_box_on_target = EMOJIS[20]
    other_floor = EMOJIS[21]
    other_hole = EMOJIS[22]
    other_hole_filled = EMOJIS[23]
    other_obstacle = EMOJIS[24]
    other_obstacle_destroyed = EMOJIS[25]
    other_target_on_floor = EMOJIS[26]
        
    wall = EMOJIS[27]
    wall_east = EMOJIS[28]
    wall_east_south = EMOJIS[29]
    wall_east_south_west = EMOJIS[30]
    wall_east_west = EMOJIS[31]
    wall_north = EMOJIS[32]
    wall_north_east = EMOJIS[33]
    wall_north_east_south = EMOJIS[33]
    wall_north_east_south_west = EMOJIS[34]
    wall_north_east_west = EMOJIS[35]
    wall_north_south = EMOJIS[36]
    wall_north_south_west = EMOJIS[37]
    wall_north_west = EMOJIS[38]
    wall_south = EMOJIS[39]
    wall_south_west = EMOJIS[40]
    wall_west = EMOJIS[41]
    
    tile_emoji_mapping = TileEmojiMapping(
        character_east_on_floor = character_east_on_floor,
        character_east_on_hole_filled = character_east_on_hole_filled,
        character_east_on_obstacle_destroyed = character_east_on_obstacle_destroyed,
        character_east_on_target_on_floor = character_east_on_target_on_floor,
        character_north_on_floor = character_north_on_floor,
        character_north_on_hole_filled = character_north_on_hole_filled,
        character_north_on_obstacle_destroyed = character_north_on_obstacle_destroyed,
        character_north_on_target_on_floor = character_north_on_target_on_floor,
        character_south_on_floor = character_south_on_floor,
        character_south_on_hole_filled = character_south_on_hole_filled,
        character_south_on_obstacle_destroyed = character_south_on_obstacle_destroyed,
        character_south_on_target_on_floor = character_south_on_target_on_floor,
        character_west_on_floor = character_west_on_floor,
        character_west_on_hole_filled = character_west_on_hole_filled,
        character_west_on_obstacle_destroyed = character_west_on_obstacle_destroyed,
        character_west_on_target_on_floor = character_west_on_target_on_floor,
        
        other_box_on_floor = other_box_on_floor,
        other_box_on_hole_filled = other_box_on_hole_filled,
        other_box_on_obstacle_destroyed = other_box_on_obstacle_destroyed,
        other_box_on_target = other_box_on_target,
        other_floor = other_floor,
        other_hole = other_hole,
        other_hole_filled = other_hole_filled,
        other_obstacle = other_obstacle,
        other_obstacle_destroyed = other_obstacle_destroyed,
        other_target_on_floor = other_target_on_floor,
        
        wall = wall,
        wall_east = wall_east,
        wall_east_south = wall_east_south,
        wall_east_south_west = wall_east_south_west,
        wall_east_west = wall_east_west,
        wall_north = wall_north,
        wall_north_east = wall_north_east,
        wall_north_east_south = wall_north_east_south,
        wall_north_east_south_west = wall_north_east_south_west,
        wall_north_east_west = wall_north_east_west,
        wall_north_south = wall_north_south,
        wall_north_south_west = wall_north_south_west,
        wall_north_west = wall_north_west,
        wall_south = wall_south,
        wall_south_west = wall_south_west,
        wall_west = wall_west,
    )
    
    output = repr(tile_emoji_mapping)
    vampytest.assert_instance(output, str)
