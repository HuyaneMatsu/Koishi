from os.path import join as join_paths

import vampytest
from scarletio import from_json

from ..chapter import Chapter
from ..constants import (
    CHAPTERS_PATH, JSON_KEY_CHAPTER_DISPLAY_NAME, JSON_KEY_CHAPTER_FIRST_STAGE_ID, JSON_KEY_CHAPTER_ID,
    JSON_KEY_CHAPTER_NEXT_CHAPTER_ID, JSON_KEY_CHAPTER_PREVIOUS_CHAPTER_ID, JSON_KEY_CHAPTER_RULE_ID,
    JSON_KEY_CHAPTER_SKILL_ID, JSON_KEY_CHAPTER_STAGES, JSON_KEY_CHAPTER_STYLE_ID,
    JSON_KEY_CHAPTER_UNLOCK_PREREQUISITE_STAGE_ID, JSON_KEY_STAGE_BEST, JSON_KEY_STAGE_DIFFICULTY_ID,
    JSON_KEY_STAGE_ID, JSON_KEY_STAGE_IN_DIFFICULTY_INDEX, JSON_KEY_STAGE_MAP,
    JSON_KEY_STAGE_NEXT_STAGE_ID, JSON_KEY_STAGE_PREVIOUS_STAGE_ID, JSON_KEY_STAGE_SIZE_X,
    JSON_KEY_STAGE_START_POSITION, JSON_KEY_STAGE_TARGET_COUNT
)
from ..loading_and_saving import set_new_best
from ..stage import Stage

from .test__Stage import _build_default_map


