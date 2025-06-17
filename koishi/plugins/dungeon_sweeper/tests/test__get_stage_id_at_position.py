import vampytest

from ..chapters import CHAPTER_DEFAULT
from ..constants import CHAPTERS
from ..helpers import get_stage_id_at_position
from ..user_state import StageResult


def _iter_options():
    # Has no results at all
    for chapter in CHAPTERS.values():
        if chapter is not CHAPTER_DEFAULT and chapter.unlock_prerequisite_stage_id == 0:
            break
    else:
        raise RuntimeError('Could not find satisfactory chapter.')
    
    yield (
        chapter,
        {},
        2,
        5,
        chapter.first_stage_id,
    )
    
    # Has result, but jump back
    for chapter in CHAPTERS.values():
        if chapter is not CHAPTER_DEFAULT and chapter.unlock_prerequisite_stage_id == 0:
            break
    else:
        raise RuntimeError('Could not find satisfactory chapter.')
    
    stage_0 = chapter.get_first_stage()
    stage_1 = stage_0.get_next_stage()
    stage_2 = stage_1.get_next_stage()
    stage_3 = stage_2.get_next_stage()
    
    yield (
        chapter,
        {
            stage_0.id : StageResult(100, stage_0.id, 50),
            stage_1.id : StageResult(101, stage_1.id, 51),
            stage_2.id : StageResult(102, stage_2.id, 52),
            stage_3.id : StageResult(103, stage_3.id, 53),
        },
        2,
        5,
        stage_3.next_stage_id,
    )

    # Has result, but jump back
    for chapter in CHAPTERS.values():
        if chapter is not CHAPTER_DEFAULT and chapter.unlock_prerequisite_stage_id == 0:
            break
    else:
        raise RuntimeError('Could not find satisfactory chapter.')
    
    stage_0 = chapter.get_first_stage()
    stage_1 = stage_0.get_next_stage()
    stage_2 = stage_1.get_next_stage()
    stage_3 = stage_2.get_next_stage()
    
    yield (
        chapter,
        {
            stage_0.id : StageResult(100, stage_0.id, 50),
            stage_1.id : StageResult(101, stage_1.id, 51),
            stage_2.id : StageResult(102, stage_2.id, 52),
            stage_3.id : StageResult(103, stage_3.id, 53),
        },
        stage_2.difficulty_id,
        stage_2.in_difficulty_index,
        stage_2.id,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_stage_id_at_position(chapter, stage_results, difficulty_id, in_difficulty_index):
    """
    Tries ot get a playable stage identifier close to the given position.
    
    Parameters
    ----------
    chapter : ``Chapter``
        The targeted chapter.
    
    stage_results: ``dict<int, StageResult>``
        Result of each completed stage by the user.
    
    difficulty_id : `int`
        The difficulty's identifier.
    
    in_difficulty_index : `int`
        The index of the chapter in the difficulty.
    
    Returns
    -------
    output : `int`
    """
    output = get_stage_id_at_position(chapter, stage_results, difficulty_id, in_difficulty_index)
    vampytest.assert_instance(output, int)
    return output
