__all__ = ('CHAPTER_STYLE_REIMU',)

from hata import Emoji

from ...constants import CHAPTER_STYLES

from ..chapter_style import ChapterStyle
from ..constants import CHAPTER_STYLE_ID_REIMU, EMOJI_UNKNOWN
from ..tile_emoji_mapping import TileEmojiMapping

from .shared import (
    CONTROL_EMOJI_MAPPING_DEFAULT, EMOJI_WALL, EMOJI_WALL_EAST, EMOJI_WALL_EAST_SOUTH, EMOJI_WALL_EAST_SOUTH_WEST,
    EMOJI_WALL_EAST_WEST, EMOJI_WALL_NORTH_EAST, EMOJI_WALL_NORTH_EAST_SOUTH, EMOJI_WALL_NORTH_EAST_SOUTH_WEST,
    EMOJI_WALL_NORTH_EAST_WEST, EMOJI_WALL_NORTH_SOUTH, EMOJI_WALL_NORTH_SOUTH_WEST, EMOJI_WALL_NORTH_WEST,
    EMOJI_WALL_SOUTH, EMOJI_WALL_SOUTH_WEST, EMOJI_WALL_WEST
)

EMOJI_REIMU = Emoji.precreate(574307645347856384, name = 'REIMU')


TILE_EMOJI_MAPPING_REIMU = TileEmojiMapping(
    character_east_on_floor = Emoji.precreate(574213472347226114, name = '0E'),
    character_east_on_hole_filled = Emoji.precreate(574249291074240523, name = '09'),
    character_east_on_obstacle_destroyed = EMOJI_UNKNOWN,
    character_east_on_target_on_floor = Emoji.precreate(574249292026478595, name = '07'),
    character_north_on_floor = Emoji.precreate(574214258871500800, name = '0D'),
    character_north_on_hole_filled = Emoji.precreate(574249293662388264, name = '02'),
    character_north_on_obstacle_destroyed = EMOJI_UNKNOWN,
    character_north_on_target_on_floor = Emoji.precreate(574249292496371732, name = '04'),
    character_south_on_floor = Emoji.precreate(574220751662612502, name = '0B'),
    character_south_on_hole_filled = Emoji.precreate(574249291145543681, name = '08'),
    character_south_on_obstacle_destroyed = EMOJI_UNKNOWN,
    character_south_on_target_on_floor = Emoji.precreate(574249292261490690, name = '06'),
    character_west_on_floor = Emoji.precreate(574218036156825629, name = '0C'),
    character_west_on_hole_filled = Emoji.precreate(574249292957614090, name = '03'),
    character_west_on_obstacle_destroyed = EMOJI_UNKNOWN,
    character_west_on_target_on_floor = Emoji.precreate(574249292487720970, name = '05'),
    
    other_box_on_floor = Emoji.precreate(574212211434717214, name = '0G'),
    other_box_on_hole_filled = Emoji.precreate(574212211434717214, name = '0G'),
    other_box_on_obstacle_destroyed = EMOJI_UNKNOWN,
    other_box_on_target = Emoji.precreate(574213002190913536, name = '0F'),
    other_floor = Emoji.precreate(574211101638656010, name = '0H'),
    other_hole = Emoji.precreate(574187906642477066, name = '0J'),
    other_hole_filled = Emoji.precreate(574202754134835200, name = '0I'),
    other_obstacle = EMOJI_UNKNOWN,
    other_obstacle_destroyed = EMOJI_UNKNOWN,
    other_target_on_floor = Emoji.precreate(574234087645249546, name = '0A'),
    
    wall = EMOJI_WALL,
    wall_east = EMOJI_WALL_EAST,
    wall_east_south = EMOJI_WALL_EAST_SOUTH,
    wall_east_south_west = EMOJI_WALL_EAST_SOUTH_WEST,
    wall_east_west = EMOJI_WALL_EAST_WEST,
    wall_north = Emoji.precreate(580141387631165450, name = '0O'),
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


CHAPTER_STYLE_REIMU = CHAPTER_STYLES[CHAPTER_STYLE_ID_REIMU] = ChapterStyle(
    CHAPTER_STYLE_ID_REIMU,
    EMOJI_REIMU,
    CONTROL_EMOJI_MAPPING_DEFAULT,
    TILE_EMOJI_MAPPING_REIMU,
)
