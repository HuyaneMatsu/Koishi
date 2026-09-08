import vampytest
from hata import KOKORO
from scarletio import Task

from ..constants import GUILD_STATS_CACHE, GUILD_STATS
from ..queries import guild_stats_get
from ..guild_stats import GuildStats, guild_stats_create


async def test__get_stats__cached():
    """
    Tests whether ``get_stats`` works as intended.
    
    Case: cached.
    """
    guild_id_0 = 202608300000
    guild_id_1 = 202608300001
    
    async def mocked_query_guild_stats_get(guild_id):
        raise RuntimeError
    
    
    mocked = vampytest.mock_globals(
        guild_stats_get,
        query_guild_stats_get = mocked_query_guild_stats_get,
        recursion = 2
    )
    
    try:
        guild_stats_0 = guild_stats_create(guild_id_0)
        guild_stats_1 = guild_stats_create(guild_id_1)
        
        GUILD_STATS_CACHE[guild_id_0] = guild_stats_0
        GUILD_STATS_CACHE[guild_id_1] = guild_stats_1
        
        GUILD_STATS[guild_id_0] = guild_stats_0
        GUILD_STATS[guild_id_1] = guild_stats_1
        
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
        vampytest.assert_eq(
            {*GUILD_STATS.keys()},
            {guild_id_1, guild_id_0},
        )
        
    finally:
        GUILD_STATS_CACHE.clear()


async def test__get_stats__request():
    """
    Tests whether ``get_stats`` works as intended.
    
    Case: requesting.
    """
    guild_id = 202608300002
    
    credibility = 12222
    
    entry_id = 3502
    
    entry = {
        'id': entry_id,
        'guild_id': guild_id,
        
        'credibility': credibility,
    }
    
    async def mocked_query_guild_stats_get(input_guild_id):
        nonlocal entry
        nonlocal guild_id
        
        vampytest.assert_eq(input_guild_id, guild_id)
        return entry
    
    
    mocked = vampytest.mock_globals(
        guild_stats_get,
        query_guild_stats_get = mocked_query_guild_stats_get,
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
        
        vampytest.assert_eq(
            {*GUILD_STATS.keys()},
            set(),
        )
        
        output_0 = await task_0
        output_1 = await task_1
        
        vampytest.assert_is_not(output_0, None)
        vampytest.assert_is(output_1, output_0)
        
        vampytest.assert_eq(
            [*GUILD_STATS_CACHE.keys()],
            [guild_id],
        )
        vampytest.assert_eq(
            {*GUILD_STATS.keys()},
            {guild_id},
        )
    
    finally:
        GUILD_STATS_CACHE.clear()
        if (task_0 is not None):
            task_0.cancel()
        
        if (task_1 is not None):
            task_1.cancel()
