__all__ = ('RelationshipRequest',)

from scarletio import copy_docs

from ...bot_utils.entry_proxy import EntryProxy
from ...bot_utils.models import DB_ENGINE

from .constants import RELATIONSHIP_REQUEST_CACHE, RELATIONSHIP_REQUEST_CACHE_LISTING
from .relationship_request_saver import RelationshipRequestSaver
from .relationship_types import get_relationship_type_name


class RelationshipRequest(EntryProxy):
    """
    Relationship request.
    
    Attributes
    ----------
    entry_id : `int`
        The entry's identifier in the database.
    
    investment : `int`
        The investment the request should go through with.
    
    relationship_type : `int`
        The requested relationship type.
    
    saver : `None | RelationshipRequestSaver`
        Saver responsible to save synchronization.
    
    source_user_id : `int`
        Source user identifier.
    
    target_user_id : `int`
        Target user identifier.
    """
    __slots__ = ('__weakref__', 'investment', 'relationship_type', 'source_user_id', 'target_user_id')
    
    saver_type = RelationshipRequestSaver
    
    
    def __new__(cls, source_user_id, target_user_id, relationship_type, investment):
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
            The investment the request should go through with.
        """
        self = object.__new__(cls)
        self.investment = investment
        self.entry_id = -1
        self.relationship_type = relationship_type
        self.saver = None
        self.source_user_id = source_user_id
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
        
        # investment
        repr_parts.append(', investment = ')
        repr_parts.append(repr(self.investment))
        
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
        RELATIONSHIP_REQUEST_CACHE[self.entry_id] = self
        
        for listing_key in ((self.source_user_id, True), (self.target_user_id, False)):
            try:
                listing = RELATIONSHIP_REQUEST_CACHE_LISTING[listing_key]
            except KeyError:
                if (DB_ENGINE is not None):
                    continue
                
                listing = None
            
            if (listing is None):
                RELATIONSHIP_REQUEST_CACHE_LISTING[listing_key] = [self]
                continue
            
            if (self not in listing):
                listing.append(self)
            
            continue
    
    @copy_docs(EntryProxy._pop_from_cache)
    def _pop_from_cache(self):
        try:
            del RELATIONSHIP_REQUEST_CACHE[self.entry_id]
        except KeyError:
            pass
        
        for listing_key in ((self.source_user_id, True), (self.target_user_id, False)):
            try:
                listing = RELATIONSHIP_REQUEST_CACHE_LISTING[listing_key]
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
            
            RELATIONSHIP_REQUEST_CACHE_LISTING[listing_key] = None
            continue
    
    
    @classmethod
    @copy_docs(EntryProxy.from_entry)
    def from_entry(cls, entry):
        entry_id = entry['id']
        
        try:
            self = RELATIONSHIP_REQUEST_CACHE[entry_id]
        except KeyError:
            self = object.__new__(cls)
            self.entry_id = entry_id
            self.saver = None
            RELATIONSHIP_REQUEST_CACHE[entry_id] = self
        
        self.investment = entry['investment']
        self.relationship_type = entry['relationship_type']
        self.source_user_id = entry['source_user_id']
        self.target_user_id = entry['target_user_id']
        
        return self
