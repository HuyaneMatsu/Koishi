import vampytest
from hata import KOKORO
from scarletio import Task, skip_ready_cycle

from ..constants import USER_BALANCE_CACHE, USER_BALANCE_SAVE_TASKS
from ..queries import save_user_balance
from ..user_balance import UserBalance


async def test__save_user_balance__cached():
    """
    Tests whether ``save_user_balance`` works as intended.
    
    Case: cached.
    """
    user_id = 202511130000
    
    async def patched_query_save_user_balance_loop(input_user_balance):
        nonlocal user_balance
        vampytest.assert_is(input_user_balance, user_balance)
        await skip_ready_cycle()
    
    
    mocked = vampytest.mock_globals(
        save_user_balance,
        query_save_user_balance_loop = patched_query_save_user_balance_loop,
    )
    
    try:
        user_balance = UserBalance(user_id)
        
        task = Task(KOKORO, mocked(user_balance))
        await skip_ready_cycle()
        vampytest.assert_in(user_id, USER_BALANCE_SAVE_TASKS)
        await task
        vampytest.assert_is(user_balance.modified_fields, None)
        
    finally:
        USER_BALANCE_CACHE.clear()
