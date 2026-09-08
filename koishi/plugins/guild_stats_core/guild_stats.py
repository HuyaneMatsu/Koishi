__all__ = (
    'GuildStats', 'guild_stats_create', 'guild_stats_create_from_entry', 'guild_stats_generate_quest_batch',
    'guild_stats_modify_credibility_by',
)

from scarletio import RichAttributeErrorBaseType

from ..quest_core import get_guild_adventurer_rank_info, quest_batch_create, get_current_batch_id


GUILD_STATS_MODIFICATION_FLAG_CREDIBILITY = 1 << 0


class GuildStats(RichAttributeErrorBaseType):
    """
    Represents a guild's stats.
    
    Attributes
    ----------
    _cache_quest_batch : ``None | QuestBatch``
        The guild's current quest batch.
    
    credibility : `int`
        How much the credibility the guild has. Higher credibility means more stats and harder stats.
    
    entry_id : `int`
        The entry's identifier in the database.
    
    guild_id : `int`
        The parent guild's identifier.
    
    modification_flags : `int`
        Bit flags describing which fields were modified.
    """
    __slots__ = ('__weakref__', '_cache_quest_batch', 'credibility', 'entry_id', 'guild_id', 'modification_flags')
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # entry_id
        entry_id = self.entry_id
        if entry_id != 0:
            repr_parts.append(' entry_id = ')
            repr_parts.append(repr(entry_id))
            repr_parts.append(',')
        
        # guild_id
        repr_parts.append(' guild_id = ')
        repr_parts.append(repr(self.guild_id))
        
        # credibility
        credibility = self.credibility
        if credibility:
            repr_parts.append(', credibility = ')
            repr_parts.append(repr(credibility))
        
        repr_parts.append('>')
        return ''.join(repr_parts)


def guild_stats_create(guild_id):
    """
    Creates a new guild stats.
    
    Parameters
    ----------
    guild_id : `int`
        The parent guild identifier.
    
    Returns
    -------
    guild_stats : ``GuildStats``
    """
    guild_stats = object.__new__(GuildStats)
    guild_stats._cache_quest_batch = None
    guild_stats.credibility = 0
    guild_stats.entry_id = 0
    guild_stats.guild_id = guild_id
    guild_stats.modification_flags = 0
    return guild_stats


def guild_stats_create_from_entry(entry):
    """
    Creates a new guild stats from the given entry.
    
    Parameters
    ----------
    entry : `sqlalchemy.engine.result.RowProxy`
        The entry to create the instance based on.
    
    Returns
    -------
    guild_stats : ``GuildStats``
    """
    guild_stats = object.__new__(GuildStats)
    guild_stats._cache_quest_batch = None
    guild_stats.credibility = entry['credibility']
    guild_stats.entry_id = entry['id']
    guild_stats.guild_id = entry['guild_id']
    guild_stats.modification_flags = 0
    return guild_stats


def guild_stats_generate_quest_batch(guild_stats):
    """
    Gets the guild's current quest's batch.
    
    Parameters
    ----------
    guild_stats : ``GuildStats``
        Guild stats to work with.
    
    Returns
    -------
    quest_batch : ``QuestBatch``
    """
    batch_id = get_current_batch_id()
    quest_batch = guild_stats._cache_quest_batch
    
    if (quest_batch is None) or (quest_batch.id != batch_id):
        adventurer_rank_info = get_guild_adventurer_rank_info(guild_stats.credibility)
        quest_batch = quest_batch_create(
            guild_stats.guild_id, batch_id, adventurer_rank_info.level, adventurer_rank_info.quest_limit
        )
        guild_stats._cache_quest_batch = quest_batch
    
    return quest_batch


def guild_stats_modify_credibility_by(guild_stats, value):
    """
    Modifies the credibility of the guild stats.
    
    Parameters
    ----------
    guild_stats : ``GuildStats``
        Guild stats to modify.
    
    value : `int`
        value to modify by.
    """
    guild_stats.credibility = max(guild_stats.credibility + value, 0)
    guild_stats.modification_flags |= GUILD_STATS_MODIFICATION_FLAG_CREDIBILITY


def guild_stats_collect_modifications(guild_stats):
    """
    Collects the modifications done to the guild stats.
    
    Parameters
    ----------
    guild_stats : ``GuildStats``
        The guild stats to collect of.
    
    Returns
    -------
    modifications : `None | dict<str, object>`
    """
    modification_flags = guild_stats.modification_flags
    if not modification_flags:
        return None
    
    guild_stats.modification_flags = 0
    
    modifications = {}
    
    if modification_flags & GUILD_STATS_MODIFICATION_FLAG_CREDIBILITY:
        modifications['credibility'] = guild_stats.credibility
    
    return modifications
