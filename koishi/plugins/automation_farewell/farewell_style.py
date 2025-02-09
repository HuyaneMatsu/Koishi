__all__ = ('FarewellStyle',)

from scarletio import RichAttributeErrorBaseType


class FarewellStyle(RichAttributeErrorBaseType):
    """
    Stores a farewell style.
    
    Attributes
    ----------    
    client_id : `int`
        Client identifier to associate with the welcome style.
    
    items : `tuple<FarewellStyleItem>`
        Items to pick when farewelling.
    
    name : `str`
        The farewell style's name.
    """
    __slots__ = ('client_id', 'items', 'name')
    
    
    def __new__(cls, name, client_id, items):
        """
        Creates a new farewell style instance.
        
        Parameters
        ----------
        name : `str`
            The farewell style's name.
        
        client_id : `int`
            Client identifier to associate with the welcome style.
        
        items : `tuple<FarewellStyleItem>`
            Items to pick when farewelling.
        """
        self = object.__new__(cls)
        self.client_id = client_id
        self.items = items
        self.name = name
        return self
    
    
    def __repr__(self):
        """Returns the farewell style's representation."""
        repr_parts = ['<', type(self).__name__]
        
        # name
        repr_parts.append(' name = ')
        repr_parts.append(repr(self.name))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
