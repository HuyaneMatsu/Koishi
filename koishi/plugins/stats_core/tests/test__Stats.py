import vampytest
from scarletio import Task, get_event_loop, skip_ready_cycle

from ....bot_utils.models import DB_ENGINE

from ..constants import STATS_CACHE
from ..stats import Stats
from ..stats_saver import StatsSaver


def _assert_fields_set(stats):
    """
    Asserts whether every fields are set of the stats.
    
    Parameters
    ----------
    stats : ``Stats``
        Stats to test.
    """
    vampytest.assert_instance(stats, Stats)
    vampytest.assert_instance(stats.entry_id, int)
    vampytest.assert_instance(stats.experience, int)
    vampytest.assert_instance(stats.level, int)
    vampytest.assert_instance(stats.raw_costume, bytes)
    vampytest.assert_instance(stats.raw_species, bytes)
    vampytest.assert_instance(stats.raw_weapon, bytes)
    vampytest.assert_instance(stats.stat_bedroom, int)
    vampytest.assert_instance(stats.stat_charm, int)
    vampytest.assert_instance(stats.stat_cuteness, int)
    vampytest.assert_instance(stats.stat_housewife, int)
    vampytest.assert_instance(stats.stat_loyalty, int)
    vampytest.assert_instance(stats.user_id, int)


def test__Stats__new():
    """
    Tests whether ``Stats.__new__`` works as intended.
    """
    user_id = 20250310008
    
    try:
        stats = Stats(user_id)
        _assert_fields_set(stats)
        
        # Should not auto store in cache
        vampytest.assert_is(STATS_CACHE.get(stats.user_id, None), None)
        
    finally:
        STATS_CACHE.clear()


def test__Stats__repr():
    """
    Tests whether ``stats.__repr__`` works as intended.
    """
    user_id = 20250310009
    entry_id = 19999
    
    try:
        stats = Stats(user_id)
        
        stats.entry_id = entry_id
        
        output = repr(stats)
        
        vampytest.assert_instance(output, str)
        
        vampytest.assert_in(Stats.__name__, output)
        vampytest.assert_in(f'entry_id = {entry_id!r}', output)
        vampytest.assert_in(f'user_id = {user_id!r}', output)
        
    finally:
        STATS_CACHE.clear()


def test__Stats__bool():
    """
    Tests whether ``Stats.__bool__`` works as intended.
    
    Returns
    -------
    output : `bool`
    """
    user_id = 20250310010
    
    try:
        stats = Stats(user_id)
        
        output = bool(stats)
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, True)
    
    finally:
        STATS_CACHE.clear()


def test__Stats__get_saver():
    """
    Tests whether ``Stats.get_saver`` works as intended.
    """
    user_id = 20250310011
    
    try:
        stats = Stats(user_id)
        
        output = stats.get_saver()
        vampytest.assert_instance(output, StatsSaver)
        vampytest.assert_is(output.entry_proxy, stats)
        vampytest.assert_is(stats.saver, output)
    
    finally:
        STATS_CACHE.clear()


def test__Stats__get_saver__caching():
    """
    Tests whether ``Stats.get_saver`` works as intended.
    
    Case: caching.
    """
    user_id = 20250310012
    
    try:
        stats = Stats(user_id)
        
        output_0 = stats.get_saver()
        output_1 = stats.get_saver()
        vampytest.assert_is(output_0, output_1)
    
    finally:
        STATS_CACHE.clear()


def test__Stats__from_entry():
    """
    Tests whether ``Stats.from_entry`` works as intended.
    """
    user_id = 20250310013
    
    stat_housewife = 11
    stat_cuteness = 12
    stat_bedroom = 13
    stat_charm = 14
    stat_loyalty = 15
    
    level = 25
    experience = 12222
    
    raw_species = b'a'
    raw_weapon = b'b'
    raw_costume = b'c'
    
    entry_id = 3501
    
    try:
        entry = {
            'id': entry_id,
            'user_id': user_id,
            
            'stat_housewife': stat_housewife,
            'stat_cuteness': stat_cuteness,
            'stat_bedroom': stat_bedroom,
            'stat_charm': stat_charm,
            'stat_loyalty': stat_loyalty,
            
            'level': level,
            'experience': experience,
            
            'raw_species': raw_species,
            'raw_weapon': raw_weapon,
            'raw_costume': raw_costume,
        }
        
        stats = Stats.from_entry(entry)
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
        vampytest.assert_eq(stats.level, level)
        vampytest.assert_eq(stats.experience, experience)
        vampytest.assert_eq(stats.raw_species, raw_species)
        vampytest.assert_eq(stats.raw_weapon, raw_weapon)
        vampytest.assert_eq(stats.raw_costume, raw_costume)
    
    finally:
        STATS_CACHE.clear()


def test__Stats__from_entry__cache():
    """
    Tests whether ``Stats.from_entry`` works as intended.
    
    Case: Caching.
    """
    user_id = 20250310014
    
    stat_housewife = 11
    stat_cuteness = 12
    stat_bedroom = 13
    stat_charm = 14
    stat_loyalty = 15
    
    level = 25
    experience = 12222
    
    raw_species = b'a'
    raw_weapon = b'b'
    raw_costume = b'c'
    
    entry_id = 3502
    
    try:
        stats = Stats(user_id)
        stats.user_id = user_id
        stats.entry_id = entry_id
        STATS_CACHE[user_id] = stats
        
        entry = {
            'id': entry_id,
            'user_id': user_id,
            
            'stat_housewife': stat_housewife,
            'stat_cuteness': stat_cuteness,
            'stat_bedroom': stat_bedroom,
            'stat_charm': stat_charm,
            'stat_loyalty': stat_loyalty,
            
            'level': level,
            'experience': experience,
            
            'raw_species': raw_species,
            'raw_weapon': raw_weapon,
            'raw_costume': raw_costume,
        }
        
        output = Stats.from_entry(entry)
        vampytest.assert_is(output, stats)
        
        vampytest.assert_eq(stats.entry_id, entry_id)
        vampytest.assert_eq(stats.user_id, user_id)
        vampytest.assert_eq(stats.stat_housewife, stat_housewife)
        vampytest.assert_eq(stats.stat_cuteness, stat_cuteness)
        vampytest.assert_eq(stats.stat_bedroom, stat_bedroom)
        vampytest.assert_eq(stats.stat_charm, stat_charm)
        vampytest.assert_eq(stats.stat_loyalty, stat_loyalty)
        vampytest.assert_eq(stats.level, level)
        vampytest.assert_eq(stats.experience, experience)
        vampytest.assert_eq(stats.raw_species, raw_species)
        vampytest.assert_eq(stats.raw_weapon, raw_weapon)
        vampytest.assert_eq(stats.raw_costume, raw_costume)
        
    finally:
        STATS_CACHE.clear()


@vampytest.skip_if(DB_ENGINE is not None)
async def test__Stats__delete():
    """
    Tests whether ``Stats.delete`` works as intended.
    
    This function is a coroutine.
    """
    user_id = 20250310015
    
    try:
        stats = Stats(user_id)
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
async def test__Stats__set__add_field():
    """
    Tests whether ``Stats.set`` works as intended.
    
    This function is a coroutine.
    
    Case: Add field.
    """
    user_id = 20250310016
    
    new_stat_bedroom = 2002
    
    try:
        stats = Stats(user_id)
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
async def test__Stats__set__save():
    """
    Tests whether ``Stats.save`` works as intended.
    
    This function is a coroutine.
    """
    user_id = 20250310017
    
    try:
        stats = Stats(user_id)
        
        
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
