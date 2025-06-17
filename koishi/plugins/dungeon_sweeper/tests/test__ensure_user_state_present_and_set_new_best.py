import vampytest

from ....bot_utils.models import DB_ENGINE

from ...user_balance import UserBalance

from ..chapters import STAGE_DEFAULT, Stage
from ..helpers import ensure_user_state_present_and_set_new_best
from ..user_state import UserState


@vampytest.skip_if(DB_ENGINE is not None)
async def test__ensure_user_state_present_and_set_new_best():
    """
    Tests whether ``ensure_user_state_present_and_set_new_best`` works as intended.
    """
    stage_id = 999
    best = 40
    steps = 50
    
    
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
    
    ensure_user_state_created_called = False
    save_stage_result_called = False
    get_user_balance_called = False
    
    user_id = 202506150000
    
    user_state = UserState(user_id)
    user_balance = UserBalance(user_id)
    
    
    async def ensure_user_state_created(input_user_state):
        nonlocal user_state
        nonlocal ensure_user_state_created_called
        vampytest.assert_is(input_user_state, user_state)
        ensure_user_state_created_called = True
    
    
    async def save_stage_result(input_user_id, input_stage_result):
        nonlocal user_id
        nonlocal stage_id
        nonlocal steps
        nonlocal save_stage_result_called
        
        vampytest.assert_eq(input_user_id, user_id)
        vampytest.assert_eq(input_stage_result.stage_id, stage_id)
        vampytest.assert_eq(input_stage_result.best, steps)
        save_stage_result_called = True
    
    
    async def get_user_balance(input_user_id):
        nonlocal user_id
        nonlocal get_user_balance_called
        nonlocal user_balance
        
        vampytest.assert_eq(input_user_id, user_id)
        get_user_balance_called = True
        return user_balance
    
    
    mocked = vampytest.mock_globals(
        ensure_user_state_present_and_set_new_best,
        2,
        ensure_user_state_created = ensure_user_state_created,
        save_stage_result = save_stage_result,
        get_user_balance = get_user_balance,
        STAGES = {
            stage_id: stage,
        },
    )
    
    await mocked(user_state, stage_id, steps)
    
    
    vampytest.assert_true(ensure_user_state_created_called)
    vampytest.assert_true(save_stage_result_called)
    vampytest.assert_true(get_user_balance_called)
    vampytest.assert_eq(user_balance.balance, 400)
