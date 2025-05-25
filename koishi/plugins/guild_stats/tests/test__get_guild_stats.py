import vampytest
from hata import KOKORO
from scarletio import Future, Task, skip_ready_cycle

from ..constants import GUILD_STATS_CACHE, GUILD_STATS_QUERY_TASKS
from ..queries import get_guild_stats
from ..guild_stats import GuildStats


async def test__get_guild_stats__cached():
    """
    Tests whether ``get_guild_stats`` works as intended.
    
    Case: cached.
    """
    guild_id_0 = 202505070000
    guild_id_1 = 202505070001
    
    async def mocked_query_guild_stats(guild_id, waiters):
        raise RuntimeError
    
    
    mocked = vampytest.mock_globals(
        get_guild_stats,
        query_guild_stats = mocked_query_guild_stats,
        recursion = 2
    )
    
    try:
        guild_stats_0 = GuildStats(guild_id_0)
        guild_stats_1 = GuildStats(guild_id_1)
        
        GUILD_STATS_CACHE[guild_id_0] = guild_stats_0
        GUILD_STATS_CACHE[guild_id_1] = guild_stats_1
        
        vampytest.assert_eq(
            [*GUILD_STATS_CACHE.keys()],
            [guild_id_0, guild_id_1],
        )
        
        output = await mocked(guild_id_0)
        vampytest.assert_instance(output, GuildStats)
        vampytest.assert_is(output, guild_stats_0)
        
        vampytest.assert_eq(
            [*GUILD_STATS_CACHE.keys()],
            [guild_id_1, guild_id_0],
        )
        
    finally:
        GUILD_STATS_CACHE.clear()


async def test__get_guild_stats__request():
    """
    Tests whether ``get_guild_stats`` works as intended.
    
    Case: requesting.
    """
    credibility = 50
    entry_id = 1100
    guild_id = 202505070002
    
    guild_stats = None
    
    entry = {
        'credibility': credibility,
        'id': entry_id,
        'guild_id': guild_id,
    }
    
    async def mocked_query_guild_stats(input_guild_id, waiters):
        nonlocal entry
        nonlocal guild_id
        nonlocal guild_stats
        
        try:
            vampytest.assert_eq(input_guild_id, guild_id)
            vampytest.assert_instance(waiters, list)
            for element in waiters:
                vampytest.assert_instance(element, Future)
            
            guild_stats = GuildStats.from_entry(entry)
            for waiter in waiters:
                waiter.set_result_if_pending(guild_stats)
        finally:
            try:
                del GUILD_STATS_QUERY_TASKS[guild_id]
            except KeyError:
                pass
    
    
    mocked = vampytest.mock_globals(
        get_guild_stats,
        query_guild_stats = mocked_query_guild_stats,
        recursion = 2
    )
    
    task_0 = None
    task_1 = None
    
    try:
        task_0 = Task(KOKORO, mocked(guild_id))
        task_0.apply_timeout(0.1)
        task_1 = Task(KOKORO, mocked(guild_id))
        task_1.apply_timeout(0.1)
        
        vampytest.assert_eq(
            [*GUILD_STATS_CACHE.keys()],
            [],
        )
        
        vampytest.assert_false(GUILD_STATS_QUERY_TASKS)
        
        await skip_ready_cycle()
        
        vampytest.assert_true(GUILD_STATS_QUERY_TASKS)
        
        output_0 = await task_0
        output_1 = await task_1
        
        vampytest.assert_is_not(guild_stats, None)
        vampytest.assert_is(guild_stats, output_0)
        vampytest.assert_is(guild_stats, output_1)
        
        vampytest.assert_eq(
            [*GUILD_STATS_CACHE.keys()],
            [guild_id],
        )
        vampytest.assert_false(GUILD_STATS_QUERY_TASKS)
        
    finally:
        GUILD_STATS_CACHE.clear()
        GUILD_STATS_QUERY_TASKS.clear()
        
        if (task_0 is not None):
            task_0.cancel()
        
        if (task_1 is not None):
            task_1.cancel()
