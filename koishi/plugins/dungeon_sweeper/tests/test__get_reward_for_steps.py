import vampytest
from scarletio import Future, get_event_loop

from ..chapters import STAGE_DEFAULT, Stage
from ..helpers import get_reward_for_steps


def _iter_options():
    yield 40, 33, (1750, True)
    yield 40, 40, (750, False)
    yield 40, 47, (500, False)
    yield 40, 54, (400, False)
    yield 40, 61, (300, False)
    yield 40, 68, (200, False)
    yield 40, 75, (100, False)
    yield 40, 82, (100, False)


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_reward_for_steps(best, steps):
    """
    Tests whether ``get_reward_for_steps`` works as intended.
    
    Parameters
    ----------
    best : `int`
        The minimal amount of steps required to defeat the stage.
    
    steps : `int`
        The user's step count.
    
    Returns
    -------
    output : `(int, bool)`
    """
    set_new_best_called = False
    
    stage_id = 999
    
    stage = Stage(
        STAGE_DEFAULT.chapter_id,
        stage_id,
        
        STAGE_DEFAULT.difficulty_id,
        STAGE_DEFAULT.in_difficulty_index,
        STAGE_DEFAULT.next_stage_id,
        STAGE_DEFAULT.previous_stage_id,
        
        best,
        STAGE_DEFAULT.map.copy(),
        STAGE_DEFAULT.size_x,
        STAGE_DEFAULT.start_position,
        STAGE_DEFAULT.target_count,
    )
    
    
    def set_new_best(input_stage, input_steps):
        nonlocal set_new_best_called
        nonlocal stage
        nonlocal steps
        vampytest.assert_is(stage, input_stage)
        vampytest.assert_eq(input_steps, steps)
        set_new_best_called = True
        future = Future(get_event_loop())
        future.set_result(None)
        return future
    
    mocked = vampytest.mock_globals(
        get_reward_for_steps,
        set_new_best = set_new_best,
        STAGES = {
            stage_id : stage,
        }
    )
    
    output = mocked(stage_id, steps)
    vampytest.assert_instance(output, int)
    return output, set_new_best_called
