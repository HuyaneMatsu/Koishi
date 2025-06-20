__all__ = ()

from os.path import dirname as get_parent_directory_path, join as join_paths

from scarletio import Lock, get_event_loop

from ..tile_bit_masks import (
    BIT_FLAG_EAST, BIT_FLAG_NORTH, BIT_FLAG_SOUTH, BIT_FLAG_WEST, BIT_MASK_BOX, BIT_MASK_BOX_ON_TARGET,
    BIT_MASK_CHARACTER, BIT_MASK_FLOOR, BIT_MASK_HOLE, BIT_MASK_HOLE_FILLED, BIT_MASK_OBSTACLE,
    BIT_MASK_TARGET_ON_FLOOR, BIT_MASK_WALL
)


FILE_LOCK = Lock(get_event_loop())
CHAPTERS_PATH = join_paths(get_parent_directory_path(__file__), 'assets')

CHAPTER_ID_DEFAULT = 0
STAGE_ID_DEFAULT = 0

FILE_NAME_REIMU = 'reimu.json'
FILE_NAME_FLANDRE = 'flandre.json'
FILE_NAME_YUKARI = 'yukari.json'


JSON_KEY_CHAPTER_ID = "id"
JSON_KEY_CHAPTER_UNLOCK_PREREQUISITE_STAGE_ID = "unlock_prerequisite_stage_id"
JSON_KEY_CHAPTER_FIRST_STAGE_ID = "first_stage_id"
JSON_KEY_CHAPTER_PREVIOUS_CHAPTER_ID = "previous_chapter_id"
JSON_KEY_CHAPTER_NEXT_CHAPTER_ID = "next_chapter_id"
JSON_KEY_CHAPTER_SKILL_ID = 'skill_id'
JSON_KEY_CHAPTER_STYLE_ID = 'style_id'
JSON_KEY_CHAPTER_STAGES = "stages"
JSON_KEY_CHAPTER_RULE_ID = 'rule_id'
JSON_KEY_CHAPTER_DISPLAY_NAME = 'display_name'

JSON_KEY_STAGE_BEST = 'best'
JSON_KEY_STAGE_DIFFICULTY_ID = 'difficulty_id'
JSON_KEY_STAGE_IN_DIFFICULTY_INDEX = 'in_difficulty_index'
JSON_KEY_STAGE_ID = 'id'
JSON_KEY_STAGE_START_POSITION = 'start_position'
JSON_KEY_STAGE_TARGET_COUNT = 'target_count'
JSON_KEY_STAGE_MAP = 'map'
JSON_KEY_STAGE_SIZE_X = 'size_x'
JSON_KEY_STAGE_PREVIOUS_STAGE_ID = 'previous_stage_id'
JSON_KEY_STAGE_NEXT_STAGE_ID = 'next_stage_id'


TILE_VALUE_DEFAULT = BIT_MASK_WALL
TILE_NAME_DEFAULT = ''

TILE_NAME_TO_VALUE = {
    'FLOOR'     : BIT_MASK_FLOOR,
    'TARGET'    : BIT_MASK_TARGET_ON_FLOOR,
    'BOX'       : BIT_MASK_FLOOR | BIT_MASK_BOX,
    'BOX_TARGET': BIT_MASK_FLOOR | BIT_MASK_BOX_ON_TARGET,
    'HOLE'      : BIT_MASK_HOLE,
    'HOLE_F'    : BIT_MASK_HOLE_FILLED,
    'OBSTACLE'  : BIT_MASK_OBSTACLE,
    
    'CN_FLOOR'  : BIT_MASK_CHARACTER | BIT_FLAG_NORTH | BIT_MASK_FLOOR,
    'CE_FLOOR'  : BIT_MASK_CHARACTER | BIT_FLAG_EAST | BIT_MASK_FLOOR,
    'CS_FLOOR'  : BIT_MASK_CHARACTER | BIT_FLAG_SOUTH | BIT_MASK_FLOOR,
    'CW_FLOOR'  : BIT_MASK_CHARACTER | BIT_FLAG_WEST | BIT_MASK_FLOOR,
    'CN_TARGET' : BIT_MASK_CHARACTER | BIT_FLAG_NORTH | BIT_MASK_TARGET_ON_FLOOR,
    'CE_TARGET' : BIT_MASK_CHARACTER | BIT_FLAG_EAST | BIT_MASK_TARGET_ON_FLOOR,
    'CS_TARGET' : BIT_MASK_CHARACTER | BIT_FLAG_SOUTH | BIT_MASK_TARGET_ON_FLOOR,
    'CW_TARGET' : BIT_MASK_CHARACTER | BIT_FLAG_WEST | BIT_MASK_TARGET_ON_FLOOR,
    
    'NOTHING'   : BIT_MASK_WALL,
    'WALL_N'    : BIT_MASK_WALL | BIT_FLAG_NORTH,
    'WALL_E'    : BIT_MASK_WALL | BIT_FLAG_EAST,
    'WALL_S'    : BIT_MASK_WALL | BIT_FLAG_SOUTH,
    'WALL_W'    : BIT_MASK_WALL | BIT_FLAG_WEST,
    'WALL_HV'   : BIT_MASK_WALL | BIT_FLAG_NORTH | BIT_FLAG_EAST | BIT_FLAG_SOUTH | BIT_FLAG_WEST,
    'WALL_SE'   : BIT_MASK_WALL | BIT_FLAG_EAST | BIT_FLAG_SOUTH,
    'WALL_SW'   : BIT_MASK_WALL | BIT_FLAG_SOUTH | BIT_FLAG_WEST,
    'WALL_NE'   : BIT_MASK_WALL | BIT_FLAG_NORTH | BIT_FLAG_EAST,
    'WALL_NW'   : BIT_MASK_WALL | BIT_FLAG_NORTH | BIT_FLAG_WEST,
    'WALL_HE'   : BIT_MASK_WALL | BIT_FLAG_NORTH | BIT_FLAG_EAST | BIT_FLAG_SOUTH,
    'WALL_HW'   : BIT_MASK_WALL | BIT_FLAG_NORTH | BIT_FLAG_SOUTH | BIT_FLAG_WEST,
    'WALL_H'    : BIT_MASK_WALL | BIT_FLAG_NORTH | BIT_FLAG_SOUTH,
    'WALL_V'    : BIT_MASK_WALL | BIT_FLAG_EAST | BIT_FLAG_WEST,
    'WALL_NV'   : BIT_MASK_WALL | BIT_FLAG_EAST | BIT_FLAG_SOUTH | BIT_FLAG_WEST,
    'WALL_SV'   : BIT_MASK_WALL | BIT_FLAG_NORTH | BIT_FLAG_EAST | BIT_FLAG_WEST,
}

TILE_VALUE_TO_NAME = {value: key for key, value in TILE_NAME_TO_VALUE.items()}
