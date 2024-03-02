import vampytest
from scarletio import Handle

from ..looping import start_remind_loop


def test__start_remind_loop__not_yet_started():
    """
    Tests whether ``start_remind_loop`` works as intended.
    
    Case: Not yet started.
    """
    step_remind_loop_called = False
    
    def step_remind_loop():
        nonlocal step_remind_loop_called
        step_remind_loop_called = True
    
    handle = None
    
    mocked = vampytest.mock_globals(
        start_remind_loop,
        handle = handle,
        step_remind_loop = step_remind_loop,
    )
    
    mocked()
    
    vampytest.assert_true(step_remind_loop_called)


def test__start_remind_loop__already_started():
    """
    Tests whether ``start_remind_loop`` works as intended.
    
    Case: Already started.
    """
    step_remind_loop_called = False
    
    def step_remind_loop():
        nonlocal step_remind_loop_called
        step_remind_loop_called = True
    
    handle = Handle(lambda : None, None)
    
    mocked = vampytest.mock_globals(
        start_remind_loop,
        handle = handle,
        step_remind_loop = step_remind_loop,
    )
    
    mocked()
    
    vampytest.assert_false(step_remind_loop_called)
