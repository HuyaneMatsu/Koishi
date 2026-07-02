__all__ = ('DataBaseField',)

from scarletio import RichAttributeErrorBaseType


class DataBaseField(RichAttributeErrorBaseType):
    """
    Represents a field of a data base.

    Attributes
    ----------
    name : `str`
        The field's name.
    
    data_type : ``DataType``
        Data type.
    """
    __slots__ = ('data_type', 'name')
    
    def __new__(cls, name, data_type):
        """
        Creates a nwe data base field.
        
        Parameters
        ----------
        name : `str`
            The field's name.
        
        data_type : ``DataType``
            Data type.
        """
        assert (name is not None) and (type(name) is str) and name
        self = object.__new__(cls)
        self.data_type = data_type
        self.name = name
        return self
        
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # name
        repr_parts.append(' name = ')
        repr_parts.append(repr(self.name))
        
        # data_type
        repr_parts.append(', data_type = ')
        repr_parts.append(self.data_type.name)
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns self == other."""
        if type(self) is not type(other):
            return NotImplemented
        
        # data_type
        if self.data_type is not other.data_type:
            return False
        
        # name
        if self.name != other.name:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns hash(self)."""
        return hash(self.data_type) ^ hash(self.name)
