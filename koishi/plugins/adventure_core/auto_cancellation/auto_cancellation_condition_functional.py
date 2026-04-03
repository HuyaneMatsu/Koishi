__all__ = ('AutoCancellationConditionFunctional',)

from scarletio import RichAttributeErrorBaseType


class AutoCancellationConditionFunctional(RichAttributeErrorBaseType):
    """
    A functional condition of an auto cancellation rule.
    
    Attributes
    ----------
    function : `(object) : bool`
        Function to execute.
    
    name : `str`
        The name of the condition.
    """
    __slots__ = ('function', 'name')
    
    def __new__(cls, name, function):
        """
        Creates a new condition.
        
        Parameters
        ----------
        name : `str`
            The name of the condition.
        
        function : `(object) : bool`
            Function to execute.
        """
        self = object.__new__(cls)
        self.function = function
        self.name = name
        return self
    
    
    def __repr__(self):
        """Return repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # condition
        repr_parts.append(', name = ')
        repr_parts.append(repr(self.name))
        
        # threshold
        repr_parts.append(', function = ')
        repr_parts.append(repr(self.function))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns self == other."""
        if type(self) is not type(other):
            return NotImplemented
        
        # condition
        if self.name != other.name:
            return False
        
        # threshold
        if self.function is not other.function:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns hash(self)."""
        hash_value = 0
        
        # name
        hash_value ^= hash(self.name)
        
        # function
        hash_value ^= hash(self.function)
        
        return hash_value
