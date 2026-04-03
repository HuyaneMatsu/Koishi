__all__ = ('ItemGroup',)

from scarletio import RichAttributeErrorBaseType


class ItemGroup(RichAttributeErrorBaseType):
    """
    Represents a group of items.
    
    Attributes
    ----------
    description : `str`
        Description of the item group.
    
    emoji : ``None | Emoji``
        Emoji representing the item group.
    
    id : `int`
        The group's identifier.
    
    item_ids : `None | tuple<int>`
        The item's identifiers covered by this group.
    
    name : `str`
        The group's name.
    """
    __slots__ = ('description', 'emoji', 'id', 'item_ids', 'name')
    
    def __new__(cls, item_group_id, name, emoji, description, item_ids):
        """
        Creates a new item group.
        
        Parameters
        ----------
        item_group_id : `int`
            The group's identifier.
        
        name : `str`
            The group's name.
        
        item_ids : `None | tuple<int>`
            The item's identifiers covered by this group.
        """
        self = object.__new__(cls)
        self.description = description
        self.emoji = emoji
        self.id = item_group_id
        self.item_ids = item_ids
        self.name = name
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # id
        repr_parts.append(' id = ')
        repr_parts.append(repr(self.id))
        
        # name
        repr_parts.append(', name = ')
        repr_parts.append(repr(self.name))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
