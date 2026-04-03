__all__ = ()

from scarletio import RichAttributeErrorBaseType


class TextWallMode(RichAttributeErrorBaseType):
    """
    Represents a mode for the text wall command.
    
    Attributes
    ----------
    builder : `FunctionType`
        Output builder.
    
    name : `str`
        Name of the mode.
    
    splitter : `FunctionType`
        Function to split the input string.
    """
    __slots__ = ('builder', 'name', 'splitter')
    
    def __new__(cls, name, splitter, builder):
        """
        Creates a new text wall mode instance.
        
        Parameters
        ----------
        name : `str`
            Name of the mode.
        
        splitter : `FunctionType`
            Function to split the input string.
        
        builder : `FunctionType`
            Output builder.
        """
        self = object.__new__(cls)
        self.builder = builder
        self.name = name
        self.splitter = splitter
        return self
    
    
    def __repr__(self):
        """Returns repr(self)-"""
        repr_parts = ['<', type(self).__name__]
        
        # name
        repr_parts.append(' name = ')
        repr_parts.append(repr(self.name))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
