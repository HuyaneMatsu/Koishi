import vampytest

from ...quest_core import QuestBatch

from ..guild_stats import (
    GUILD_STATS_MODIFICATION_FLAG_CREDIBILITY, GuildStats, guild_stats_collect_modifications, guild_stats_create,
    guild_stats_create_from_entry, guild_stats_generate_quest_batch, guild_stats_modify_credibility_by
)


def assert_guild_stat_fields_set(guild_stats):
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
    vampytest.assert_instance(guild_stats.modification_flags, int)


def test__GuildStats__repr():
    """
    Tests whether ``GuildStats.__repr__`` works as intended.
    """
    credibility = 7
    entry_id = 1020
    guild_id = 202505070004
    
    guild_stats = guild_stats_create(guild_id)
    guild_stats.credibility = credibility
    guild_stats.entry_id = entry_id
    
    output = repr(guild_stats)
    
    vampytest.assert_instance(output, str)
    
    vampytest.assert_in(GuildStats.__name__, output)
    vampytest.assert_in(f'credibility = {credibility!r}', output)
    vampytest.assert_in(f'entry_id = {entry_id!r}', output)
    vampytest.assert_in(f'guild_id = {guild_id!r}', output)


def test__guild_stats_create():
    """
    Tests whether ``guild_stats_create`` works as intended.
    """
    guild_id = 202505070003
    
    guild_stats = guild_stats_create(guild_id)
    assert_guild_stat_fields_set(guild_stats)
    
    vampytest.assert_eq(guild_stats.guild_id, guild_id)


def test__guild_stats_create_from_entry():
    """
    Tests whether ``guild_stats_create_from_entry`` works as intended.
    
    Case: Caching.
    """
    credibility = 40
    entry_id = 1022
    guild_id = 202505070009
    
    entry = {
        'credibility': credibility,
        'id': entry_id,
        'guild_id': guild_id,
    }
    
    guild_stats = guild_stats_create_from_entry(entry)
    assert_guild_stat_fields_set(guild_stats)
    
    vampytest.assert_eq(guild_stats.credibility, credibility)
    vampytest.assert_eq(guild_stats.entry_id, entry_id)
    vampytest.assert_eq(guild_stats.guild_id, guild_id)


def test__guild_stats_generate_quest_batch():
    """
    Tests whether ``guild_stats_generate_quest_batch`` works as intended.
    """
    guild_id = 202505160000
    
    guild_stats = guild_stats_create(guild_id)
    
    quest_batch = guild_stats_generate_quest_batch(guild_stats)
    vampytest.assert_instance(quest_batch, QuestBatch)
    vampytest.assert_is(guild_stats._cache_quest_batch, quest_batch)


def test__guild_stats_modify_credibility_by():
    """
    Tests whether ``guild_stats_modify_credibility_by`` works as intended.
    """
    current = 10
    amount = 2
    
    guild_stats = guild_stats_create(202608300020)
    guild_stats.credibility = current
    guild_stats_modify_credibility_by(guild_stats, amount)
    
    vampytest.assert_eq(guild_stats.credibility, current + amount)
    vampytest.assert_true(guild_stats.modification_flags & GUILD_STATS_MODIFICATION_FLAG_CREDIBILITY)


def test__guild_stats_collect_modifications():
    """
    Tests whether ``guild_stats_collect_modifications`` works as intended.
    """
    guild_stats = guild_stats_create(202608300021)
    
    amount = 20
    guild_stats_modify_credibility_by(guild_stats, amount)
    
    output = guild_stats_collect_modifications(guild_stats)
    vampytest.assert_eq(
        output,
        {
            'credibility': amount,
        },
    )
    vampytest.assert_eq(guild_stats.modification_flags, 0)
