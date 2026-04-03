__all__ = ('CHAPTER_FLANDRE', 'CHAPTER_DEFAULT', 'CHAPTER_REIMU', 'CHAPTER_YUKARI', 'STAGE_DEFAULT')

from scarletio import export

from ..chapter_rules import CHAPTER_RULE_DEFAULT
from ..chapter_styles import CHAPTER_STYLE_DEFAULT
from ..constants import CHAPTERS, STAGES
from ..skills import SKILL_DEFAULT
from ..tile_bit_masks import BIT_MASK_CHARACTER, BIT_FLAG_NORTH, BIT_MASK_TARGET_ON_FLOOR, BIT_MASK_WALL

from .chapter import Chapter
from .constants import CHAPTER_ID_DEFAULT, FILE_NAME_FLANDRE, FILE_NAME_REIMU, FILE_NAME_YUKARI, STAGE_ID_DEFAULT
from .loading_and_saving import load_chapter_data
from .stage import Stage


STAGE_DEFAULT = STAGES[STAGE_ID_DEFAULT] = Stage(
    CHAPTER_ID_DEFAULT,
    STAGE_ID_DEFAULT,
    
    0,
    0,
    0,
    0,
    
    9999,
    [
        BIT_MASK_WALL | BIT_FLAG_NORTH,
        BIT_MASK_WALL | BIT_FLAG_NORTH,
        BIT_MASK_WALL | BIT_FLAG_NORTH,
        BIT_MASK_WALL | BIT_FLAG_NORTH,
        BIT_MASK_CHARACTER | BIT_FLAG_NORTH | BIT_MASK_TARGET_ON_FLOOR,
        BIT_MASK_WALL | BIT_FLAG_NORTH,
        BIT_MASK_WALL | BIT_FLAG_NORTH,
        BIT_MASK_WALL | BIT_FLAG_NORTH,
        BIT_MASK_WALL | BIT_FLAG_NORTH,
    ],
    3,
    5,
    1,
)


CHAPTER_DEFAULT = CHAPTERS[CHAPTER_ID_DEFAULT] = Chapter(
    None,
    CHAPTER_ID_DEFAULT,
    
    CHAPTER_ID_DEFAULT,
    0,
    0,
    0,
    
    'unknown',
    CHAPTER_RULE_DEFAULT.id,
    SKILL_DEFAULT.id,
    [
        STAGE_DEFAULT,
    ],
    CHAPTER_STYLE_DEFAULT.id,
)


CHAPTER_REIMU = Chapter.from_data(FILE_NAME_REIMU, load_chapter_data(FILE_NAME_REIMU))
CHAPTERS[CHAPTER_REIMU.id] = CHAPTER_REIMU

CHAPTER_FLANDRE = Chapter.from_data(FILE_NAME_FLANDRE, load_chapter_data(FILE_NAME_FLANDRE))
CHAPTERS[CHAPTER_FLANDRE.id] = CHAPTER_FLANDRE

CHAPTER_YUKARI = Chapter.from_data(FILE_NAME_YUKARI, load_chapter_data(FILE_NAME_YUKARI))
CHAPTERS[CHAPTER_YUKARI.id] = CHAPTER_YUKARI


# Register the stages

for chapter in CHAPTERS.values():
    for stage in chapter.stages:
        STAGES[stage.id] = stage

del chapter
del stage

export(STAGE_DEFAULT, 'STAGE_DEFAULT')
export(CHAPTER_DEFAULT, 'CHAPTER_DEFAULT')
