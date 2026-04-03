__all__ = ('GuildStats',)

from scarletio import copy_docs

from ...bot_utils.entry_proxy import EntryProxy

from ..quest_core import get_guild_adventurer_rank_info, create_quest_batch, get_current_batch_id

from .guild_stats_saver import GuildStatsSaver
from .constants import GUILD_STATS_CACHE, GUILD_STATS_CACHE_SIZE


class GuildStats(EntryProxy):
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
    
    saver : ``None | GuildStatsSaver``
        Saver set while saving.
    """
    __slots__ = ('_cache_quest_batch', 'credibility', 'guild_id')
    
    saver_type = GuildStatsSaver
    
    
    def __new__(cls, guild_id):
        """
        Creates a new guild stats.
        
        Parameters
        ----------
        guild_id : `int`
            The parent guild identifier.
        """
        self = object.__new__(cls)
        self._cache_quest_batch = None
        self.credibility = 0
        self.entry_id = 0
        self.guild_id = guild_id
        self.saver = None
        return self
    
    
    @copy_docs(EntryProxy._put_repr_parts)
    def _put_repr_parts(self, repr_parts, field_added):
        if field_added:
            repr_parts.append(',')
        
        # guild_id
        repr_parts.append(' guild_id = ')
        repr_parts.append(repr(self.guild_id))
        
        # credibility
        credibility = self.credibility
        if credibility:
            repr_parts.append(', credibility = ')
            repr_parts.append(repr(credibility))
    
    
    async def save(self):
        """
        Saves the entry and then caches it.
        
        This function is a coroutine.
        """
        saver = self.get_saver()
        await saver.begin()
        self._store_in_cache()
    
    
    @copy_docs(EntryProxy._store_in_cache)
    def _store_in_cache(self):
        guild_id = self.guild_id
        if guild_id in GUILD_STATS_CACHE:
            GUILD_STATS_CACHE.move_to_end(guild_id)
        else:
            GUILD_STATS_CACHE[guild_id] = self
            
            if len(GUILD_STATS_CACHE) > GUILD_STATS_CACHE_SIZE:
                del GUILD_STATS_CACHE[next(iter(GUILD_STATS_CACHE))]
    
    
    @copy_docs(EntryProxy._pop_from_cache)
    def _pop_from_cache(self):
        try:
            del GUILD_STATS_CACHE[self.guild_id]
        except KeyError:
            pass
    
    
    @classmethod
    @copy_docs(EntryProxy.from_entry)
    def from_entry(cls, entry):
        guild_id = entry['guild_id']
        
        try:
            self = GUILD_STATS_CACHE[guild_id]
        except KeyError:
            self = object.__new__(cls)
            self._cache_quest_batch = None
            self.guild_id = guild_id
            self.saver = None
            GUILD_STATS_CACHE[guild_id] = self
        
        self.entry_id = entry['id']
        self.credibility = entry['credibility']
        
        return self
    
    
    def get_quest_batch(self):
        """
        Gets the guild's current quest's batch.
        
        Returns
        -------
        quest_batch : ``QuestBatch``
        """
        batch_id = get_current_batch_id()
        quest_batch = self._cache_quest_batch
        
        if (quest_batch is None) or (quest_batch.id != batch_id):
            adventurer_rank_info = get_guild_adventurer_rank_info(self.credibility)
            quest_batch = create_quest_batch(
                self.guild_id, batch_id, adventurer_rank_info.level, adventurer_rank_info.quest_limit
            )
            self._cache_quest_batch = quest_batch
        
        return quest_batch
