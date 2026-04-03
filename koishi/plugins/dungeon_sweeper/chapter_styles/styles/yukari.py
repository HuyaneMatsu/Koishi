__all__ = ('CHAPTER_STYLE_YUKARI',)

from hata import Emoji

from ...constants import CHAPTER_STYLES

from ..chapter_style import ChapterStyle
from ..constants import CHAPTER_STYLE_ID_YUKARI, EMOJI_UNKNOWN
from ..tile_emoji_mapping import TileEmojiMapping

from .shared import (
    CONTROL_EMOJI_MAPPING_DEFAULT, EMOJI_WALL, EMOJI_WALL_EAST, EMOJI_WALL_EAST_SOUTH, EMOJI_WALL_EAST_SOUTH_WEST,
    EMOJI_WALL_EAST_WEST, EMOJI_WALL_NORTH_EAST, EMOJI_WALL_NORTH_EAST_SOUTH, EMOJI_WALL_NORTH_EAST_SOUTH_WEST,
    EMOJI_WALL_NORTH_EAST_WEST, EMOJI_WALL_NORTH_SOUTH, EMOJI_WALL_NORTH_SOUTH_WEST, EMOJI_WALL_NORTH_WEST,
    EMOJI_WALL_SOUTH, EMOJI_WALL_SOUTH_WEST, EMOJI_WALL_WEST
)


EMOJI_YUKARI = Emoji.precreate(575389643424661505, name = 'YUKARI')

TILE_EMOJI_MAPPING_YUKARI = TileEmojiMapping(
    character_east_on_floor = Emoji.precreate(593179300153262257, name = '15'),
    character_east_on_hole_filled = Emoji.precreate(593179300300193800, name = '1D'),
    character_east_on_obstacle_destroyed = EMOJI_UNKNOWN,
    character_east_on_target_on_floor = Emoji.precreate(593179300145135646, name = '19'),
    character_north_on_floor = Emoji.precreate(593179300161650871, name = '14'),
    character_north_on_hole_filled = Emoji.precreate(593179300199399531, name = '1C'),
    character_north_on_obstacle_destroyed = EMOJI_UNKNOWN,
    character_north_on_target_on_floor = Emoji.precreate(593179300207919125, name = '18'),
    character_south_on_floor = Emoji.precreate(593179300300324887, name = '16'),
    character_south_on_hole_filled = Emoji.precreate(593179300216176760, name = '1E'),
    character_south_on_obstacle_destroyed = EMOJI_UNKNOWN,
    character_south_on_target_on_floor = Emoji.precreate(593179300170301451, name = '1A'),
    character_west_on_floor = Emoji.precreate(593179300237410314, name = '17'),
    character_west_on_hole_filled = Emoji.precreate(593179300153524224, name = '1F'),
    character_west_on_obstacle_destroyed = EMOJI_UNKNOWN,
    character_west_on_target_on_floor = Emoji.precreate(593179300153262189, name = '1B'),
    
    other_box_on_floor = Emoji.precreate(593179300296130561, name = '10'),
    other_box_on_hole_filled = Emoji.precreate(593179300149067790, name = '12'),
    other_box_on_obstacle_destroyed = EMOJI_UNKNOWN,
    other_box_on_target = Emoji.precreate(593179300136615936, name = '11'),
    other_floor = Emoji.precreate(593179300426022914, name = '0x'),
    other_hole = Emoji.precreate(593179300153262196, name = '13'),
    other_hole_filled = Emoji.precreate(593179300287479833, name = '0z'),
    other_obstacle = EMOJI_UNKNOWN,
    other_obstacle_destroyed = EMOJI_UNKNOWN,
    other_target_on_floor = Emoji.precreate(593179300019306556, name = '0y'),
    
    wall = EMOJI_WALL,
    wall_east = EMOJI_WALL_EAST,
    wall_east_south = EMOJI_WALL_EAST_SOUTH,
    wall_east_south_west = EMOJI_WALL_EAST_SOUTH_WEST,
    wall_east_west = EMOJI_WALL_EAST_WEST,
    wall_north = Emoji.precreate(593179300270702593, name = '0w'),
    wall_north_east = EMOJI_WALL_NORTH_EAST,
    wall_north_east_south = EMOJI_WALL_NORTH_EAST_SOUTH,
    wall_north_east_south_west = EMOJI_WALL_NORTH_EAST_SOUTH_WEST,
    wall_north_east_west = EMOJI_WALL_NORTH_EAST_WEST,
    wall_north_south = EMOJI_WALL_NORTH_SOUTH,
    wall_north_south_west = EMOJI_WALL_NORTH_SOUTH_WEST,
    wall_south_west = EMOJI_WALL_SOUTH_WEST,
    wall_south = EMOJI_WALL_SOUTH,
    wall_north_west = EMOJI_WALL_NORTH_WEST,
    wall_west = EMOJI_WALL_WEST,
)


CHAPTER_STYLE_YUKARI = CHAPTER_STYLES[CHAPTER_STYLE_ID_YUKARI] = ChapterStyle(
    CHAPTER_STYLE_ID_YUKARI,
    EMOJI_YUKARI,
    CONTROL_EMOJI_MAPPING_DEFAULT,
    TILE_EMOJI_MAPPING_YUKARI,
)
