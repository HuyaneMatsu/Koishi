import vampytest
from hata import KOKORO
from scarletio import Task, skip_ready_cycle

from ..constants import GUILD_STATS_CACHE, GUILD_STATS_SAVE_TASKS
from ..queries import guild_stats_save
from ..guild_stats import guild_stats_create


async def test__guild_stats_save__cached():
    """
    Tests whether ``guild_stats_save`` works as intended.
    
    Case: cached.
    """
    guild_id = 202511290000
    
    async def patched_query_guild_stats_save_loop(input_guild_stats):
        nonlocal guild_stats
        vampytest.assert_is(input_guild_stats, guild_stats)
        await skip_ready_cycle()
    
    
    mocked = vampytest.mock_globals(
        guild_stats_save,
        query_guild_stats_save_loop = patched_query_guild_stats_save_loop,
    )
    
    try:
        guild_stats = guild_stats_create(guild_id)
        
        task = Task(KOKORO, mocked(guild_stats))
        await skip_ready_cycle()
        vampytest.assert_in(guild_id, GUILD_STATS_SAVE_TASKS)
        await task
        vampytest.assert_eq(guild_stats.modification_flags, 0)
        
    finally:
        GUILD_STATS_CACHE.clear()
