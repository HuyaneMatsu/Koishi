__all__ = ('Target',)


from scarletio import RichAttributeErrorBaseType


class Target(RichAttributeErrorBaseType):
    """
    Represents a target action of a location.
    
    Attributes
    ----------
    action_ids : `tuple<int>`
        The possible actions.
    
    duration_suggestion_set_id : `int`
        identifier for duration suggestions.
    
    id : `int`
        The identifier of the target.
    
    name : `str`
        The target's name.
    """
    __slots__ = ('action_ids', 'duration_suggestion_set_id', 'id', 'name')
    
    def __new__(cls, target_id, name, duration_suggestion_set_id, action_ids):
        """
        Creates a new target.
        
        Parameters
        ----------
        target_id : `int`
            The identifier of the target.
        
        name : `str`
            The target's name.
        
        duration_suggestion_set_id : `int`
            identifier for duration suggestions.
        
        action_ids : `tuple<int>`
            The possible actions.
        """
        self = object.__new__(cls)
        self.action_ids = action_ids
        self.id = target_id
        self.duration_suggestion_set_id = duration_suggestion_set_id
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
        
        # duration_suggestion_set_id
        repr_parts.append(', duration_suggestion_set_id = ')
        repr_parts.append(repr(self.duration_suggestion_set_id))
        
        # action_ids
        repr_parts.append(', action_ids = ')
        repr_parts.append(repr(self.action_ids))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
