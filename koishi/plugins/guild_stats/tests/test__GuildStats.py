import vampytest
from scarletio import Task, get_event_loop, skip_ready_cycle

from ....bot_utils.models import DB_ENGINE

from ...quest_core import QuestBatch

from ..constants import GUILD_STATS_CACHE
from ..guild_stats import GuildStats
from ..guild_stats_saver import GuildStatsSaver


def _assert_fields_set(guild_stats):
    """
    Asserts whether every fields are set of the guild stats.
    
    Parameters
    ----------
    guild_stats : ``GuildStats``
        The guild stats to test.
    """
    vampytest.assert_instance(guild_stats, GuildStats)
    vampytest.assert_instance(guild_stats._cache_quest_batch, QuestBatch, nullable = True)
    vampytest.assert_instance(guild_stats.credibility, int)
    vampytest.assert_instance(guild_stats.entry_id, int)
    vampytest.assert_instance(guild_stats.guild_id, int)


def test__GuildStats__new():
    """
    Tests whether ``GuildStats.__new__`` works as intended.
    """
    guild_id = 202505070003
    
    try:
        guild_stats = GuildStats(guild_id)
        _assert_fields_set(guild_stats)
        
        vampytest.assert_eq(guild_stats.guild_id, guild_id)
        
        # Should not auto store in cache
        vampytest.assert_is(GUILD_STATS_CACHE.get(guild_stats.entry_id, None), None)
        
    finally:
        GUILD_STATS_CACHE.clear()


def test__GuildStats__repr():
    """
    Tests whether ``guild_stats.__repr__`` works as intended.
    """
    credibility = 7
    entry_id = 1020
    guild_id = 202505070004
    
    try:
        
        guild_stats = GuildStats(guild_id)
        guild_stats.credibility = credibility
        guild_stats.entry_id = entry_id
        
        guild_stats.entry_id = entry_id
        
        output = repr(guild_stats)
        
        vampytest.assert_instance(output, str)
        
        vampytest.assert_in(GuildStats.__name__, output)
        vampytest.assert_in(f'credibility = {credibility!r}', output)
        vampytest.assert_in(f'entry_id = {entry_id!r}', output)
        vampytest.assert_in(f'guild_id = {guild_id!r}', output)
        
    finally:
        GUILD_STATS_CACHE.clear()


def test__GuildStats__bool():
    """
    Tests whether ``GuildStats.__bool__`` works as intended.
    
    Returns
    -------
    output : `bool`
    """
    guild_id = 202505070005
    
    try:
        guild_stats = GuildStats(guild_id)
        
        output = bool(guild_stats)
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, True)
    
    finally:
        GUILD_STATS_CACHE.clear()


def test__GuildStats__get_saver():
    """
    Tests whether ``GuildStats.get_saver`` works as intended.
    """
    guild_id = 202505070006
    
    try:
        guild_stats = GuildStats(guild_id)
        
        output = guild_stats.get_saver()
        vampytest.assert_instance(output, GuildStatsSaver)
        vampytest.assert_is(output.entry_proxy, guild_stats)
        vampytest.assert_is(guild_stats.saver, output)
    
    finally:
        GUILD_STATS_CACHE.clear()


def test__GuildStats__get_saver__caching():
    """
    Tests whether ``GuildStats.get_saver`` works as intended.
    
    Case: caching.
    """
    guild_id = 202505070007
    
    try:
        guild_stats = GuildStats(guild_id)
        
        output_0 = guild_stats.get_saver()
        output_1 = guild_stats.get_saver()
        vampytest.assert_is(output_0, output_1)
    
    finally:
        GUILD_STATS_CACHE.clear()


def test__GuildStats__from_entry():
    """
    Tests whether ``GuildStats.from_entry`` works as intended.
    """
    credibility = 20
    entry_id = 1021
    guild_id = 202505070008
    
    try:
        entry = {
            'credibility': credibility,
            'id': entry_id,
            'guild_id': guild_id,
        }
        
        guild_stats = GuildStats.from_entry(entry)
        _assert_fields_set(guild_stats)
        
        # Should auto store in cache
        vampytest.assert_is(GUILD_STATS_CACHE.get(guild_id, None), guild_stats)
        
        vampytest.assert_eq(guild_stats.credibility, credibility)
        vampytest.assert_eq(guild_stats.entry_id, entry_id)
        vampytest.assert_eq(guild_stats.guild_id, guild_id)
    
    finally:
        GUILD_STATS_CACHE.clear()


