from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from scarletio import Task, get_event_loop, skip_ready_cycle

from ....bot_utils.models import DB_ENGINE

from ..constants import STATS_CACHE
from ..user_stats import UserStats
from ..user_stats_calculated import UserStatsCalculated
from ..user_stats_saver import UserStatsSaver


def _assert_fields_set(stats):
    """
    Asserts whether every fields are set of the stats.
    
    Parameters
    ----------
    stats : ``UserStats``
        UserStats to test.
    """
    vampytest.assert_instance(stats, UserStats)
    vampytest.assert_instance(stats._cache_stats_calculated, UserStatsCalculated, nullable = True)
    vampytest.assert_instance(stats.entry_id, int)
    vampytest.assert_instance(stats.credibility, int)
    vampytest.assert_instance(stats.item_id_costume, int)
    vampytest.assert_instance(stats.item_id_head, int)
    vampytest.assert_instance(stats.item_id_species, int)
    vampytest.assert_instance(stats.item_id_weapon, int)
    vampytest.assert_instance(stats.recovering_until, DateTime, nullable = True)
    vampytest.assert_instance(stats.stat_bedroom, int)
    vampytest.assert_instance(stats.stat_charm, int)
    vampytest.assert_instance(stats.stat_cuteness, int)
    vampytest.assert_instance(stats.stat_housewife, int)
    vampytest.assert_instance(stats.stat_loyalty, int)
    vampytest.assert_instance(stats.user_id, int)


def test__UserStats__new():
    """
    Tests whether ``UserStats.__new__`` works as intended.
    """
    user_id = 20250310008
    
    try:
        stats = UserStats(user_id)
        _assert_fields_set(stats)
        
        # Should not auto store in cache
        vampytest.assert_is(STATS_CACHE.get(stats.user_id, None), None)
        
    finally:
        STATS_CACHE.clear()


def test__UserStats__repr():
    """
    Tests whether ``stats.__repr__`` works as intended.
    """
    user_id = 20250310009
    entry_id = 19999
    
    try:
        stats = UserStats(user_id)
        
        stats.entry_id = entry_id
        
        output = repr(stats)
        
        vampytest.assert_instance(output, str)
        
        vampytest.assert_in(UserStats.__name__, output)
        vampytest.assert_in(f'entry_id = {entry_id!r}', output)
        vampytest.assert_in(f'user_id = {user_id!r}', output)
        
    finally:
        STATS_CACHE.clear()


def test__UserStats__bool():
    """
    Tests whether ``UserStats.__bool__`` works as intended.
    
    Returns
    -------
    output : `bool`
    """
    user_id = 20250310010
    
    try:
        stats = UserStats(user_id)
        
        output = bool(stats)
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, True)
    
    finally:
        STATS_CACHE.clear()


def test__UserStats__get_saver():
    """
    Tests whether ``UserStats.get_saver`` works as intended.
    """
    user_id = 20250310011
    
    try:
        stats = UserStats(user_id)
        
        output = stats.get_saver()
        vampytest.assert_instance(output, UserStatsSaver)
        vampytest.assert_is(output.entry_proxy, stats)
        vampytest.assert_is(stats.saver, output)
    
    finally:
        STATS_CACHE.clear()


def test__UserStats__get_saver__caching():
    """
    Tests whether ``UserStats.get_saver`` works as intended.
    
    Case: caching.
    """
    user_id = 20250310012
    
    try:
        stats = UserStats(user_id)
        
        output_0 = stats.get_saver()
        output_1 = stats.get_saver()
        vampytest.assert_is(output_0, output_1)
    
    finally:
        STATS_CACHE.clear()


def test__UserStats__from_entry():
    """
    Tests whether ``UserStats.from_entry`` works as intended.
    """
    user_id = 20250310013
    
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
    
    entry_id = 3501
    
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
    
    try:
        stats = UserStats.from_entry(entry)
        _assert_fields_set(stats)
        
        # Should auto store in cache
        vampytest.assert_is(STATS_CACHE.get(user_id, None), stats)
        
        vampytest.assert_eq(stats.entry_id, entry_id)
        vampytest.assert_eq(stats.user_id, user_id)
        
        vampytest.assert_eq(stats.stat_housewife, stat_housewife)
        vampytest.assert_eq(stats.stat_cuteness, stat_cuteness)
        vampytest.assert_eq(stats.stat_bedroom, stat_bedroom)
        vampytest.assert_eq(stats.stat_charm, stat_charm)
        vampytest.assert_eq(stats.stat_loyalty, stat_loyalty)
        
        vampytest.assert_eq(stats.credibility, credibility)
        vampytest.assert_eq(stats.recovering_until, recovering_until)
        
        vampytest.assert_eq(stats.item_id_costume, item_id_costume)
        vampytest.assert_eq(stats.item_id_head, item_id_head)
        vampytest.assert_eq(stats.item_id_species, item_id_species)
        vampytest.assert_eq(stats.item_id_weapon, item_id_weapon)
    
    finally:
        STATS_CACHE.clear()


