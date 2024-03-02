import vampytest
from scarletio import skip_ready_cycle

from ..looping import step_remind_loop


async def test__step_remind_loop():
    """
    Tests whether ``step_remind_loop`` works as intended.
    
    This function is a coroutine.
    """
    remind_forgot_daily_called = False
    
    async def remind_forgot_daily():
        nonlocal remind_forgot_daily_called
        remind_forgot_daily_called = True
    
    handle = None
    
    mocked = vampytest.mock_globals(
        step_remind_loop,
        handle = handle,
        remind_forgot_daily = remind_forgot_daily,
    )
    
    mocked()
    
    await skip_ready_cycle()
    
    handle = mocked.__globals__.get('handle', None)
    vampytest.assert_is_not(handle, None)
    handle.cancel()
    
    vampytest.assert_true(remind_forgot_daily_called)
