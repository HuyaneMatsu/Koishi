import vampytest
from hata import KOKORO
from scarletio import Task, skip_ready_cycle

from ..constants import USER_STATS_CACHE, USER_STATS_SAVE_TASKS
from ..queries import user_stats_save
from ..user_stats import user_stats_create


async def test__user_stats_save__cached():
    """
    Tests whether ``user_stats_save`` works as intended.
    
    Case: cached.
    """
    user_id = 202511290000
    
    async def patched_query_user_stats_save_loop(input_user_stats):
        nonlocal user_stats
        vampytest.assert_is(input_user_stats, user_stats)
        await skip_ready_cycle()
    
    
    mocked = vampytest.mock_globals(
        user_stats_save,
        query_user_stats_save_loop = patched_query_user_stats_save_loop,
    )
    
    try:
        user_stats = user_stats_create(user_id)
        
        task = Task(KOKORO, mocked(user_stats))
        await skip_ready_cycle()
        vampytest.assert_in(user_id, USER_STATS_SAVE_TASKS)
        await task
        vampytest.assert_eq(user_stats.modification_flags, 0)
        
    finally:
        USER_STATS_CACHE.clear()
