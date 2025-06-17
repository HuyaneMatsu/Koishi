__all__ = ('CHAPTER_STYLE_DEFAULT', 'TILE_EMOJI_MAPPING_DEFAULT')

from ...constants import CHAPTER_STYLES

from ..chapter_style import ChapterStyle
from ..constants import CHAPTER_STYLE_ID_DEFAULT, EMOJI_UNKNOWN
from ..tile_emoji_mapping import TileEmojiMapping

from .shared import (
    CONTROL_EMOJI_MAPPING_DEFAULT, EMOJI_WALL, EMOJI_WALL_EAST, EMOJI_WALL_EAST_SOUTH, EMOJI_WALL_EAST_SOUTH_WEST,
    EMOJI_WALL_EAST_WEST, EMOJI_WALL_NORTH_EAST, EMOJI_WALL_NORTH_EAST_SOUTH, EMOJI_WALL_NORTH_EAST_SOUTH_WEST,
    EMOJI_WALL_NORTH_EAST_WEST, EMOJI_WALL_NORTH_SOUTH, EMOJI_WALL_NORTH_SOUTH_WEST, EMOJI_WALL_NORTH_WEST,
    EMOJI_WALL_SOUTH, EMOJI_WALL_SOUTH_WEST, EMOJI_WALL_WEST
)

EMOJI_DEFAULT = EMOJI_UNKNOWN


TILE_EMOJI_MAPPING_DEFAULT = TileEmojiMapping(
    character_east_on_floor = EMOJI_UNKNOWN,
    character_east_on_hole_filled = EMOJI_UNKNOWN,
    character_east_on_obstacle_destroyed = EMOJI_UNKNOWN,
    character_east_on_target_on_floor = EMOJI_UNKNOWN,
    character_north_on_floor = EMOJI_UNKNOWN,
    character_north_on_hole_filled = EMOJI_UNKNOWN,
    character_north_on_obstacle_destroyed = EMOJI_UNKNOWN,
    character_north_on_target_on_floor = EMOJI_UNKNOWN,
    character_south_on_floor = EMOJI_UNKNOWN,
    character_south_on_hole_filled = EMOJI_UNKNOWN,
    character_south_on_obstacle_destroyed = EMOJI_UNKNOWN,
    character_south_on_target_on_floor = EMOJI_UNKNOWN,
    character_west_on_floor = EMOJI_UNKNOWN,
    character_west_on_hole_filled = EMOJI_UNKNOWN,
    character_west_on_obstacle_destroyed = EMOJI_UNKNOWN,
    character_west_on_target_on_floor = EMOJI_UNKNOWN,
    
    other_box_on_floor = EMOJI_UNKNOWN,
    other_box_on_hole_filled = EMOJI_UNKNOWN,
    other_box_on_obstacle_destroyed = EMOJI_UNKNOWN,
    other_box_on_target = EMOJI_UNKNOWN,
    other_floor = EMOJI_UNKNOWN,
    other_hole = EMOJI_UNKNOWN,
    other_hole_filled = EMOJI_UNKNOWN,
    other_obstacle = EMOJI_UNKNOWN,
    other_obstacle_destroyed = EMOJI_UNKNOWN,
    other_target_on_floor = EMOJI_UNKNOWN,
    
    wall = EMOJI_WALL,
    wall_east = EMOJI_WALL_EAST,
    wall_east_south = EMOJI_WALL_EAST_SOUTH,
    wall_east_south_west = EMOJI_WALL_EAST_SOUTH_WEST,
    wall_east_west = EMOJI_WALL_EAST_WEST,
    wall_north = EMOJI_UNKNOWN,
    wall_north_east = EMOJI_WALL_NORTH_EAST,
    wall_north_east_south = EMOJI_WALL_NORTH_EAST_SOUTH,
    wall_north_east_south_west = EMOJI_WALL_NORTH_EAST_SOUTH_WEST,
    wall_north_east_west = EMOJI_WALL_NORTH_EAST_WEST,
    wall_north_south = EMOJI_WALL_NORTH_SOUTH,
    wall_north_south_west = EMOJI_WALL_NORTH_SOUTH_WEST,
    wall_north_west = EMOJI_WALL_NORTH_WEST,
    wall_south = EMOJI_WALL_SOUTH,
    wall_south_west = EMOJI_WALL_SOUTH_WEST,
    wall_west = EMOJI_WALL_WEST,
)


CHAPTER_STYLE_DEFAULT = CHAPTER_STYLES[CHAPTER_STYLE_ID_DEFAULT] = ChapterStyle(
    CHAPTER_STYLE_ID_DEFAULT,
    EMOJI_DEFAULT,
    CONTROL_EMOJI_MAPPING_DEFAULT,
    TILE_EMOJI_MAPPING_DEFAULT,
)