def test__UserStats__from_entry__cache():
    """
    Tests whether ``UserStats.from_entry`` works as intended.
    
    Case: Caching.
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
    
    entry = {
        'id': entry_id,
        'user_id': user_id,
        
        'stat_housewife': stat_housewife,
        'stat_cuteness': stat_cuteness,
        'stat_bedroom': stat_bedroom,
        'stat_charm': stat_charm,
        'stat_loyalty': stat_loyalty,
        
        'credibility': credibility,
        'recovering_until': recovering_until.replace(tzinfo = TimeZone.utc),
        
        'item_id_costume': item_id_costume,
        'item_id_head': item_id_head,
        'item_id_species': item_id_species,
        'item_id_weapon': item_id_weapon,
    }
    
    try:
        stats = UserStats(user_id)
        stats.user_id = user_id
        stats.entry_id = entry_id
        STATS_CACHE[user_id] = stats
        
        output = UserStats.from_entry(entry)
        vampytest.assert_is(output, stats)
        
        vampytest.assert_eq(stats.entry_id, entry_id)
        vampytest.assert_eq(stats.user_id, user_id)
        
        vampytest.assert_eq(stats.stat_housewife, stat_housewife)
        vampytest.assert_eq(stats.stat_cuteness, stat_cuteness)
        vampytest.assert_eq(stats.stat_bedroom, stat_bedroom)
        vampytest.assert_eq(stats.stat_charm, stat_charm)
        vampytest.assert_eq(stats.stat_loyalty, stat_loyalty)
        
        vampytest.assert_eq(stats.credibility, credibility)
        vampytest.assert_eq(stats.recovering_until, recovering_until)
        
        vampytest.assert_eq(stats.item_id_costume, item_id_costume)
        vampytest.assert_eq(stats.item_id_head, item_id_head)
        vampytest.assert_eq(stats.item_id_species, item_id_species)
        vampytest.assert_eq(stats.item_id_weapon, item_id_weapon)
        
    finally:
        STATS_CACHE.clear()


@vampytest.skip_if(DB_ENGINE is not None)
async def test__UserStats__delete():
    """
    Tests whether ``UserStats.delete`` works as intended.
    
    This function is a coroutine.
    """
    user_id = 20250310015
    
    try:
        stats = UserStats(user_id)
        STATS_CACHE[user_id] = stats
        
        vampytest.assert_is(stats.saver, None)
        vampytest.assert_is_not(STATS_CACHE.get(user_id, None), None)
        
        stats.delete()
        
        vampytest.assert_is_not(stats.saver, None)
        vampytest.assert_is(STATS_CACHE.get(user_id, None), None)
        
        await skip_ready_cycle()
        await skip_ready_cycle()
        
        vampytest.assert_is(stats.saver, None)
        vampytest.assert_is(STATS_CACHE.get(user_id, None), None)
    
    finally:
        STATS_CACHE.clear()


@vampytest.skip_if(DB_ENGINE is not None)
async def test__UserStats__set__add_field():
    """
    Tests whether ``UserStats.set`` works as intended.
    
    This function is a coroutine.
    
    Case: Add field.
    """
    user_id = 20250310016
    
    new_stat_bedroom = 2002
    
    try:
        stats = UserStats(user_id)
        vampytest.assert_is(stats.saver, None)
        vampytest.assert_is(STATS_CACHE.get(user_id, None), None)
        vampytest.assert_ne(stats.stat_bedroom, new_stat_bedroom)
        
        stats.set('stat_bedroom', new_stat_bedroom)
        
        vampytest.assert_eq(stats.stat_bedroom, new_stat_bedroom)
        vampytest.assert_is_not(stats.saver, None)
        vampytest.assert_eq(stats.saver.modified_fields, {'stat_bedroom': new_stat_bedroom})
        vampytest.assert_is(STATS_CACHE.get(user_id, None), stats)
        
        await skip_ready_cycle()
        await skip_ready_cycle()
        
        vampytest.assert_eq(stats.stat_bedroom, new_stat_bedroom)
        vampytest.assert_is(stats.saver, None)
        vampytest.assert_is(STATS_CACHE.get(user_id, None), stats)
        
    finally:
        STATS_CACHE.clear()


@vampytest.skip_if(DB_ENGINE is not None)
async def test__UserStats__set__save():
    """
    Tests whether ``UserStats.save`` works as intended.
    
    This function is a coroutine.
    """
    user_id = 20250310017
    
    try:
        stats = UserStats(user_id)
        
        
        task = Task(get_event_loop(), stats.save())
        
        await skip_ready_cycle()
        
        vampytest.assert_is_not(stats.saver, None)
        
        task.apply_timeout(0.1)
        await task
        
        key = next(iter(STATS_CACHE.keys()), None)
        vampytest.assert_is_not(key, None)
        vampytest.assert_eq(stats.user_id, key)
        vampytest.assert_is(STATS_CACHE.get(key, None), stats)
        
        vampytest.assert_is(stats.saver, None)
        
    finally:
        STATS_CACHE.clear()


@vampytest.skip_if(DB_ENGINE is not None)
async def test__UserStats__set__stats_calculated_reset():
    """
    Tests whether ``UserStats.set`` works as intended.
    
    This function is a coroutine.
    
    Case: UserStats calculated reset.
    """
    user_id = 202503230003
    
    new_stat_bedroom = 2002
    
    try:
        stats = UserStats(user_id)
        stats.stats_calculated
        
        stats.set('stat_bedroom', new_stat_bedroom)
        
        vampytest.assert_is(stats._cache_stats_calculated, None)
        
    finally:
        STATS_CACHE.clear()


def test__UserStats__stats_calculated():
    """
    Tests whether ``UserStats.stats_calculated`` works as intended.
    """
    user_id = 202503230002
    
    try:
        stats = UserStats(user_id)
        _assert_fields_set(stats)
        
        output = stats.stats_calculated
        vampytest.assert_instance(output, UserStatsCalculated)
        vampytest.assert_is(stats._cache_stats_calculated, output)
        
    finally:
        STATS_CACHE.clear()
