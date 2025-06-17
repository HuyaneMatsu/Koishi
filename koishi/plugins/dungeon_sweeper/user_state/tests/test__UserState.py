from itertools import count

import vampytest

from ...chapters import STAGE_DEFAULT, Stage
from ...constants import STAGES

from ..game_state import GameState
from ..stage_result import StageResult
from ..user_state import UserState


def _assert_fields_set(user_state):
    """
    Asserts whether the user state has all of its fields set.
    
    Parameters
    ----------
    user_state : ``UserState``
    """
    vampytest.assert_instance(user_state, UserState)
    vampytest.assert_instance(user_state.entry_id, int)
    vampytest.assert_instance(user_state.game_state, GameState, nullable = True)
    vampytest.assert_instance(user_state.selected_stage_id, int)
    vampytest.assert_instance(user_state.stage_results, dict)
    vampytest.assert_instance(user_state.user_id, int)


def test__UserState__new():
    """
    Tests whether ``UserState.__new__`` works as intended.
    """
    user_id = 202506140000
    
    user_state = UserState(user_id)
    _assert_fields_set(user_state)
    
    vampytest.assert_eq(user_state.user_id, user_id)


def test__UserState__repr():
    """
    Tests whether ``UserState.__repr__`` works as intended.
    """
    user_id = 202506140001
    
    user_state = UserState(user_id)
    
    output = repr(user_state)
    vampytest.assert_instance(output, str)


def test__UserState__from_entry():
    """
    Tests whether ``UserState.from_entry`` works as intended.
    """
    user_id = 202506140002
    game_state = None
    selected_stage_id = 3
    entry_id = 122
    
    stage_results = [
        StageResult(stage_result_entry_id, stage_id, 100)
        for stage_id, stage_result_entry_id in zip(range(1, selected_stage_id), count(56))
    ]
    
    assert game_state is None
    ds_entry = {
        'user_id': user_id,
        'game_state': None,
        'selected_stage_id': selected_stage_id,
        'id': entry_id
    }
    
    ds_result_entries = [
        {
            'user_id': user_id,
            'stage_id': stage_result.stage_id,
            'id': stage_result.entry_id,
            'best': stage_result.best,
        }
        for stage_result in stage_results
    ]
    
    user_state = UserState.from_entry(ds_entry, ds_result_entries)
    _assert_fields_set(user_state)
    
    vampytest.assert_eq(user_state.user_id, user_id)
    assert game_state is None
    vampytest.assert_is(user_state.game_state, None)
    vampytest.assert_eq(user_state.selected_stage_id, selected_stage_id)
    vampytest.assert_eq(user_state.entry_id, entry_id)
    vampytest.assert_eq(
        user_state.stage_results,
        {stage_result.stage_id: stage_result for stage_result in stage_results},
    )


def test__UserState__get_game_state_data__has():
    """
    Tests whether ``UserState.get_game_state_data`` works as intended.
    
    Case: has.
    """
    user_id = 202506140003
    
    game_state = GameState(STAGE_DEFAULT, -1)
    game_state.next_skill = True
    
    user_state = UserState(user_id)
    user_state.game_state = game_state
    
    output = user_state.get_game_state_data()
    vampytest.assert_instance(output, bytes, nullable = True)
    vampytest.assert_is_not(output, None)
    

def test__UserState__get_game_state_data__none():
    """
    Tests whether ``UserState.get_game_state_data`` works as intended.
    
    Case: none.
    """
    user_id = 202506140004
    game_state = None
    
    user_state = UserState(user_id)
    user_state.game_state = game_state
    
    output = user_state.get_game_state_data()
    vampytest.assert_instance(output, bytes, nullable = True)
    vampytest.assert_is(output, None)
    

def test__UserState__get_selected_stage__default():
    """
    Tests whether ``UserState.get_selected_stage`` works as intended.
    
    Case: default.
    """
    user_id = 202506140005
    
    user_state = UserState(user_id)
    
    output = user_state.get_selected_stage()
    vampytest.assert_instance(output, Stage)
    vampytest.assert_eq(output.id, 1)


def test__UserState__get_selected_stage__set():
    """
    Tests whether ``UserState.get_selected_stage`` works as intended.
    
    Case: set.
    """
    selected_stage_id = 10
    assert selected_stage_id in STAGES
    user_id = 202506140006
    
    user_state = UserState(user_id)
    user_state.selected_stage_id = selected_stage_id
    
    output = user_state.get_selected_stage()
    vampytest.assert_instance(output, Stage)
    vampytest.assert_eq(output.id, selected_stage_id)


def test__UserState__get_selected_stage__unknown():
    """
    Tests whether ``UserState.get_selected_stage`` works as intended.
    
    Case: unknown.
    """
    selected_stage_id = 99999
    assert selected_stage_id not in STAGES
    user_id = 202506140007
    
    user_state = UserState(user_id)
    user_state.selected_stage_id = selected_stage_id
    
    output = user_state.get_selected_stage()
    vampytest.assert_instance(output, Stage)
    vampytest.assert_eq(output.id, 1)
