__all__ = ('AutomationReactionRoleItem',)

from scarletio import RichAttributeErrorBaseType


class AutomationReactionRoleItem(RichAttributeErrorBaseType):
    """
    Represents an item of an auto react role.
    
    Attributes
    ----------
    emoji_id : `int`
        The assigned emoji's identifier.
    
    add_role_ids : `None | tuple<int>`
        Role identifiers to add on reaction.
    
    remove_role_ids : `None | tuple<int>`
        Role identifiers to remove on reaction.
    """
    __slots__ = ('emoji_id', 'add_role_ids', 'remove_role_ids')
    
    def __new__(cls, emoji_id, add_role_ids, remove_role_ids):
        """
        Creates an auto react role item.
        
        Parameters
        ----------
        emoji_id : `int`
            The assigned emoji's identifier.
        
        add_role_ids : `None | tuple<int>`
            Role identifiers to add on reaction.
        
        remove_role_ids : `None | tuple<int>`
            Role identifiers to remove on reaction.
        """
        self = object.__new__(cls)
        self.emoji_id = emoji_id
        self.add_role_ids = add_role_ids
        self.remove_role_ids = remove_role_ids
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # emoji_id
        repr_parts.append(' emoji_id = ')
        repr_parts.append(repr(self.emoji_id))
        
        # add_role_ids
        add_role_ids = self.add_role_ids
        if (add_role_ids is not None):
            repr_parts.append(', add_role_ids = ')
            repr_parts.append(repr(add_role_ids))
        
        # remove_role_ids
        remove_role_ids = self.remove_role_ids
        if (remove_role_ids is not None):
            repr_parts.append(', remove_role_ids = ')
            repr_parts.append(repr(remove_role_ids))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns self == other."""
        if type(self) is not type(other):
            return NotImplemented
        
        # emoji_id
        if self.emoji_id != other.emoji_id:
            return False
        
        # add_role_ids
        if self.add_role_ids != other.add_role_ids:
            return False
        
        # remove_role_ids
        if self.remove_role_ids != other.remove_role_ids:
            return False
        
        return True
    
    
    def copy(self):
        """
        Copies the auto react role item.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        
        # emoji:id
        new.emoji_id = self.emoji_id
        
        # add_role_ids
        add_role_ids = self.add_role_ids
        if (add_role_ids is not None):
            add_role_ids = (*add_role_ids,)
        new.add_role_ids = add_role_ids
        
        # remove_role_ids
        remove_role_ids = self.remove_role_ids
        if (remove_role_ids is not None):
            remove_role_ids = (*remove_role_ids,)
        new.remove_role_ids = remove_role_ids
        
        return new
