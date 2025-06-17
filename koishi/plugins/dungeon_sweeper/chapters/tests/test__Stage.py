import vampytest

from ...constants import CHAPTERS, STAGES
from ...tile_bit_masks import BIT_MASK_CHARACTER, BIT_FLAG_NORTH, BIT_MASK_TARGET_ON_FLOOR, BIT_MASK_WALL

from ..chapter import Chapter
from ..chapters import CHAPTER_DEFAULT, STAGE_DEFAULT
from ..constants import (
    JSON_KEY_STAGE_BEST, JSON_KEY_STAGE_DIFFICULTY_ID, JSON_KEY_STAGE_ID, JSON_KEY_STAGE_IN_DIFFICULTY_INDEX,
    JSON_KEY_STAGE_MAP, JSON_KEY_STAGE_NEXT_STAGE_ID, JSON_KEY_STAGE_PREVIOUS_STAGE_ID, JSON_KEY_STAGE_SIZE_X,
    JSON_KEY_STAGE_START_POSITION, JSON_KEY_STAGE_TARGET_COUNT, TILE_VALUE_TO_NAME
)
from ..stage import Stage


def _build_default_map():
    """
    Builds a 3x3 map with the character in the middle, unsolvable.
    
    Returns
    -------
    map_ : `list<int>`
    """
    wall = BIT_MASK_WALL | BIT_FLAG_NORTH
    middle = BIT_MASK_CHARACTER | BIT_FLAG_NORTH | BIT_MASK_TARGET_ON_FLOOR
    
    return [wall, wall, wall, wall, middle, wall, wall, wall, wall]


def _assert_fields_set(stage):
    """
    Asserts whether the given stage has all of its fields set.
    
    Parameters
    ----------
    stage : ``Stage``
        The stage to test.
    """
    vampytest.assert_instance(stage, Stage)
    vampytest.assert_instance(stage.best, int)
    vampytest.assert_instance(stage.chapter_id, int)
    vampytest.assert_instance(stage.difficulty_id, int)
    vampytest.assert_instance(stage.id, int)
    vampytest.assert_instance(stage.in_difficulty_index, int)
    vampytest.assert_instance(stage.map, list)
    vampytest.assert_instance(stage.next_stage_id, int)
    vampytest.assert_instance(stage.previous_stage_id, int)
    vampytest.assert_instance(stage.size_x, int)
    vampytest.assert_instance(stage.start_position, int)
    vampytest.assert_instance(stage.target_count, int)


def test__Stage__new():
    """
    Tests whether ``Stage.__new__`` works as intended.
    """
    chapter_id = 999
    stage_id = 998
    
    difficulty_id = 1
    in_difficulty_index = 3
    next_stage_id = 997
    previous_stage_id = 996
    
    best = 99
    map_ = _build_default_map()
    size_x = 3
    start_position = 5
    target_count = 1
    
    
    stage = Stage(
        chapter_id,
        stage_id,
        
        difficulty_id,
        in_difficulty_index,
        next_stage_id,
        previous_stage_id,
        
        best,
        map_,
        size_x,
        start_position,
        target_count,
    )
    _assert_fields_set(stage)
    
    vampytest.assert_eq(stage.chapter_id, chapter_id)
    vampytest.assert_eq(stage.id, stage_id)
    
    vampytest.assert_eq(stage.difficulty_id, difficulty_id)
    vampytest.assert_eq(stage.in_difficulty_index, in_difficulty_index)
    vampytest.assert_eq(stage.next_stage_id, next_stage_id)
    vampytest.assert_eq(stage.previous_stage_id, previous_stage_id)
    
    vampytest.assert_eq(stage.best, best)
    vampytest.assert_eq(stage.map, map_)
    vampytest.assert_eq(stage.size_x, size_x)
    vampytest.assert_eq(stage.start_position, start_position)
    vampytest.assert_eq(stage.target_count, target_count)


def test__Stage__from_data():
    """
    Tests whether ``Stage.from_data`` works as intended.
    """
    chapter_id = 999
    stage_id = 998
    
    difficulty_id = 1
    in_difficulty_index = 3
    next_stage_id = 997
    previous_stage_id = 996
    
    best = 99
    map_ = _build_default_map()
    size_x = 3
    start_position = 5
    target_count = 1
    
    data = {
        JSON_KEY_STAGE_ID : stage_id,
        
        JSON_KEY_STAGE_DIFFICULTY_ID : difficulty_id,
        JSON_KEY_STAGE_IN_DIFFICULTY_INDEX : in_difficulty_index,
        JSON_KEY_STAGE_NEXT_STAGE_ID : next_stage_id,
        JSON_KEY_STAGE_PREVIOUS_STAGE_ID : previous_stage_id,
        
        JSON_KEY_STAGE_BEST : best,
        JSON_KEY_STAGE_MAP : [TILE_VALUE_TO_NAME[value] for value in map_],
        JSON_KEY_STAGE_SIZE_X : size_x,
        JSON_KEY_STAGE_START_POSITION : start_position,
        JSON_KEY_STAGE_TARGET_COUNT : target_count
    }
    
    stage = Stage.from_data(
        chapter_id,
        data,
    )
    _assert_fields_set(stage)
    
    vampytest.assert_eq(stage.chapter_id, chapter_id)
    vampytest.assert_eq(stage.id, stage_id)
    
    vampytest.assert_eq(stage.difficulty_id, difficulty_id)
    vampytest.assert_eq(stage.in_difficulty_index, in_difficulty_index)
    vampytest.assert_eq(stage.next_stage_id, next_stage_id)
    vampytest.assert_eq(stage.previous_stage_id, previous_stage_id)
    
    vampytest.assert_eq(stage.best, best)
    vampytest.assert_eq(stage.map, map_)
    vampytest.assert_eq(stage.size_x, size_x)
    vampytest.assert_eq(stage.start_position, start_position)
    vampytest.assert_eq(stage.target_count, target_count)


