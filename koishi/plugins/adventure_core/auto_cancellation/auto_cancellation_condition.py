__all__ = ('AutoCancellationCondition',)

from scarletio import RichAttributeErrorBaseType


class AutoCancellationCondition(RichAttributeErrorBaseType):
    """
    A condition of an auto cancellation rule.
    
    Attributes
    ----------
    condition : `int`
        The condition's identifier.
    
    threshold : `int`
        Threshold value.
    """
    __slots__ = ('condition', 'threshold')
    
    def __new__(cls, condition, threshold):
        """
        
        Parameters
        ----------
        condition : `int`
            Condition identifier.
        
        threshold : `int`
            Threshold value.
        """
        self = object.__new__(cls)
        self.condition = condition
        self.threshold = threshold
        return self
    
    
    def __repr__(self):
        """Return repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # condition
        repr_parts.append(', condition = ')
        repr_parts.append(repr(self.condition))
        
        # threshold
        repr_parts.append(', threshold = ')
        repr_parts.append(repr(self.threshold))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns self == other."""
        if type(self) is not type(other):
            return NotImplemented
        
        # condition
        if self.condition != other.condition:
            return False
        
        # threshold
        if self.threshold != other.threshold:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns hash(self)."""
        hash_value = 0
        
        # condition
        hash_value ^= self.condition << 16
        
        # threshold
        hash_value ^= self.threshold
        
        return hash_value
