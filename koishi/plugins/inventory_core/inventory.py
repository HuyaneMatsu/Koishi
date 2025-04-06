__all__ = ('Inventory',)

from scarletio import RichAttributeErrorBaseType

from .item_entry import ItemEntry


class Inventory(RichAttributeErrorBaseType):
    """
    Represents a user's inventory.
    
    Attributes
    ----------
    item_entries : `None | dict<int, ItemEntry>`
        The items of the user.
    
    item_entries_modified : `None | dict<int, ItemEntry>`
        The modified items of the user.
    
    user_id : `int`
        The user's identifier.
    
    weight : `int`
        The cumulative weight of the inventory.
    
    Notes
    -----
    Inventory instances are weakreferable.
    """
    __slots__ = ('__weakref__', 'item_entries', 'item_entries_modified', 'user_id', 'weight')
    
    def __new__(cls, user_id):
        """
        Creates a new empty inventory.
        
        Parameters
        ----------
        user_id : `int`
            The user's identifier.
        """
        self = object.__new__(cls)
        self.item_entries = None
        self.item_entries_modified = None
        self.user_id = user_id
        self.weight = 0
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # user_id
        repr_parts.append(' user_id = ')
        repr_parts.append(repr(self.user_id))
        
        # weight
        repr_parts.append(' weight = ')
        repr_parts.append(repr(self.weight))
        
        # item_entries
        item_entries = self.item_entries
        if (item_entries is not None):
            repr_parts.append(', item_entries = [')
            
            field_added = False
            
            for item_entry in item_entries.values():
                if field_added:
                    repr_parts.append(', ')
                else:
                    field_added = True
                
                repr_parts.append(repr(item_entry))
            
            repr_parts.append(']')
        
        # item_entries_modified
        item_entries_modified = self.item_entries_modified
        if (item_entries_modified is not None):
            repr_parts.append(', item_entries_modified = [')
            
            field_added = False
            
            for item_entry in item_entries_modified.values():
                if field_added:
                    repr_parts.append(', ')
                else:
                    field_added = True
                
                repr_parts.append(repr(item_entry))
            
            repr_parts.append(']')
        
        
        repr_parts.append('>')
        return ''.join(repr_parts)    
    
    
    def get_item_amount(self, item):
        """
        Returns how much amount of the given item the inventory has in.
        
        Parameters
        ----------
        item : ``Item``
            The item to modify its amount of.
        
        Returns
        -------
        amount : `int`
        """
        item_entry = self.get_item_entry_by_id(item.id)
        if item_entry is None:
            return 0
        
        return item_entry.amount
    
    
    def modify_item_amount(self, item, amount):
        """
        Modifies the amount of the given item.
        
        Parameters
        ----------
        item : ``Item``
            The item to modify its amount of.
        
        amount : `int`
            The amount to modify the current amount with.
        
        Returns
        -------
        new_amount : `int`
        """
        item_entries = self.item_entries
        item_entries_modified = self.item_entries_modified
        
        while True:
            if (item_entries is not None):
                try:
                    item_entry = item_entries.pop(item.id)
                except KeyError:
                    pass
                else:
                    if not item_entries:
                        self.item_entries = None
                    break
            
            if (item_entries_modified is not None):
                try:
                    item_entry = item_entries_modified.pop(item.id)
                except KeyError:
                    pass
                else:
                    if not item_entries_modified:
                        self.item_entries_modified = None
                    break
            
            item_entry = None
            break
        
        if (item_entry is None):
            if amount <= 0:
                return 0
            
            weight_change = item.weight * amount
            item_entry = ItemEntry(item, amount)
            new_amount = amount
        
        else:
            old_amount = item_entry.amount
            
            if amount == 0:
                return old_amount
            
            if amount < 0:
                amount = max(amount, -old_amount)
            
            new_amount = old_amount + amount
            weight_change = item.weight * amount
            
            item_entry.amount = new_amount
        
        # Ignore freshly removed & added back items.
        if (item_entry.entry_id != - 1) or new_amount:
            if item_entries_modified is None:
                item_entries_modified = {}
            
            # It may happened that we assigned this as `None`, so reassign it. Hell yeah.
            self.item_entries_modified = item_entries_modified
            item_entries_modified[item.id] = item_entry
        
        self.weight += weight_change
        
        return new_amount
    
    
    def get_modified_item_entry(self):
        """
        Gets a modified item entry.
        
        Returns
        -------
        modified_item_entry : `None | ItemEntry`
        """
        item_entries_modified = self.item_entries_modified
        if (item_entries_modified is not None):
            return next(iter(item_entries_modified.values())).copy()
    
    
    def apply_modified_item_entry(self, item_entry):
        """
        Applies a modified item entry.
        
        Parameters
        ----------
        item_entry : ``ItemEntry``
            The modified item entry.
        """
        item_entries_modified = self.item_entries_modified
        
        if (item_entries_modified is not None):
            try:
                current_item_entry = item_entries_modified[item_entry.item.id]
            except KeyError:
                pass
            else:
                # Double modified?
                if item_entry.amount != current_item_entry.amount:
                    current_item_entry.entry_id = item_entry.entry_id
                    return
                
                del item_entries_modified[item_entry.item.id]
                if not item_entries_modified:
                    item_entries_modified = None
                    self.item_entries_modified = None
        
        # Do not add to owned items if the amount is 0.
        if item_entry.amount == 0:
            return
        
        item_entries = self.item_entries
        if (item_entries is None):
            item_entries = {}
            self.item_entries = item_entries
        
        item_entries[item_entry.item.id] = item_entry
    
    
    def iter_item_entries(self):
        """
        Iterates over the item entries of the inventory.
        
        This method is an iterable generator.
        
        Yields
        ------
        item_entry : ``ItemEntry``
        """
        item_entries = self.item_entries
        if (item_entries is not None):
            yield from item_entries.values()
        
        item_entries_modified = self.item_entries_modified
        if (item_entries_modified is not None):
            for item_entry in item_entries_modified.values():
                if item_entry.amount:
                    yield item_entry
    
    
    def get_item_entry_by_id(self, item_id):
        """
        Gets the item for the given identifier if it is in the inventory.
        
        Parameters
        ----------
        item_id : `int`
            The item's identifier.
        
        Returns
        -------
        item : `None | ItemEntry`
        """
        item_entries = self.item_entries
        if (item_entries is not None):
            try:
                return item_entries[item_id]
            except KeyError:
                pass
        
        item_entries_modified = self.item_entries_modified
        if (item_entries_modified is not None):
            try:
                return item_entries_modified[item_id]
            except KeyError:
                pass
    
    
    @classmethod
    def from_entries(cls, user_id, entries):
        """
        Creates an from the given database item entries.
        
        Parameters
        ----------
        user_id : `int`
            The user's identifier.
        
        entries : `list<sqlalchemy.engine.result.RowProxy>`
            The entries to create the inventory from.
        
        Returns
        -------
        self : `instance<cls>`
        """
        if entries:
            item_entries = {entry['item_id']: ItemEntry.from_entry(entry) for entry in entries}
            weight = sum(item_entry.item.weight * item_entry.amount for item_entry in item_entries.values())
        else:
            item_entries = None
            weight = 0
        
        self = object.__new__(cls)
        self.item_entries = item_entries
        self.item_entries_modified = None
        self.user_id = user_id
        self.weight = weight
        return self
