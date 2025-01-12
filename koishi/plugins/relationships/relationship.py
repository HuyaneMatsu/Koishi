__all__ = ('Relationship',)

from datetime import timezone as TimeZone

from scarletio import copy_docs
from hata import DATETIME_FORMAT_CODE

from ...bot_utils.entry_proxy import EntryProxy
from ...bot_utils.models import DB_ENGINE

from .constants import RELATIONSHIP_CACHE, RELATIONSHIP_CACHE_LISTING
from .relationship_saver import RelationshipSaver
from .relationship_types import get_relationship_type_name


class Relationship(EntryProxy):
    """
    Represents the relationship between two users.
    
    Attributes
    ----------
    entry_id : `int`
        The entry's identifier in the database.
    
    relationship_type : `int`
        The requested relationship type.
    
    saver : `None | RelationshipSaver`
        Saver responsible to save synchronization.
    
    source_can_boost_at : `Datetime`
        When the source user can boost next.
    
    source_investment : `int`
        The investment of the source user.
    
    source_user_id : `int`
        Source user identifier.
    
    target_can_boost_at : `Datetime`
        When the target user can boost next.
    
    target_investment : `int`
        The investment the target user.
    
    target_user_id : `int`
        Target user identifier.
    """
    __slots__ = (
        '__weakref__', 'relationship_type', 'source_can_boost_at', 'source_investment', 'source_user_id',
        'target_can_boost_at', 'target_investment', 'target_user_id'
    )
    
    saver_type = RelationshipSaver
    
    
    def __new__(cls, source_user_id, target_user_id, relationship_type, investment, now):
        """
        Creates a new relationship request.
        
        Parameters
        ----------
        source_user_id : `int`
            The source user's identifier.
        
        target_user_id : `int`
            Target user identifier.
        
        relationship_type : `int`
            The requested relationship type.
        
        investment : `int`
            The investment of the source user.
        
        now : `DateTime`
            The investment the target user.
        """
        self = object.__new__(cls)
        self.entry_id = -1
        self.relationship_type = relationship_type
        self.saver = None
        self.source_can_boost_at = now
        self.source_investment = investment
        self.source_user_id = source_user_id
        self.target_can_boost_at = now
        self.target_investment = 0
        self.target_user_id = target_user_id
        
        return self
    
    
    @copy_docs(EntryProxy._put_repr_parts)
    def _put_repr_parts(self, repr_parts, field_added):
        if field_added:
            repr_parts.append(',')
        
        # source_user_id
        repr_parts.append(' source_user_id = ')
        repr_parts.append(repr(self.source_user_id))
        
        # target_user_id
        repr_parts.append(', target_user_id = ')
        repr_parts.append(repr(self.target_user_id))
        
        # relationship_type
        relationship_type = self.relationship_type
        repr_parts.append(', relationship_type = ')
        repr_parts.append(get_relationship_type_name(relationship_type))
        repr_parts.append(' ~ ')
        repr_parts.append(repr(relationship_type))
        
        # source_investment
        repr_parts.append(', source_investment = ')
        repr_parts.append(repr(self.source_investment))
        
        # target_investment
        repr_parts.append(', target_investment = ')
        repr_parts.append(repr(self.target_investment))
        
        # source_can_boost_at
        repr_parts.append(', source_can_boost_at = ')
        repr_parts.append(format(self.source_can_boost_at, DATETIME_FORMAT_CODE))
        
        # target_can_boost_at
        repr_parts.append(', target_can_boost_at = ')
        repr_parts.append(format(self.target_can_boost_at, DATETIME_FORMAT_CODE))
        
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
        RELATIONSHIP_CACHE[self.entry_id] = self
        
        for listing_key in (self.source_user_id, self.target_user_id):
            try:
                listing = RELATIONSHIP_CACHE_LISTING[listing_key]
            except KeyError:
                if (DB_ENGINE is not None):
                    continue
                
                listing = None
            
            if (listing is None):
                RELATIONSHIP_CACHE_LISTING[listing_key] = [self]
                continue
            
            if (self not in listing):
                listing.append(self)
            
            continue
    
    
    @copy_docs(EntryProxy._pop_from_cache)
    def _pop_from_cache(self):
        try:
            del RELATIONSHIP_CACHE[self.entry_id]
        except KeyError:
            pass
        
        for listing_key in (self.source_user_id, self.target_user_id):
            try:
                listing = RELATIONSHIP_CACHE_LISTING[listing_key]
            except KeyError:
                continue
            
            if (listing is None):
                continue
            
            try:
                listing.remove(self)
            except ValueError:
                continue
            
            if listing:
                continue
            
            RELATIONSHIP_CACHE_LISTING[listing_key] = None
            continue
    
    
    @classmethod
    @copy_docs(EntryProxy.from_entry)
    def from_entry(cls, entry):
        entry_id = entry['id']
        
        try:
            self = RELATIONSHIP_CACHE[entry_id]
        except KeyError:
            self = object.__new__(cls)
            self.entry_id = entry_id
            self.saver = None
            RELATIONSHIP_CACHE[entry_id] = self
        
        self.relationship_type = entry['relationship_type']
        
        self.source_can_boost_at = entry['source_can_boost_at'].replace(tzinfo = TimeZone.utc)
        self.source_investment = entry['source_investment']
        self.source_user_id = entry['source_user_id']
        
        self.target_can_boost_at = entry['target_can_boost_at'].replace(tzinfo = TimeZone.utc)
        self.target_investment = entry['target_investment']
        self.target_user_id = entry['target_user_id']
        
        return self