async def test__set_new_best():
    """
    Tests whether ``set_new_best`` works as intended.
    """
    written = None
    new_best = 3
    
    chapter_id = 300
    stage_0_id = 100
    stage_1_id = 200
    
    stage_0_difficulty_id = 1
    stage_0_in_difficulty_index = 0
    stage_0_next_stage_id = 200
    stage_0_previous_stage_id = 0
    
    stage_0_best = 99
    stage_0_map = _build_default_map()
    stage_0_size_x = 3
    stage_0_start_position = 5
    stage_0_target_count = 1
    
    stage_0 = Stage(
        chapter_id,
        stage_0_id,
        
        stage_0_difficulty_id,
        stage_0_in_difficulty_index,
        stage_0_next_stage_id,
        stage_0_previous_stage_id,
        
        stage_0_best,
        stage_0_map,
        stage_0_size_x,
        stage_0_start_position,
        stage_0_target_count,
    )
    
    stage_1_difficulty_id = 1
    stage_1_in_difficulty_index = 1
    stage_1_next_stage_id = 0
    stage_1_previous_stage_id = 100
    
    stage_1_best = 90
    stage_1_map = _build_default_map()
    stage_1_size_x = 3
    stage_1_start_position = 5
    stage_1_target_count = 1
    
    stage_1 = Stage(
        chapter_id,
        stage_1_id,
        
        stage_1_difficulty_id,
        stage_1_in_difficulty_index,
        stage_1_next_stage_id,
        stage_1_previous_stage_id,
        
        stage_1_best,
        stage_1_map,
        stage_1_size_x,
        stage_1_start_position,
        stage_1_target_count,
    )
    
    file_name = 'orin.json'
    
    first_stage_id = 100
    next_chapter_id = 0
    previous_chapter_id = 0
    unlock_prerequisite_stage_id = 0
    
    display_name = 'Orin'
    rule_id = 301
    skill_id = 302
    stages = [stage_0, stage_1]
    style_id = 303
    
    chapter = Chapter(
        file_name,
        chapter_id,
        
        first_stage_id,
        next_chapter_id,
        previous_chapter_id,
        unlock_prerequisite_stage_id,
        
        display_name,
        rule_id,
        skill_id,
        stages,
        style_id,
    )
    
    
    CHAPTERS = {
        chapter_id : chapter,
    }
    
    
    class MockAsyncIO():
        async def __new__(cls, path, mode):
            nonlocal file_name
            
            vampytest.assert_eq(path, join_paths(CHAPTERS_PATH, file_name))
            vampytest.assert_eq(mode, 'w')
            return object.__new__(cls)
        
        
        def __enter__(self):
            return self
        
        
        def __exit__(self, exception_type, exception_value, exception_traceback):
            return False
        
        
        async def write(self, data):
            nonlocal written
            assert written is None
            written = data
            return len(data)
    
    
    get_chapter = Stage.get_chapter
    mocked_get_chapter = vampytest.mock_globals(
        get_chapter,
        CHAPTERS = CHAPTERS,
    )
    
    
    try:
        Stage.get_chapter = mocked_get_chapter
        
        mocked = vampytest.mock_globals(
            set_new_best,
            2,
            AsyncIO = MockAsyncIO,
            
        )
        
        await mocked(stage_1, new_best)
        
    finally:
        Stage.get_chapter = get_chapter
    
    
    vampytest.assert_eq(stage_1.best, new_best)
    
    vampytest.assert_is_not(written, None)
    vampytest.assert_eq(
        written,
        (
            f'{{\n'
            f'    "{JSON_KEY_CHAPTER_ID}": {chapter_id},\n'
            f'    "{JSON_KEY_CHAPTER_UNLOCK_PREREQUISITE_STAGE_ID}": {unlock_prerequisite_stage_id},\n'
            f'    "{JSON_KEY_CHAPTER_FIRST_STAGE_ID}": {first_stage_id},\n'
            f'    "{JSON_KEY_CHAPTER_PREVIOUS_CHAPTER_ID}": {previous_chapter_id},\n'
            f'    "{JSON_KEY_CHAPTER_NEXT_CHAPTER_ID}": {next_chapter_id},\n'
            f'    "{JSON_KEY_CHAPTER_SKILL_ID}": {skill_id},\n'
            f'    "{JSON_KEY_CHAPTER_STYLE_ID}": {style_id},\n'
            f'    "{JSON_KEY_CHAPTER_RULE_ID}": {rule_id},\n'
            f'    "{JSON_KEY_CHAPTER_DISPLAY_NAME}": "{display_name}",\n'
            f'    "{JSON_KEY_CHAPTER_STAGES}": [\n'
            f'        {{\n'
            f'            "{JSON_KEY_STAGE_DIFFICULTY_ID}": {stage_0_difficulty_id},\n'
            f'            "{JSON_KEY_STAGE_IN_DIFFICULTY_INDEX}": {stage_0_in_difficulty_index},\n'
            f'            "{JSON_KEY_STAGE_ID}": {stage_0_id},\n'
            f'            "{JSON_KEY_STAGE_START_POSITION}": {stage_0_start_position},\n'
            f'            "{JSON_KEY_STAGE_TARGET_COUNT}": {stage_0_target_count},\n'
            f'            "{JSON_KEY_STAGE_SIZE_X}": {stage_0_size_x},\n'
            f'            "{JSON_KEY_STAGE_BEST}": {stage_0_best},\n'
            f'            "{JSON_KEY_STAGE_PREVIOUS_STAGE_ID}": {stage_0_previous_stage_id},\n'
            f'            "{JSON_KEY_STAGE_NEXT_STAGE_ID}": {stage_0_next_stage_id},\n'
            f'            "{JSON_KEY_STAGE_MAP}": [\n'
            f'                "WALL_N"    , "WALL_N"    , "WALL_N"    ,\n'
            f'                "WALL_N"    , "CN_TARGET" , "WALL_N"    ,\n'
            f'                "WALL_N"    , "WALL_N"    , "WALL_N"\n'
            f'            ]\n'
            f'        }}, {{\n'
            f'            "{JSON_KEY_STAGE_DIFFICULTY_ID}": {stage_1_difficulty_id},\n'
            f'            "{JSON_KEY_STAGE_IN_DIFFICULTY_INDEX}": {stage_1_in_difficulty_index},\n'
            f'            "{JSON_KEY_STAGE_ID}": {stage_1_id},\n'
            f'            "{JSON_KEY_STAGE_START_POSITION}": {stage_1_start_position},\n'
            f'            "{JSON_KEY_STAGE_TARGET_COUNT}": {stage_1.target_count},\n'
            f'            "{JSON_KEY_STAGE_SIZE_X}": {stage_1_size_x},\n'
            f'            "{JSON_KEY_STAGE_BEST}": {new_best},\n'
            f'            "{JSON_KEY_STAGE_PREVIOUS_STAGE_ID}": {stage_1_previous_stage_id},\n'
            f'            "{JSON_KEY_STAGE_NEXT_STAGE_ID}": {stage_1_next_stage_id},\n'
            f'            "{JSON_KEY_STAGE_MAP}": [\n'
            f'                "WALL_N"    , "WALL_N"    , "WALL_N"    ,\n'
            f'                "WALL_N"    , "CN_TARGET" , "WALL_N"    ,\n'
            f'                "WALL_N"    , "WALL_N"    , "WALL_N"\n'
            f'            ]\n'
            f'        }}\n'
            f'    ]\n'
            f'}}\n'
        ),
    )
    
    output = from_json(written)
    vampytest.assert_eq(
        output,
        {
            JSON_KEY_CHAPTER_ID : chapter_id,
            JSON_KEY_CHAPTER_UNLOCK_PREREQUISITE_STAGE_ID : unlock_prerequisite_stage_id,
            JSON_KEY_CHAPTER_FIRST_STAGE_ID : first_stage_id,
            JSON_KEY_CHAPTER_PREVIOUS_CHAPTER_ID : previous_chapter_id,
            JSON_KEY_CHAPTER_NEXT_CHAPTER_ID : next_chapter_id,
            JSON_KEY_CHAPTER_SKILL_ID : skill_id,
            JSON_KEY_CHAPTER_STYLE_ID : style_id,
            JSON_KEY_CHAPTER_RULE_ID : rule_id,
            JSON_KEY_CHAPTER_DISPLAY_NAME : display_name,
            JSON_KEY_CHAPTER_STAGES : [
                {
                    JSON_KEY_STAGE_DIFFICULTY_ID : stage_0_difficulty_id,
                    JSON_KEY_STAGE_IN_DIFFICULTY_INDEX : stage_0_in_difficulty_index,
                    JSON_KEY_STAGE_ID : stage_0_id,
                    JSON_KEY_STAGE_START_POSITION : stage_0_start_position,
                    JSON_KEY_STAGE_TARGET_COUNT : stage_0_target_count,
                    JSON_KEY_STAGE_SIZE_X : stage_0_size_x,
                    JSON_KEY_STAGE_BEST : stage_0_best,
                    JSON_KEY_STAGE_PREVIOUS_STAGE_ID : stage_0_previous_stage_id,
                    JSON_KEY_STAGE_NEXT_STAGE_ID : stage_0_next_stage_id,
                    JSON_KEY_STAGE_MAP : [
                        'WALL_N', 'WALL_N', 'WALL_N',
                        'WALL_N', 'CN_TARGET', 'WALL_N',
                        'WALL_N', 'WALL_N', 'WALL_N',
                    ],
                }, {
                    JSON_KEY_STAGE_DIFFICULTY_ID : stage_1_difficulty_id,
                    JSON_KEY_STAGE_IN_DIFFICULTY_INDEX : stage_1_in_difficulty_index,
                    JSON_KEY_STAGE_ID : stage_1_id,
                    JSON_KEY_STAGE_START_POSITION : stage_1_start_position,
                    JSON_KEY_STAGE_TARGET_COUNT : stage_1_target_count,
                    JSON_KEY_STAGE_SIZE_X : stage_1_size_x,
                    JSON_KEY_STAGE_BEST : new_best,
                    JSON_KEY_STAGE_PREVIOUS_STAGE_ID : stage_1_previous_stage_id,
                    JSON_KEY_STAGE_NEXT_STAGE_ID : stage_1_next_stage_id,
                    JSON_KEY_STAGE_MAP : [
                        'WALL_N', 'WALL_N', 'WALL_N',
                        'WALL_N', 'CN_TARGET', 'WALL_N',
                        'WALL_N', 'WALL_N', 'WALL_N',
                    ],
                },
            ],
        },
    )
