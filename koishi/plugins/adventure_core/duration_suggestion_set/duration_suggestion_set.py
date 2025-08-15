__all__ = ('DurationSuggestionSet',)

from scarletio import RichAttributeErrorBaseType


class DurationSuggestionSet(RichAttributeErrorBaseType):
    """
    Represents a duration suggestion set.
    
    Attributes
    ----------
    durations : `tuple<int>`
        The suggested durations.
    
    id : `int`
        The identifier of the duration suggestion set.
    """
    __slots__ = ('durations', 'id')
    
    def __new__(cls, duration_suggestion_set_id, durations):
        """
        Creates a new target.
        
        Parameters
        ----------
        duration_suggestion_set_id : `int`
            The identifier of the target.
        
        durations : `tuple<int>`
            The suggested durations.
        """
        self = object.__new__(cls)
        self.durations = durations
        self.id = duration_suggestion_set_id
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # id
        repr_parts.append(' id = ')
        repr_parts.append(repr(self.id))
        
        # durations
        repr_parts.append(', durations = ')
        repr_parts.append(repr(self.durations))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
