__all__ = ('Return',)

from scarletio import RichAttributeErrorBaseType


class Return(RichAttributeErrorBaseType):
    """
    Represents a return.
    
    Attributes
    ----------
    id : `int`
        The identifier of the return.
    
    name : `str`
        The return's name.
    """
    __slots__ =( 'id', 'name')
    
    def __new__(cls, return_id, name):
        """
        Creates a new return.
        
        Parameters
        ----------
        return_id : `int`
            The identifier of the return.
        
        name : `str`
            The return's name.
        """
        self = object.__new__(cls)
        self.id = return_id
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
