__all__ = ('UserStats',)

from datetime import timezone as TimeZone

from scarletio import copy_docs

from ...bot_utils.entry_proxy import EntryProxy

from .constants import STATS_CACHE
from .helpers import generate_user_stats_defaults
from .user_stats_calculated import UserStatsCalculated
from .user_stats_saver import UserStatsSaver


class UserStats(EntryProxy):
    """
    A user's stats.
    
    Attributes
    ----------
    _cache_stats_calculated : `None | UserStatsCalculated`
        Cache field for the calculated stats after applying the modifiers.
    
    entry_id : `int`
        The entry's identifier in the database.
    
    credibility : `int`
        The accumulated credibility of the user.
    
    item_id_costume : `int`
        The user's costume item's identifier.
    
    item_id_head : `int`
        The user's head item's identifier.
    
    item_id_species : `int`
        Target user's species' identifier.
    
    item_id_weapon : `int`
        The user's weapon item's identifier.
    
    recovering_until : `None | DateTime`
        Until when the user is in recovery.
    
    saver : `None | UserStatsSaver`
        Saver responsible for save synchronization.
    
    stat_bedroom : `int`
        The user's bedroom skills.
    
    stat_charm : `int`
        The user's charm.
    
    stat_cuteness : `int`
        The user's cuteness.
    
    stat_housewife : `int`
        The user's housewife skills.
    
    stat_loyalty : `int`
        The user's loyalty.
    
    user_id : `int`
        The represented user's identifier.
    """
    __slots__ = (
        '__weakref__', '_cache_stats_calculated', 'credibility', 'item_id_costume', 'item_id_head', 'item_id_species',
        'item_id_weapon', 'recovering_until', 'saver', 'stat_bedroom', 'stat_charm', 'stat_cuteness', 'stat_housewife',
        'stat_loyalty', 'user_id',
    )
    
    saver_type = UserStatsSaver
    
    
    def __new__(cls, user_id):
        """
        Creates new stats.
        
        Parameters
        ----------
        user_id : `int`
            The user's identifier.
        """
        self = object.__new__(cls)
        self._cache_stats_calculated = None
        self.saver = None
        
        self.entry_id = 0
        self.user_id = user_id
        
        self.credibility = 0
        self.recovering_until = None
        
        self.item_id_costume = 0
        self.item_id_head = 0
        self.item_id_species = 0
        self.item_id_weapon = 0
        
        (
            self.stat_housewife,
            self.stat_cuteness,
            self.stat_bedroom,
            self.stat_charm,
            self.stat_loyalty,
        ) = generate_user_stats_defaults(user_id)
        
        return self
    
    
    @copy_docs(EntryProxy._put_repr_parts)
    def _put_repr_parts(self, repr_parts, field_added):
        if field_added:
            repr_parts.append(',')
        
        # source_user_id
        repr_parts.append(' user_id = ')
        repr_parts.append(repr(self.user_id))
        
        return repr_parts
    
    
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
        STATS_CACHE[self.user_id] = self
    
    
    @copy_docs(EntryProxy._pop_from_cache)
    def _pop_from_cache(self):
        try:
            del STATS_CACHE[self.user_id]
        except KeyError:
            pass
    
    
    @classmethod
    @copy_docs(EntryProxy.from_entry)
    def from_entry(cls, entry):
        user_id = entry['user_id']
        
        try:
            self = STATS_CACHE[user_id]
        except KeyError:
            self = object.__new__(cls)
            self.entry_id = entry['id']
            self.user_id = user_id
            self._cache_stats_calculated = None
            self.saver = None
            STATS_CACHE[user_id] = self
        
        self.stat_housewife = entry['stat_housewife']
        self.stat_cuteness = entry['stat_cuteness']
        self.stat_bedroom = entry['stat_bedroom']
        self.stat_charm = entry['stat_charm']
        self.stat_loyalty = entry['stat_loyalty']
        
        self.credibility = entry['credibility']
        
        recovering_until = entry['recovering_until']
        if (recovering_until is not None):
            recovering_until = recovering_until.replace(tzinfo = TimeZone.utc)
        self.recovering_until = recovering_until
        
        self.item_id_costume = entry['item_id_costume']
        self.item_id_head = entry['item_id_head']
        self.item_id_species = entry['item_id_species']
        self.item_id_weapon = entry['item_id_weapon']
        
        return self
    
    
    @copy_docs(EntryProxy.set)
    def set(self, field_name, field_value):
        EntryProxy.set(self, field_name, field_value)
        self._cache_stats_calculated = None
    
    
    @property
    def stats_calculated(self):
        """
        Returns the calculated stats.
        
        Returns
        -------
        stats_calculated : ``UserStatsCalculated``
        """
        stats_calculated = self._cache_stats_calculated
        if stats_calculated is None:
            stats_calculated = UserStatsCalculated(self)
            self._cache_stats_calculated = stats_calculated
        
        return stats_calculated
