import vampytest

from ..chapters import CHAPTER_DEFAULT
from ..constants import CHAPTERS, STAGES
from ..helpers import get_selectable_stages
from ..user_state import StageResult


def _iter_options():
    # First stage
    for chapter in CHAPTERS.values():
        if chapter is not CHAPTER_DEFAULT:
            break
    
    else:
        raise RuntimeError('Could not detect sufficient chapter.')
    
    stage = STAGES[chapter.first_stage_id]
    
    yield (
        {},
        stage,
        [
            (stage, -1, True),
        ],
    )
    
    
    # Has up and down
    
    # First stage
    for chapter in CHAPTERS.values():
        if chapter is not CHAPTER_DEFAULT:
            break
    
    else:
        raise RuntimeError('Could not detect sufficient chapter.')
    
    stage_0 = STAGES[chapter.first_stage_id]
    stage_1 = STAGES[stage_0.next_stage_id]
    stage_2 = STAGES[stage_1.next_stage_id]
    stage_3 = STAGES[stage_2.next_stage_id]
    stage_4 = STAGES[stage_3.next_stage_id]
    stage_5 = STAGES[stage_4.next_stage_id]
    stage_6 = STAGES[stage_5.next_stage_id]
    stage_7 = STAGES[stage_6.next_stage_id]
    stage_8 = STAGES[stage_7.next_stage_id]
    
    yield (
        {
            stage_0.id: StageResult(100, stage_0.id, 50),
            stage_1.id: StageResult(101, stage_1.id, 51),
            stage_2.id: StageResult(102, stage_2.id, 52),
            stage_3.id: StageResult(103, stage_3.id, 53),
            stage_4.id: StageResult(104, stage_1.id, 54),
            stage_5.id: StageResult(105, stage_1.id, 55),
            stage_6.id: StageResult(106, stage_1.id, 56),
            stage_7.id: StageResult(107, stage_1.id, 57),
            stage_8.id: StageResult(108, stage_1.id, 58),
        },
        stage_4,
        [
            (stage_7, 57, False),
            (stage_6, 56, False),
            (stage_5, 55, False),
            (stage_4, 54, True),
            (stage_3, 53, False),
            (stage_2, 52, False),
            (stage_1, 51, False),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_selectable_stages(stage_results, selected_stage):
    """
    Tests whether ``get_selectable_stages`` works as intended.
    
    Returns
    -------
    stage_results: ``dict<int, StageResult>``
        Result of each completed stage by the user.
    
    selected_stage : ``stage``
        The selected stage by the user.
    
    Returns
    -------
    output : ``list<(Stage, int, bool)>``
    """
    output = get_selectable_stages(stage_results, selected_stage)
    vampytest.assert_instance(output, list)
    return output
