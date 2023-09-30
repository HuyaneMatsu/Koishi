__all__ = ('NotificationSettings',)

from scarletio import RichAttributeErrorBaseType


class NotificationSettings(RichAttributeErrorBaseType):
    """
    A user's notification settings.
    
    Attributes
    ----------
    entry_id : `int`
        The entry's identifier in the database.
    user_id : `int`
        The user's identifier.
    daily : `bool`
        Whether daily notification should be delivered.
    proposal : `bool`
        Whether proposal notification should be delivered.
    """
    __slots__ = ('entry_id', 'user_id', 'daily', 'proposal')
    
    def __new__(cls, user_id, *, daily = True, proposal = True):
        """
        Creates a new notification settings object.
        
        Parameters
        ----------
        user_id : `int`
            The user's identifier.
        daily : `bool` = `True`, Optional (Keyword only)
            Whether daily notification should be delivered.
        daily : `bool` = `True`, Optional (Keyword only)
            Whether proposal notification should be delivered.
        """
        self = object.__new__(cls)
        self.entry_id = -1
        self.user_id = user_id
        self.daily = daily
        self.proposal = proposal
        return self
    
    
    @classmethod
    def from_entry(cls, entry):
        """
        Creates an automation configuration from the given entry.
        
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
        self.daily = entry['daily']
        self.proposal = entry['proposal']
        return self
    
    
    def __repr__(self):
        """Returns the notification settings' representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        entry_id = self.entry_id
        if (entry_id != -1):
            repr_parts.append(' entry_id = ')
            repr_parts.append(repr(entry_id))
            repr_parts.append(',')
        
        repr_parts.append(' user_id = ')
        repr_parts.append(repr(self.user_id))
        
        repr_parts.append(', daily = ')
        repr_parts.append(repr(self.daily))
        
        repr_parts.append(', proposal = ')
        repr_parts.append(repr(self.proposal))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two notification settings are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.user_id != other.user_id:
            return False
        
        if self.daily != other.daily:
            return False
        
        if self.proposal != other.proposal:
            return False
        
        return True
    
    
    def __bool__(self):
        """Returns whether teh notification setting has anything modified."""
        if self.daily != True:
            return True
        
        if self.proposal != True:
            return True
        
        return False
    
    
    def copy(self):
        """
        Copies the notification settings.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.entry_id = self.entry_id
        new.user_id = self.user_id
        new.daily = self.daily
        new.proposal = self.proposal
        return new