def test__GuildStats__from_entry__cache():
    """
    Tests whether ``GuildStats.from_entry`` works as intended.
    
    Case: Caching.
    """
    credibility = 40
    entry_id = 1022
    guild_id = 202505070009
    
    try:
        guild_stats = GuildStats(guild_id)
        guild_stats.entry_id = entry_id
        GUILD_STATS_CACHE[guild_id] = guild_stats
        
        entry = {
            'credibility': credibility,
            'id': entry_id,
            'guild_id': guild_id,
        }
        
        output = GuildStats.from_entry(entry)
        vampytest.assert_is(output, guild_stats)
        
        vampytest.assert_eq(guild_stats.credibility, credibility)
        vampytest.assert_eq(guild_stats.entry_id, entry_id)
        vampytest.assert_eq(guild_stats.guild_id, guild_id)
    
    finally:
        GUILD_STATS_CACHE.clear()


@vampytest.skip_if(DB_ENGINE is not None)
async def test__GuildStats__delete():
    """
    Tests whether ``GuildStats.delete`` works as intended.
    
    This function is a coroutine.
    """
    guild_id = 202505070010
    entry_id = 1030
    
    try:
        guild_stats = GuildStats(guild_id)
        guild_stats.entry_id = entry_id
        GUILD_STATS_CACHE[guild_id] = guild_stats
        
        vampytest.assert_is(guild_stats.saver, None)
        vampytest.assert_is_not(GUILD_STATS_CACHE.get(guild_id, None), None)
        
        guild_stats.delete()
        
        vampytest.assert_is_not(guild_stats.saver, None)
        vampytest.assert_is(GUILD_STATS_CACHE.get(guild_id, None), None)
        
        await skip_ready_cycle()
        await skip_ready_cycle()
        
        vampytest.assert_is(guild_stats.saver, None)
        vampytest.assert_is(GUILD_STATS_CACHE.get(guild_id, None), None)
    
    finally:
        GUILD_STATS_CACHE.clear()


@vampytest.skip_if(DB_ENGINE is not None)
async def test__GuildStats__set__add_field():
    """
    Tests whether ``GuildStats.set`` works as intended.
    
    This function is a coroutine.
    
    Case: Add field.
    """
    guild_id = 202505070011
    old_credibility = 50
    
    new_credibility = 20
    
    try:
        guild_stats = GuildStats(guild_id)
        guild_stats.credibility = old_credibility
        
        vampytest.assert_is(guild_stats.saver, None)
        vampytest.assert_is(GUILD_STATS_CACHE.get(guild_id, None), None)
        vampytest.assert_eq(guild_stats.credibility, old_credibility)
        
        guild_stats.set('credibility', new_credibility)
        
        vampytest.assert_eq(guild_stats.credibility, new_credibility)
        vampytest.assert_is_not(guild_stats.saver, None)
        vampytest.assert_eq(guild_stats.saver.modified_fields, {'credibility': new_credibility})
        vampytest.assert_is(GUILD_STATS_CACHE.get(guild_id, None), guild_stats)
        
        await skip_ready_cycle()
        await skip_ready_cycle()
        
        vampytest.assert_eq(guild_stats.credibility, new_credibility)
        vampytest.assert_is(guild_stats.saver, None)
        vampytest.assert_is(GUILD_STATS_CACHE.get(guild_id, None), guild_stats)
        
    finally:
        GUILD_STATS_CACHE.clear()


@vampytest.skip_if(DB_ENGINE is not None)
async def test__GuildStats__set__save():
    """
    Tests whether ``GuildStats.save`` works as intended.
    
    This function is a coroutine.
    """
    guild_id = 202505070012
    
    try:
        guild_stats = GuildStats(guild_id)
        
        task = Task(get_event_loop(), guild_stats.save())
        
        await skip_ready_cycle()
        
        vampytest.assert_is_not(guild_stats.saver, None)
        
        task.apply_timeout(0.1)
        await task
        
        key = next(iter(GUILD_STATS_CACHE.keys()), None)
        vampytest.assert_is_not(key, None)
        vampytest.assert_eq(guild_stats.guild_id, key)
        vampytest.assert_is(GUILD_STATS_CACHE.get(key, None), guild_stats)
        
        vampytest.assert_is(guild_stats.saver, None)
        
    finally:
        GUILD_STATS_CACHE.clear()


def test__GuildStats__get_quest_batch():
    """
    Tests whether ``GuildStats.get_quest_batch`` works as intended.
    """
    guild_id = 202505160000
    try:
        guild_stats = GuildStats(guild_id)
        
        quest_batch = guild_stats.get_quest_batch()
        vampytest.assert_instance(quest_batch, QuestBatch)
        vampytest.assert_is(guild_stats._cache_quest_batch, quest_batch)
    
    finally:
        GUILD_STATS_CACHE.clear()
