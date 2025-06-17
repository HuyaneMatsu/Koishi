__all__ = ('CHAPTER_STYLE_FLANDRE',)

from hata import Emoji

from ...constants import CHAPTER_STYLES

from ..chapter_style import ChapterStyle
from ..constants import CHAPTER_STYLE_ID_FLANDRE, EMOJI_UNKNOWN
from ..tile_emoji_mapping import TileEmojiMapping

from .shared import (
    CONTROL_EMOJI_MAPPING_DEFAULT, EMOJI_WALL, EMOJI_WALL_EAST, EMOJI_WALL_EAST_SOUTH, EMOJI_WALL_EAST_SOUTH_WEST,
    EMOJI_WALL_EAST_WEST, EMOJI_WALL_NORTH_EAST, EMOJI_WALL_NORTH_EAST_SOUTH, EMOJI_WALL_NORTH_EAST_SOUTH_WEST,
    EMOJI_WALL_NORTH_EAST_WEST, EMOJI_WALL_NORTH_SOUTH, EMOJI_WALL_NORTH_SOUTH_WEST, EMOJI_WALL_NORTH_WEST,
    EMOJI_WALL_SOUTH, EMOJI_WALL_SOUTH_WEST, EMOJI_WALL_WEST
)

EMOJI_FLANDRE = Emoji.precreate(575387120147890210, name = 'FLAN')


TILE_EMOJI_MAPPING_FLANDRE = TileEmojiMapping(
    character_east_on_floor = Emoji.precreate(580357693093576714, name = '0h'),
    character_east_on_hole_filled = Emoji.precreate(580357693072736257, name = '0p'),
    character_east_on_obstacle_destroyed = Emoji.precreate(580357692711763973, name = '0t'),
    character_east_on_target_on_floor = Emoji.precreate(580357693085188109, name = '0l'),
    character_north_on_floor = Emoji.precreate(580357693022142485, name = '0g'),
    character_north_on_hole_filled = Emoji.precreate(580357693324132352, name = '0o'),
    character_north_on_obstacle_destroyed = Emoji.precreate(580357693143777300, name = '0s'),
    character_north_on_target_on_floor = Emoji.precreate(580357693018210305, name = '0k'),
    character_south_on_floor = Emoji.precreate(580357693160685578, name = '0i'),
    character_south_on_hole_filled = Emoji.precreate(580357693131456513, name = '0q'),
    character_south_on_obstacle_destroyed = Emoji.precreate(580357693269606410, name = '0u'),
    character_south_on_target_on_floor = Emoji.precreate(580357693181657089, name = '0m'),
    character_west_on_floor = Emoji.precreate(580357693152165900, name = '0j'),
    character_west_on_hole_filled = Emoji.precreate(580357693366337536, name = '0r'),
    character_west_on_obstacle_destroyed = Emoji.precreate(580357693387177984, name = '0v'),
    character_west_on_target_on_floor = Emoji.precreate(580357693361881089, name = '0n'),
    
    other_box_on_floor = Emoji.precreate(580151963937931277, name = '0a'),
    other_box_on_hole_filled = Emoji.precreate(580151963937931277, name = '0a'),
    other_box_on_obstacle_destroyed = Emoji.precreate(580151963937931277, name = '0a'),
    other_box_on_target = Emoji.precreate(580188214086598667, name = '0f'),
    other_floor = Emoji.precreate(580150656501940245, name = '0Y'),
    other_hole = Emoji.precreate(580156463888990218, name = '0c'),
    other_hole_filled = Emoji.precreate(580159124466303001, name = '0d'),
    other_obstacle = Emoji.precreate(580151385258065925, name = '0Z'),
    other_obstacle_destroyed = Emoji.precreate(580163014045728818, name = '0e'),
    other_target_on_floor = Emoji.precreate(580153111545511967, name = '0b'),
    
    wall = EMOJI_WALL,
    wall_east = EMOJI_WALL_EAST,
    wall_east_south = EMOJI_WALL_EAST_SOUTH,
    wall_east_south_west = EMOJI_WALL_EAST_SOUTH_WEST,
    wall_east_west = EMOJI_WALL_EAST_WEST,
    wall_north = Emoji.precreate(580143707534262282, name = '0X'),
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


CHAPTER_STYLE_FLANDRE = CHAPTER_STYLES[CHAPTER_STYLE_ID_FLANDRE] = ChapterStyle(
    CHAPTER_STYLE_ID_FLANDRE,
    EMOJI_FLANDRE,
    CONTROL_EMOJI_MAPPING_DEFAULT,
    TILE_EMOJI_MAPPING_FLANDRE,
)
