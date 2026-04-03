import vampytest

from ..chapters import CHAPTER_DEFAULT
from ..constants import CHAPTERS, STAGES
from ..helpers import can_play_selected_stage
from ..user_state import StageResult


def _iter_options():
    # Stage id in results.
    for chapter in CHAPTERS.values():
        if chapter is not CHAPTER_DEFAULT:
            break
    
    else:
        raise RuntimeError('Could not detect sufficient chapter.')
    
    stage = STAGES[STAGES[STAGES[chapter.first_stage_id].next_stage_id].next_stage_id]
    
    yield (
        {
            stage.id : StageResult(100, stage.id, 100),
        },
        stage,
        True,
    )
    
    
    # Previous id in results.
    for chapter in CHAPTERS.values():
        if chapter is not CHAPTER_DEFAULT:
            break
    
    else:
        raise RuntimeError('Could not detect sufficient chapter.')
    
    stage = STAGES[STAGES[chapter.first_stage_id].next_stage_id]
    
    yield (
        {
            stage.previous_stage_id : StageResult(100, stage.previous_stage_id, 100),
        },
        stage,
        True,
    )
    
    
    # Non first.
    for chapter in CHAPTERS.values():
        if chapter is not CHAPTER_DEFAULT:
            break
    
    else:
        raise RuntimeError('Could not detect sufficient chapter.')
    
    stage = STAGES[STAGES[chapter.first_stage_id].next_stage_id]
    
    yield (
        {},
        stage,
        False,
    )
    
    
    # First and first chapter
    for chapter in CHAPTERS.values():
        if chapter is not CHAPTER_DEFAULT and chapter.unlock_prerequisite_stage_id == 0:
            break
    
    else:
        raise RuntimeError('Could not detect sufficient chapter.')
    
    stage = STAGES[chapter.first_stage_id]
    
    yield (
        {},
        stage,
        True,
    )
    
    # First and other chapter, but unlocked
    for chapter in CHAPTERS.values():
        if chapter is not CHAPTER_DEFAULT and chapter.unlock_prerequisite_stage_id != 0:
            break
    
    else:
        raise RuntimeError('Could not detect sufficient chapter.')
    
    stage = STAGES[chapter.first_stage_id]
    
    yield (
        {
            
            chapter.unlock_prerequisite_stage_id : StageResult(100, chapter.unlock_prerequisite_stage_id, 100),
        },
        stage,
        True,
    )
    
    # First and other chapter, but not unlocked
    for chapter in CHAPTERS.values():
        if chapter is not CHAPTER_DEFAULT and chapter.unlock_prerequisite_stage_id != 0:
            break
    
    else:
        raise RuntimeError('Could not detect sufficient chapter.')
    
    stage = STAGES[chapter.first_stage_id]
    
    yield (
        {},
        stage,
        False,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__can_play_selected_stage(stage_results, selected_stage):
    """
    Tests whether ``can_play_selected_stage`` works as intended.
    
    Returns
    -------
    stage_results: ``dict<int, StageResult>``
        Result of each completed stage by the user.
    
    selected_stage : ``stage``
        The selected stage by the user.
    
    Returns
    -------
    output : `bool`
    """
    output = can_play_selected_stage(stage_results, selected_stage)
    vampytest.assert_instance(output, bool)
    return output
