__all__ = ('UserStats',)

from datetime import timezone as TimeZone

from scarletio import RichAttributeErrorBaseType

from .helpers import generate_user_stats_defaults
from .user_stats_calculated import UserStatsCalculated


class UserStats(RichAttributeErrorBaseType):
    """
    A user's stats.
    
    Attributes
    ----------
    _cache_user_stats_calculated : `None | UserStatsCalculated`
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
    
    modified_fields : `None | dict<str, object>`
        The name of the already modified fields.
    
    recovering_until : `None | DateTime`
        Until when the user is in recovery.
    
    recovering_until_notification_at : `None | DateTime`
        When the recovery notification should be delivered at. Set upon delivering the original notification fails.
    
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
        '__weakref__', '_cache_user_stats_calculated', 'credibility', 'entry_id', 'item_id_costume', 'item_id_head',
        'item_id_species', 'item_id_weapon', 'modified_fields', 'recovering_until',
        'recovering_until_notification_at', 'stat_bedroom', 'stat_charm', 'stat_cuteness', 'stat_housewife',
        'stat_loyalty', 'user_id',
    )
    
    def __new__(cls, user_id):
        """
        Creates new stats.
        
        Parameters
        ----------
        user_id : `int`
            The user's identifier.
        """
        self = object.__new__(cls)
        self._cache_user_stats_calculated = None
        self.modified_fields = None
        
        self.entry_id = 0
        self.user_id = user_id
        
        self.credibility = 0
        self.recovering_until = None
        self.recovering_until_notification_at = None
        
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
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # entry_id
        entry_id = self.entry_id
        if entry_id != 0:
            repr_parts.append(' entry_id = ')
            repr_parts.append(repr(entry_id))
            repr_parts.append(',')
        
        # user_id
        repr_parts.append(' user_id = ')
        repr_parts.append(repr(self.user_id))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @classmethod
    def from_entry(cls, entry):
        """
        Creates an new instance from the given entry.
        
        Parameters
        ----------
        entry : `sqlalchemy.engine.result.RowProxy`
            The entry to create the instance based on.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.entry_id = entry['id']
        self.user_id = entry['user_id']
        self._cache_user_stats_calculated = None
        self.modified_fields = None
        
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
        
        recovering_until_notification_at = entry['recovering_until_notification_at']
        if (recovering_until_notification_at is not None):
            recovering_until_notification_at = recovering_until_notification_at.replace(
                tzinfo = TimeZone.utc
            )
        self.recovering_until_notification_at = recovering_until_notification_at
        
        self.item_id_costume = entry['item_id_costume']
        self.item_id_head = entry['item_id_head']
        self.item_id_species = entry['item_id_species']
        self.item_id_weapon = entry['item_id_weapon']
        
        return self
    
    
    def _mark_modification(self, key, value):
        """
        Marks a field as modified.
        
        Parameters
        ----------
        key : `str`
            The field's key.
        
        value : `object`
            The field's value.
        """
        self._cache_user_stats_calculated = None
        modified_fields = self.modified_fields
        if (modified_fields is None):
            self.modified_fields = modified_fields = {}
        
        modified_fields[key] = value
    
    
    @property
    def stats_calculated(self):
        """
        Returns the calculated stats.
        
        Returns
        -------
        stats_calculated : ``UserStatsCalculated``
        """
        stats_calculated = self._cache_user_stats_calculated
        if stats_calculated is None:
            stats_calculated = UserStatsCalculated(self)
            self._cache_user_stats_calculated = stats_calculated
        
        return stats_calculated
    
    
    def modify_stat_housewife_by(self, value):
        """
        Modifies the housewife of the user stats.
        
        Parameters
        ----------
        value : `int`
            value to modify by.
        """
        self.stat_housewife = stat_housewife = max(self.stat_housewife + value, 0)
        self._mark_modification('stat_housewife', stat_housewife)
    
    
    def modify_stat_cuteness_by(self, value):
        """
        Modifies the cuteness of the user stats.
        
        Parameters
        ----------
        value : `int`
            value to modify by.
        """
        self.stat_cuteness = stat_cuteness = max(self.stat_cuteness + value, 0)
        self._mark_modification('stat_cuteness', stat_cuteness)
    
    
    def modify_stat_bedroom_by(self, value):
        """
        Modifies the bedroom of the user stats.
        
        Parameters
        ----------
        value : `int`
            value to modify by.
        """
        self.stat_bedroom = stat_bedroom = max(self.stat_bedroom + value, 0)
        self._mark_modification('stat_bedroom', stat_bedroom)
    
    
    def modify_stat_charm_by(self, value):
        """
        Modifies the charm of the user stats.
        
        Parameters
        ----------
        value : `int`
            value to modify by.
        """
        self.stat_charm = stat_charm = max(self.stat_charm + value, 0)
        self._mark_modification('stat_charm', stat_charm)
    
    
    def modify_stat_loyalty_by(self, value):
        """
        Modifies the loyalty of the user stats.
        
        Parameters
        ----------
        value : `int`
            value to modify by.
        """
        self.stat_loyalty = stat_loyalty = max(self.stat_loyalty + value, 0)
        self._mark_modification('stat_loyalty', stat_loyalty)
    
    
    def set_recovering_until(self, date_time):
        """
        Sets till when the user is recovering.
        
        Parameters
        ----------
        date_time : `DateTime`
            Amount to set to.
        """
        self.recovering_until = date_time
        self._mark_modification('recovering_until', date_time)
    
    
    def set_recovering_until_notification_at(self, date_time):
        """
        Sets when the recovery notification should be delivered at.
        
        Parameters
        ----------
        """
        self.recovering_until_notification_at = date_time
        self._mark_modification('recovering_until_notification_at', date_time)
    
    
    def modify_credibility_by(self, value):
        """
        Modifies the credibility of the user stats.
        
        Parameters
        ----------
        value : `int`
            value to modify by.
        """
        self.credibility = credibility = max(self.credibility + value, 0)
        self._mark_modification('credibility', credibility)
    
    
    def set_item_id_costume(self, item_id):
        """
        Sets the costume item.
        
        Parameters
        ----------
        item_id : `int`
            Item identifier to set to.
        """
        self.item_id_costume = item_id
        self._mark_modification('item_id_costume', item_id)
    
    
    def set_item_id_head(self, item_id):
        """
        Sets the head item.
        
        Parameters
        ----------
        item_id : `int`
            Item identifier to set to.
        """
        self.item_id_head = item_id
        self._mark_modification('item_id_head', item_id)
    
    
    def set_item_id_species(self, item_id):
        """
        Sets the species item.
        
        Parameters
        ----------
        item_id : `int`
            Item identifier to set to.
        """
        self.item_id_species = item_id
        self._mark_modification('item_id_species', item_id)
    
    
    def set_item_id_weapon(self, item_id):
        """
        Sets the weapon item.
        
        Parameters
        ----------
        item_id : `int`
            Item identifier to set to.
        """
        self.item_id_weapon = item_id
        self._mark_modification('item_id_weapon', item_id)