def test__Stage__repr():
    """
    Tests whether ``Stage.__repr__`` works as intended.
    """
    chapter_id = 999
    stage_id = 998
    
    difficulty_id = 1
    in_difficulty_index = 3
    next_stage_id = 997
    previous_stage_id = 996
    
    best = 99
    map_ = _build_default_map()
    size_x = 3
    start_position = 5
    target_count = 1
    
    
    stage = Stage(
        chapter_id,
        stage_id,
        
        difficulty_id,
        in_difficulty_index,
        next_stage_id,
        previous_stage_id,
        
        best,
        map_,
        size_x,
        start_position,
        target_count,
    )
    
    output = repr(stage)
    vampytest.assert_instance(output, str)


def _iter_options__get_chapter():
    for chapter in CHAPTERS.values():
        if chapter is not CHAPTER_DEFAULT:
            break
    
    else:
        raise RuntimeError('Could not find non-default chapter.')
    
    yield chapter.id, chapter
    yield 999, CHAPTER_DEFAULT


@vampytest._(vampytest.call_from(_iter_options__get_chapter()).returning_last())
def test__Stage__get_chapter(chapter_id):
    """
    Tests whether ``Stage.get_chapter`` works as intended.
    
    Parameters
    ----------
    chapter_id : `int`
        Chapter identifier.
    
    Returns
    -------
    output : ``Chapter``
    """
    stage_id = 998
    
    difficulty_id = 1
    in_difficulty_index = 3
    next_stage_id = 997
    previous_stage_id = 996
    
    best = 99
    map_ = _build_default_map()
    size_x = 3
    start_position = 5
    target_count = 1
    
    
    stage = Stage(
        chapter_id,
        stage_id,
        
        difficulty_id,
        in_difficulty_index,
        next_stage_id,
        previous_stage_id,
        
        best,
        map_,
        size_x,
        start_position,
        target_count,
    )
    
    output = stage.get_chapter()
    vampytest.assert_instance(output, Chapter)
    return output


def _iter_options__get_previous_stage():
    for stage in STAGES.values():
        if stage is not STAGE_DEFAULT:
            break
    
    else:
        raise RuntimeError('Could not find non-default stage.')
    
    yield stage.id, stage
    yield 998, STAGE_DEFAULT


@vampytest._(vampytest.call_from(_iter_options__get_previous_stage()).returning_last())
def test__Stage__get_previous_stage(previous_stage_id):
    """
    Tests whether ``Stage.get_previous_stage`` works as intended.
    
    Parameters
    ----------
    previous_stage_id : `int`
        Stage identifier.
    
    Returns
    -------
    output : ``None | Stage``
    """
    chapter_id = 999
    stage_id = 998
    
    difficulty_id = 1
    in_difficulty_index = 3
    next_stage_id = 997
    
    best = 99
    map_ = _build_default_map()
    size_x = 3
    start_position = 5
    target_count = 1
    
    
    stage = Stage(
        chapter_id,
        stage_id,
        
        difficulty_id,
        in_difficulty_index,
        next_stage_id,
        previous_stage_id,
        
        best,
        map_,
        size_x,
        start_position,
        target_count,
    )
    
    output = stage.get_previous_stage()
    vampytest.assert_instance(output, Stage, nullable = True)
    return output


def _iter_options__get_next_stage():
    for stage in STAGES.values():
        if stage is not STAGE_DEFAULT:
            break
    
    else:
        raise RuntimeError('Could not find non-default stage.')
    
    yield stage.id, stage
    yield 997, STAGE_DEFAULT


@vampytest._(vampytest.call_from(_iter_options__get_next_stage()).returning_last())
def test__Stage__get_next_stage(next_stage_id):
    """
    Tests whether ``Stage.get_next_stage`` works as intended.
    
    Parameters
    ----------
    next_stage_id : `int`
        Stage identifier.
    
    Returns
    -------
    output : ``None | Stage``
    """
    chapter_id = 999
    stage_id = 998
    
    difficulty_id = 1
    in_difficulty_index = 3
    previous_stage_id = 998
    
    best = 99
    map_ = _build_default_map()
    size_x = 3
    start_position = 5
    target_count = 1
    
    
    stage = Stage(
        chapter_id,
        stage_id,
        
        difficulty_id,
        in_difficulty_index,
        next_stage_id,
        previous_stage_id,
        
        best,
        map_,
        size_x,
        start_position,
        target_count,
    )
    
    output = stage.get_next_stage()
    vampytest.assert_instance(output, Stage, nullable = True)
    return output
