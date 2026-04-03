__all__ = ('RelationshipRequest',)

from scarletio import copy_docs

from ...bot_utils.entry_proxy import EntryProxy

from .relationship_types import get_relationship_type_name_basic


class RelationshipRequest(EntryProxy):
    """
    Relationship request.
    
    Attributes
    ----------
    entry_id : `int`
        The entry's identifier in the database.
    
    investment : `int`
        The investment the request should go through with.
    
    modified_fields : `None | dict<str, object>`
        the modified fields of the relationship.
    
    relationship_type : `int`
        The requested relationship type.
    
    source_user_id : `int`
        Source user identifier.
    
    target_user_id : `int`
        Target user identifier.
    """
    __slots__ = (
        '__weakref__', 'entry_id', 'investment', 'modified_fields', 'relationship_type', 'source_user_id',
        'target_user_id'
    )
    
    
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
        self.entry_id = 0
        self.investment = investment
        self.modified_fields = None
        self.relationship_type = relationship_type
        self.source_user_id = source_user_id
        self.target_user_id = target_user_id
        
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        entry_id = self.entry_id
        if entry_id:
            repr_parts.append(' entry_id = ')
            repr_parts.append(repr(entry_id))
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
        repr_parts.extend(get_relationship_type_name_basic(relationship_type))
        repr_parts.append(' ~ ')
        repr_parts.append(repr(relationship_type))
        
        # investment
        repr_parts.append(', investment = ')
        repr_parts.append(repr(self.investment))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @classmethod
    @copy_docs(EntryProxy.from_entry)
    def from_entry(cls, entry):
        self = object.__new__(cls)
        self.entry_id = entry['id']
        self.investment = entry['investment']
        self.modified_fields = None
        self.relationship_type = entry['relationship_type']
        self.source_user_id = entry['source_user_id']
        self.target_user_id = entry['target_user_id']
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
        modified_fields = self.modified_fields
        if (modified_fields is None):
            self.modified_fields = modified_fields = {}
        
        modified_fields[key] = value
    
    
    def set_investment(self, investment):
        """
        Sets the relationship type.
        
        Parameters
        ----------
        investment : `int`
            Investment to set.
        """
        self.investment = investment
        self._mark_modification('investment', investment)
