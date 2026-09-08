import vampytest
from hata import KOKORO
from scarletio import Task, skip_ready_cycle

from ..constants import USER_BALANCE_CACHE, USER_BALANCE_SAVE_TASKS
from ..queries import user_balance_save
from ..user_balance import user_balance_create


async def test__user_balance_save__cached():
    """
    Tests whether ``user_balance_save`` works as intended.
    
    Case: cached.
    """
    user_id = 202511130000
    
    async def patched_query_user_balance_save_loop(input_user_balance):
        nonlocal user_balance
        vampytest.assert_is(input_user_balance, user_balance)
        await skip_ready_cycle()
    
    
    mocked = vampytest.mock_globals(
        user_balance_save,
        query_user_balance_save_loop = patched_query_user_balance_save_loop,
    )
    
    try:
        user_balance = user_balance_create(user_id)
        
        task = Task(KOKORO, mocked(user_balance))
        await skip_ready_cycle()
        vampytest.assert_in(user_id, USER_BALANCE_SAVE_TASKS)
        await task
        vampytest.assert_is(user_balance.modification_flags, 0)
        
    finally:
        USER_BALANCE_CACHE.clear()
