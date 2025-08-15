from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from hata import KOKORO
from scarletio import Task

from ..constants import STATS_CACHE
from ..queries import get_user_stats
from ..user_stats import UserStats


async def test__get_stats__cached():
    """
    Tests whether ``get_stats`` works as intended.
    
    Case: cached.
    """
    user_id_0 = 20250310030
    user_id_1 = 20250310031
    
    async def mocked_query_stats(user_id):
        raise RuntimeError
    
    
    mocked = vampytest.mock_globals(
        get_user_stats,
        query_stats = mocked_query_stats,
        recursion = 2
    )
    
    try:
        stats_0 = UserStats(user_id_0)
        stats_1 = UserStats(user_id_1)
        
        STATS_CACHE[user_id_0] = stats_0
        STATS_CACHE[user_id_1] = stats_1
        
        vampytest.assert_eq(
            [*STATS_CACHE.keys()],
            [user_id_0, user_id_1],
        )
        
        output = await mocked(user_id_0)
        vampytest.assert_instance(output, UserStats)
        vampytest.assert_is(output, stats_0)
        
        vampytest.assert_eq(
            [*STATS_CACHE.keys()],
            [user_id_1, user_id_0],
        )
        
    finally:
        STATS_CACHE.clear()


async def test__get_stats__request():
    """
    Tests whether ``get_stats`` works as intended.
    
    Case: requesting.
    """
    user_id = 20250310014
    
    stat_housewife = 11
    stat_cuteness = 12
    stat_bedroom = 13
    stat_charm = 14
    stat_loyalty = 15
    
    credibility = 12222
    recovering_until = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    item_id_costume = 2
    item_id_head = 3
    item_id_species = 4
    item_id_weapon = 5
    
    entry_id = 3502
    
    stats = None
    
    entry = {
        'id': entry_id,
        'user_id': user_id,
        
        'stat_housewife': stat_housewife,
        'stat_cuteness': stat_cuteness,
        'stat_bedroom': stat_bedroom,
        'stat_charm': stat_charm,
        'stat_loyalty': stat_loyalty,
        
        'credibility': credibility,
        'recovering_until': recovering_until.replace(tzinfo = None),
        
        'item_id_costume': item_id_costume,
        'item_id_head': item_id_head,
        'item_id_species': item_id_species,
        'item_id_weapon': item_id_weapon,
    }
    
    async def mocked_query_stats(input_user_id):
        nonlocal entry
        nonlocal user_id
        nonlocal stats
        
        vampytest.assert_eq(input_user_id, user_id)
        stats = UserStats.from_entry(entry)
        return stats
    
    
    mocked = vampytest.mock_globals(
        get_user_stats,
        query_stats = mocked_query_stats,
        recursion = 2
    )
    
    task_0 = None
    task_1 = None
    
    try:
        task_0 = Task(KOKORO, mocked(user_id))
        task_0.apply_timeout(0.1)
        task_1 = Task(KOKORO, mocked(user_id))
        task_1.apply_timeout(0.1)
        
        vampytest.assert_eq(
            [*STATS_CACHE.keys()],
            [],
        )
        
        output_0 = await task_0
        output_1 = await task_1
        
        vampytest.assert_is_not(stats, None)
        vampytest.assert_is(stats, output_0)
        vampytest.assert_is(stats, output_1)
        
        vampytest.assert_eq(
            [*STATS_CACHE.keys()],
            [user_id],
        )
    finally:
        STATS_CACHE.clear()
        if (task_0 is not None):
            task_0.cancel()
        
        if (task_1 is not None):
            task_1.cancel()
