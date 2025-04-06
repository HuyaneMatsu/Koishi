__all__ = ('ItemEntry',)

from scarletio import RichAttributeErrorBaseType

from ..item_core import get_item


class ItemEntry(RichAttributeErrorBaseType):
    """
    Represents an item's entry in the database.
    
    Attributes
    ----------
    amount : `int`
        The amount of items.
    
    entry_id : `int`
        The entry's identifier in the database.
    
    item : ``Item``
        The represented item.
    """
    __slots__ = ('amount', 'entry_id', 'item')
    
    def __new__(cls, item, amount):
        """
        Creates new item entry.
        
        Parameters
        ----------
        item : ``Item``
            The item.
        
        amount : `int`
            The amount of this item the user has.
        """
        self = object.__new__(cls)
        self.amount = amount
        self.entry_id = -1
        self.item = item
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        repr_parts.append(' item = ')
        repr_parts.append(repr(self.item))
        
        repr_parts.append(', amount = ')
        repr_parts.append(repr(self.amount))
        
        entry_id = self.entry_id
        if entry_id > 0:
            repr_parts.append(' entry_id = ')
            repr_parts.append(repr(entry_id))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @classmethod
    def from_entry(cls, entry):
        """
        Creates an item from the given database entry.
        
        Parameters
        ----------
        entry : `sqlalchemy.engine.result.RowProxy`
            The entry to create the instance based on.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.amount = entry['amount']
        self.entry_id = entry['id']
        self.item = get_item(entry['item_id'])
        return self
    
    
    def copy(self):
        """
        Returns a copy of the item entry.
        
        Returns
        -------
        copy : `instance<cls>`
        """
        copy = object.__new__(type(self))
        copy.amount = self.amount
        copy.entry_id = self.entry_id
        copy.item = self.item
        return copy
    
    
    def __eq__(self, other):
        """Returns self == other."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.amount != other.amount:
            return False
        
        if self.item is not other.item:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns hash(self)."""
        return (self.item.id << 32) | self.amount
