__all__ = ()

from datetime import timezone as TimeZone

from hata import DATETIME_FORMAT_CODE
from scarletio import RichAttributeErrorBaseType


class ToDo(RichAttributeErrorBaseType):
    """
    Represents a cached to do.
    
    Attributes
    ----------
    created_at : `DateTime`
        When the entry was created.
    
    creator_id : `int`
        Wo created the entry.
    
    description : `str`
        The entry's description.
    
    entry_id : `int`
        The identifier of the entry in the database.
    
    name : `str`
        The entry's name.
    """
    __slots__ = ('created_at', 'creator_id', 'description', 'entry_id', 'name')
    
    def __new__(cls, name, description, created_at, creator_id):
        """
        Creates a new to-do to given fields.
        
        Attributes
        ----------
        name : `str`
            The entry's name.
        
        description : `str`
            The entry's description.
        
        created_at : `DateTime`
            When the entry was created.
        
        creator_id : `int`
            Wo created the entry.
        """
        self = object.__new__(cls)
        
        self.created_at = created_at
        self.creator_id = creator_id
        self.description = description
        self.entry_id = 0
        self.name = name
        
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # entry_id
        entry_id = self.entry_id
        if entry_id:
            repr_parts.append(' entry_id = ')
            repr_parts.append(repr(entry_id))
            repr_parts.append(',')
        
        # name
        repr_parts.append(' name = ')
        repr_parts.append(repr(self.name))
        
        # description
        repr_parts.append(', description = ')
        repr_parts.append(repr(self.description))
        
        # created_at
        repr_parts.append(', created_at = ')
        repr_parts.append(format(self.created_at, DATETIME_FORMAT_CODE))
        
        # creator_id
        repr_parts.append(', creator_id = ')
        repr_parts.append(repr(self.creator_id))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @classmethod
    def from_entry(cls, entry):
        """
        Creates an to do instance from the given entry.
        
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
        self.created_at = entry['created_at'].replace(tzinfo = TimeZone.utc)
        self.creator_id = entry['creator_id']
        self.description = entry['description']
        self.name = entry['name']
        return self
