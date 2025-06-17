import vampytest
from scarletio import Future, get_event_loop

from ..chapters import STAGE_DEFAULT, Stage
from ..helpers import get_reward_difference


def _iter_options():
    yield 40, 100, 33, (1650, True)
    yield 40, 100, 40, (650, False)
    yield 40, 100, 47, (400, False)
    yield 40, 100, 54, (300, False)
    yield 40, 100, 61, (200, False)
    yield 40, 100, 68, (100, False)
    yield 40, 100, 75, (0, False)
    yield 40, 100, 82, (0, False)
    
    yield 40, 50, 40, (350, False)


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_reward_difference(best, old_steps, new_steps):
    """
    Tests whether ``get_reward_difference`` works as intended.
    
    Parameters
    ----------
    best : `int`
        The minimal amount of steps required to defeat the stage.
    
    old_steps : `int`
        The old amount of steps.
    
    new_steps : `int`
        The new amount of steps.
    
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
        nonlocal new_steps
        vampytest.assert_is(stage, input_stage)
        vampytest.assert_eq(input_steps, new_steps)
        set_new_best_called = True
        future = Future(get_event_loop())
        future.set_result(None)
        return future
    
    mocked = vampytest.mock_globals(
        get_reward_difference,
        set_new_best = set_new_best,
        STAGES = {
            stage_id : stage,
        }
    )
    
    output = mocked(stage_id, old_steps, new_steps)
    vampytest.assert_instance(output, int)
    return output, set_new_best_called
