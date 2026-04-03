import vampytest
from scarletio import Task, get_event_loop, skip_ready_cycle

from ....bot_utils.models import DB_ENGINE

from ..guild_stats import GuildStats
from ..guild_stats_saver import GuildStatsSaver
from ..constants import GUILD_STATS_CACHE


def _assert_fields_set(guild_stats_saver):
    """
    Tests whether every fields are set of the given guild stats saver.
    
    Parameters
    ----------
    guild_stats_saver : ``GuildStatsSaver``
        The instance to check.
    """
    vampytest.assert_instance(guild_stats_saver, GuildStatsSaver)
    vampytest.assert_instance(guild_stats_saver.entry_proxy, GuildStats)
    vampytest.assert_instance(guild_stats_saver.ensured_for_deletion, bool)
    vampytest.assert_instance(guild_stats_saver.modified_fields, dict, nullable = True)
    vampytest.assert_instance(guild_stats_saver.run_task, Task, nullable = True)


def test__GuildStatsSaver__new():
    """
    Tests whether ``GuildStatsSaver.__new__`` works as intended.
    """
    guild_id = 202505070013
    
    try:
        guild_stats = GuildStats(guild_id)
        
        guild_stats_saver = GuildStatsSaver(guild_stats)
        _assert_fields_set(guild_stats_saver)
        
        vampytest.assert_is(guild_stats_saver.entry_proxy, guild_stats)

    finally:
        GUILD_STATS_CACHE.clear()


@vampytest.skip_if(DB_ENGINE is not None)
async def test__GuildStatsSaver__repr():
    """
    Tests whether ``GuildStatsSaver.__repr__`` works as intended.
    
    This function is a coroutine.
    """
    guild_id = 202505070014
    
    old_credibility = 56
    
    new_credibility = 57
    
    try:
        guild_stats = GuildStats(guild_id)
        guild_stats.credibility = old_credibility
        
        ensured_for_deletion = True
        modified_fields = {'credibility': new_credibility}
        
        guild_stats_saver = GuildStatsSaver(guild_stats)
        guild_stats_saver.ensured_for_deletion = ensured_for_deletion
        guild_stats_saver.modified_fields = modified_fields
        guild_stats_saver.run_task = Task(get_event_loop(), guild_stats_saver.run())
        
        output = repr(guild_stats_saver)
        
        vampytest.assert_instance(output, str)
        
        vampytest.assert_in(GuildStatsSaver.__name__, output)
        vampytest.assert_in(f'entry_proxy = {guild_stats!r}', output)
        vampytest.assert_in(f'ensured_for_deletion = {ensured_for_deletion!r}', output)
        vampytest.assert_in(f'modified_fields = {modified_fields!r}', output)
        vampytest.assert_in(f'running = {True!r}', output)
    
    finally:
        GUILD_STATS_CACHE.clear()


def test__GuildStatsSaver__add_modification():
    """
    Tests whether ``GuildStatsSaver.add_modification`` works as intended.
    """
    guild_id = 202412070017
    
    old_credibility = 56
    
    new_credibility = 57
    
    try:
        guild_stats = GuildStats(guild_id)
        guild_stats.credibility = old_credibility
        
        guild_stats_saver = GuildStatsSaver(guild_stats)
        
        vampytest.assert_eq(
            guild_stats_saver.modified_fields,
            None,
        )
        
        guild_stats_saver.add_modification('credibility', new_credibility)
        
        vampytest.assert_eq(
            guild_stats_saver.modified_fields,
            {
                'credibility': new_credibility,
            }
        )
    
    finally:
        GUILD_STATS_CACHE.clear()


def test__GuildStatsSaver__ensure_deletion():
    """
    Tests whether ``GuildStatsSaver.ensure_deletion`` works as intended.
    """
    guild_id = 202505070015
    
    try:
        guild_stats = GuildStats(guild_id)
        
        guild_stats_saver = GuildStatsSaver(guild_stats)
        
        vampytest.assert_eq(guild_stats_saver.ensured_for_deletion, False)
        
        guild_stats_saver.ensure_deletion()
        
        vampytest.assert_eq(guild_stats_saver.ensured_for_deletion, True)
    
    finally:
        GUILD_STATS_CACHE.clear()


def test__GuildStatsSaver__is_modified__not():
    """
    Tests whether ``GuildStatsSaver.is_modified`` works as intended.
    
    Case: not modified.
    """
    guild_id = 202505070016
    
    try:
        guild_stats = GuildStats(guild_id)
        
        guild_stats_saver = GuildStatsSaver(guild_stats)
        
        output = guild_stats_saver.is_modified()
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, False)
    
    finally:
        GUILD_STATS_CACHE.clear()


def test__GuildStatsSaver__is_modified__delete():
    """
    Tests whether ``GuildStatsSaver.is_modified`` works as intended.
    
    Case: ensured for deletion.
    """
    guild_id = 202505070017
    
    try:
        guild_stats = GuildStats(guild_id)
        
        guild_stats_saver = GuildStatsSaver(guild_stats)
        guild_stats_saver.ensure_deletion()
        
        output = guild_stats_saver.is_modified()
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, True)
    
    finally:
        GUILD_STATS_CACHE.clear()


def test__GuildStatsSaver__is_modified__field():
    """
    Tests whether ``GuildStatsSaver.is_modified`` works as intended.
    
    Case: field modified.
    """
    guild_id = 202505070018
    
    old_credibility = 56
    
    new_credibility = 63
    
    try:
        guild_stats = GuildStats(guild_id)
        guild_stats.credibility = old_credibility
        
        guild_stats_saver = GuildStatsSaver(guild_stats)
        guild_stats_saver.add_modification('credibility', new_credibility)
        
        output = guild_stats_saver.is_modified()
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, True)
    
    finally:
        GUILD_STATS_CACHE.clear()


@vampytest.skip_if(DB_ENGINE is not None)
async def test__GuildStatsSaver__begin():
    """
    Tests whether ``GuildStatsSaver.begin`` works as intended.
    
    This function is a coroutine.
    """
    guild_id = 202505070019
    
    try:
        guild_stats = GuildStats(guild_id)
        
        guild_stats_saver = GuildStatsSaver(guild_stats)
        guild_stats.saver = guild_stats_saver
        
        output = guild_stats_saver.begin()
        
        vampytest.assert_instance(output, Task)
        vampytest.assert_is(guild_stats_saver.run_task, output)
        vampytest.assert_is(guild_stats.saver, guild_stats_saver)
        
        # do save
        await skip_ready_cycle()
        await skip_ready_cycle()
        
        # after save nothing should be set.
        vampytest.assert_is(guild_stats_saver.run_task, None)
        vampytest.assert_is(guild_stats.saver, None)
    
    finally:
        GUILD_STATS_CACHE.clear()


@vampytest.skip_if(DB_ENGINE is not None)
async def GuildStatsSaver__running():
    """
    Tests whether ``GuildStatsSaver.running`` works as intended.
    """
    guild_id = 202505070020
    
    try:
        guild_stats = GuildStats(guild_id)
        
        guild_stats_saver = GuildStatsSaver(guild_stats)
        guild_stats.saver = guild_stats_saver
        
        output = guild_stats_saver.running
        vampytest.assert_eq(output, False)
        
        guild_stats_saver.begin()
        
        output = guild_stats_saver.running
        vampytest.assert_eq(output, True)
        
    finally:
        GUILD_STATS_CACHE.clear()
