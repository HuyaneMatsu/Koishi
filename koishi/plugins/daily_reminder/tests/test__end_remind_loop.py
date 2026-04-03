import vampytest
from scarletio import Handle

from ..looping import end_remind_loop


def test__end_remind_loop__not_yet_started():
    """
    Tests whether ``end_remind_loop`` works as intended.
    
    Case: Not yet started.
    """
    handle = None
    
    mocked = vampytest.mock_globals(
        end_remind_loop,
        handle = handle,
    )
    
    mocked()


def test__end_remind_loop__already_started():
    """
    Tests whether ``end_remind_loop`` works as intended.
    
    Case: Already started.
    """
    handle = Handle(lambda : None, None)
    
    mocked = vampytest.mock_globals(
        end_remind_loop,
        handle = handle,
    )
    
    mocked()
    
    vampytest.assert_true(handle.cancelled)
    
    handle = mocked.__globals__.get('handle', None)
    vampytest.assert_is(handle, None)
