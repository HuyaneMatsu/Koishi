__all__ = ('Location',)


from scarletio import RichAttributeErrorBaseType


class Location(RichAttributeErrorBaseType):
    """
    Represents a location to adventure at.
    
    Attributes
    ----------
    distance : `int`
        The distance to the location in meters.
    
    id : `int`
        The identifier of the location.
    
    name : `str`
        The location's name.
    
    target_ids : `tuple<int>`
        The available target actions at the location.
    """
    __slots__ = ('distance', 'id', 'name', 'target_ids', )
    
    def __new__(cls, location_id, name, distance, target_ids):
        """
        Creates a new location.
        
        Parameters
        ----------
        location_id : `int`
            The identifier of the location.
        
        name : `str`
            The location's name.
        
        distance : `int`
            The distance to the location in meters.
        
        target_ids : `tuple<int>`
            The available target actions at the location.
        """
        self = object.__new__(cls)
        self.distance = distance
        self.id = location_id
        self.name = name
        self.target_ids = target_ids
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
        
        # distance
        repr_parts.append(', distance = ')
        repr_parts.append(repr(self.distance))
        
        # target_ids
        repr_parts.append(', target_ids = ')
        repr_parts.append(repr(self.target_ids))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
