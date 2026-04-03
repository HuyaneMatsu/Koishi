import vampytest
from hata import KOKORO
from scarletio import Task, skip_ready_cycle

from ..constants import USER_STATS_CACHE, USER_STATS_SAVE_TASKS
from ..queries import save_user_stats
from ..user_stats import UserStats


async def test__save_user_stats__cached():
    """
    Tests whether ``save_user_stats`` works as intended.
    
    Case: cached.
    """
    user_id = 202511290000
    
    async def patched_query_save_user_stats_loop(input_user_stats):
        nonlocal user_stats
        vampytest.assert_is(input_user_stats, user_stats)
        await skip_ready_cycle()
    
    
    mocked = vampytest.mock_globals(
        save_user_stats,
        query_save_user_stats_loop = patched_query_save_user_stats_loop,
    )
    
    try:
        user_stats = UserStats(user_id)
        
        task = Task(KOKORO, mocked(user_stats))
        await skip_ready_cycle()
        vampytest.assert_in(user_id, USER_STATS_SAVE_TASKS)
        await task
        vampytest.assert_is(user_stats.modified_fields, None)
        
    finally:
        USER_STATS_CACHE.clear()
