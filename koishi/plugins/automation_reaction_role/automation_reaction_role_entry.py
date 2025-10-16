__all__ = ('AutomationReactionRoleEntry',)

from hata import Message
from scarletio import RichAttributeErrorBaseType

from .items import unpack_items


class AutomationReactionRoleEntry(RichAttributeErrorBaseType):
    """
    Represents an auto react role entry.
    
    Attributes
    ----------
    entry_id : `int`
        The entry's identifier in the database.
    
    flags : `int`
        Additional information stored as bit flags.
    
    items : ``None | list<AutomationReactionRoleItem>``
        Items of the auto react role.
    
    message : ``Message``
        The message the auto react role lives on.
    
    message_cached : `bool`
        Whether the message is properly cached.
    """
    __slots__ = ('entry_id', 'flags', 'items', 'message', 'message_cached')
    
    def __new__(cls, message):
        """
        Creates a new auto react role instance.
        
        Parameters
        -----------
        message : ``Message``
            The message the auto react role lives on.
        """
        self = object.__new__(cls)
        self.entry_id = 0
        self.flags = 0
        self.items = None
        self.message = message
        self.message_cached = True
        return self
    
    
    @classmethod
    def from_entry(cls, entry):
        """
        Creates an auto react role from the given entry.
        
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
        self.flags = entry['flags']
        self.items = unpack_items(entry['data'], entry['data_version'])
        self.message = Message.precreate(
            entry['message_id'],
            channel_id = entry['channel_id'],
            guild_id = entry['guild_id'],
        )
        self.message_cached = False
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        repr_parts.append(' message = ')
        repr_parts.append(repr(self.message))
        
        repr_parts.append(', items = ')
        repr_parts.append(repr(self.items))
        
        flags = self.flags
        if flags:
            repr_parts.append('flags = ')
            repr_parts.append(repr(flags))
        
        entry_id = self.entry_id
        if entry_id:
            repr_parts.append(', entry_id = ')
            repr_parts.append(repr(entry_id))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns self == other."""
        if type(self) is not type(other):
            return False
        
        # entry_id
        if self.entry_id != other.entry_id:
            return False
        
        # flags
        if self.flags != other.flags:
            return False
        
        # items
        if self.items != other.items:
            return False
        
        # message:
        if self.message != other.message:
            return False
        
        # message_cached | internal
        
        return True
    
    
    def copy(self):
        """
        Copies the auto react role entry.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        
        # entry_id
        new.entry_id = self.entry_id
        
        # flags
        new.flags = self.flags
        
        # items
        items = self.items
        if (items is not None):
            items = [item.copy() for item in items]
        new.items = items
        
        # message
        new.message = self.message
        
        # message_cached
        new.message_cached = self.message_cached
        
        return new
