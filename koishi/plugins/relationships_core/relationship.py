__all__ = ('Relationship',)

from datetime import timezone as TimeZone

from scarletio import RichAttributeErrorBaseType
from hata import DATETIME_FORMAT_CODE

from .relationship_types import get_relationship_type_name_basic


class Relationship(RichAttributeErrorBaseType):
    """
    Represents the relationship between two users.
    
    Attributes
    ----------
    entry_id : `int`
        The entry's identifier in the database.
    
    modified_fields : `None | dict<str, object>`
        the modified fields of the relationship.
    
    relationship_type : `int`
        The requested relationship type.
    
    source_can_boost_at : `DateTime`
        When the source user can boost next.
    
    source_investment : `int`
        The investment of the source user.
    
    source_user_id : `int`
        Source user identifier.
    
    target_can_boost_at : `DateTime`
        When the target user can boost next.
    
    target_investment : `int`
        The investment the target user.
    
    target_user_id : `int`
        Target user identifier.
    """
    __slots__ = (
        '__weakref__', 'entry_id', 'modified_fields', 'relationship_type', 'source_can_boost_at', 'source_investment',
        'source_user_id', 'target_can_boost_at', 'target_investment', 'target_user_id'
    )
    
    
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
        self.entry_id = 0
        self.modified_fields = None
        self.relationship_type = relationship_type
        self.source_can_boost_at = now
        self.source_investment = investment
        self.source_user_id = source_user_id
        self.target_can_boost_at = now
        self.target_investment = 0
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
        repr_parts.append(get_relationship_type_name_basic(relationship_type))
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
        self.modified_fields = None
        self.relationship_type = entry['relationship_type']
        
        self.source_can_boost_at = entry['source_can_boost_at'].replace(tzinfo = TimeZone.utc)
        self.source_investment = entry['source_investment']
        self.source_user_id = entry['source_user_id']
        
        self.target_can_boost_at = entry['target_can_boost_at'].replace(tzinfo = TimeZone.utc)
        self.target_investment = entry['target_investment']
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
    
    
    def set_relationship_type(self, relationship_type):
        """
        Sets the relationship type.
        
        Parameters
        ----------
        relationship_type : `int`
            Relationship type to set.
        """
        self.relationship_type = relationship_type
        self._mark_modification('relationship_type', relationship_type)
    
    
    def set_source_can_boost_at(self, source_can_boost_at):
        """
        Sets when the source can boost.
        
        Parameters
        ----------
        source_can_boost_at : `DateTime`
            When the source can boost at.
        """
        self.source_can_boost_at = source_can_boost_at
        self._mark_modification('source_can_boost_at', source_can_boost_at)
    
    
    def set_source_investment(self, source_investment):
        """
        Sets when the source's investment.
        
        Parameters
        ----------
        source_investment : `int`
            The source's investment.
        """
        self.source_investment = source_investment
        self._mark_modification('source_investment', source_investment)
    
    
    def set_target_can_boost_at(self, target_can_boost_at):
        """
        Sets when the target can boost.
        
        Parameters
        ----------
        target_can_boost_at : `DateTime`
            When the target can boost at.
        """
        self.target_can_boost_at = target_can_boost_at
        self._mark_modification('target_can_boost_at', target_can_boost_at)
    
    
    def set_target_investment(self, target_investment):
        """
        Sets when the target's investment.
        
        Parameters
        ----------
        target_investment : `int`
            The target's investment.
        """
        self.target_investment = target_investment
        self._mark_modification('target_investment', target_investment)
