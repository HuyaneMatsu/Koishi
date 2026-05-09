from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from hata import KOKORO
from scarletio import Task

from ..constants import USER_STATS_CACHE, USER_STATS
from ..queries import get_user_stats
from ..user_stats import UserStats


async def test__get_stats__cached():
    """
    Tests whether ``get_stats`` works as intended.
    
    Case: cached.
    """
    user_id_0 = 20250310030
    user_id_1 = 20250310031
    
    async def mocked_query_get_user_stats(user_id):
        raise RuntimeError
    
    
    mocked = vampytest.mock_globals(
        get_user_stats,
        query_get_user_stats = mocked_query_get_user_stats,
        recursion = 2
    )
    
    try:
        user_stats_0 = UserStats(user_id_0)
        user_stats_1 = UserStats(user_id_1)
        
        USER_STATS_CACHE[user_id_0] = user_stats_0
        USER_STATS_CACHE[user_id_1] = user_stats_1
        
        USER_STATS[user_id_0] = user_stats_0
        USER_STATS[user_id_1] = user_stats_1
        
        vampytest.assert_eq(
            [*USER_STATS_CACHE.keys()],
            [user_id_0, user_id_1],
        )
        
        output = await mocked(user_id_0)
        vampytest.assert_instance(output, UserStats)
        vampytest.assert_is(output, user_stats_0)
        
        vampytest.assert_eq(
            [*USER_STATS_CACHE.keys()],
            [user_id_1, user_id_0],
        )
        vampytest.assert_eq(
            {*USER_STATS.keys()},
            {user_id_1, user_id_0},
        )
        
    finally:
        USER_STATS_CACHE.clear()


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
    recovering_until_notification_at = recovering_until
    
    item_id_costume = 2
    item_id_head = 3
    item_id_species = 4
    item_id_weapon = 5
    
    entry_id = 3502
    
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
        'recovering_until_notification_at': recovering_until_notification_at.replace(tzinfo = None),
        
        'item_id_costume': item_id_costume,
        'item_id_head': item_id_head,
        'item_id_species': item_id_species,
        'item_id_weapon': item_id_weapon,
    }
    
    async def mocked_query_get_user_stats(input_user_id):
        nonlocal entry
        nonlocal user_id
        
        vampytest.assert_eq(input_user_id, user_id)
        return entry
    
    
    mocked = vampytest.mock_globals(
        get_user_stats,
        query_get_user_stats = mocked_query_get_user_stats,
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
            [*USER_STATS_CACHE.keys()],
            [],
        )
        
        vampytest.assert_eq(
            {*USER_STATS.keys()},
            set(),
        )
        
        output_0 = await task_0
        output_1 = await task_1
        
        vampytest.assert_is_not(output_0, None)
        vampytest.assert_is(output_1, output_0)
        
        vampytest.assert_eq(
            [*USER_STATS_CACHE.keys()],
            [user_id],
        )
        vampytest.assert_eq(
            {*USER_STATS.keys()},
            {user_id},
        )
    
    finally:
        USER_STATS_CACHE.clear()
        if (task_0 is not None):
            task_0.cancel()
        
        if (task_1 is not None):
            task_1.cancel()
