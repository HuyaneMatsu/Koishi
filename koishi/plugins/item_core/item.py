__all__ = ('Item',)

from scarletio import RichAttributeErrorBaseType


class Item(RichAttributeErrorBaseType):
    """
    Represents an item.
    
    Attributes
    ----------
    description : `str`
        Description of the item.
    
    emoji : ``None | Emoji``
        Emoji representing the item.
    
    flags : `int`
        Item flags.
    
    id : `int`
        The item's identifier.
    
    name : `str`
        The name of the item.
    
    modifiers : `tuple<StatModifier>`
        Modifiers of the item.
    
    value : `int`
        The default value of the item.
    
    weight : `int`
        The weight of the item in grams.
    """
    __slots__ = ('description', 'modifiers', 'emoji', 'flags', 'id', 'name', 'value', 'weight')
    
    def __new__(cls, item_id, name, emoji, description, flags, value, weight, modifiers):
        """
        Creates a new item.
        
        Parameters
        ----------
        item_id : `int`
            The item's identifier.
        
        name : `str`
            The name of the item.
        
        emoji : ``None | Emoji``
            Emoji representing the item.
        
        description : `str`
            Description of the item.
        
        flags : `int`
            Item flags.
        
        value : `int`
            The default value of the item.
        
        weight : `int`
            The weight of the item in grams.
        
        modifiers : `None`
            Effects of the item.
        """
        self = object.__new__(cls)
        self.description = description
        self.emoji = emoji
        self.flags = flags
        self.id = item_id
        self.name = name
        self.modifiers = modifiers
        self.value = value
        self.weight = weight
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # name
        repr_parts.append(' name = ')
        repr_parts.append(repr(self.name))
        
        # id
        repr_parts.append(', id = ')
        repr_parts.append(repr(self.id))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def iter_modifiers(self):
        """
        Iterates over the modifies of the item.
        
        This function is an iterable generator.
        
        Yields
        ------
        modifier : ``Modifier``
        """
        modifiers = self.modifiers
        if (modifiers is not None):
            yield from modifiers
