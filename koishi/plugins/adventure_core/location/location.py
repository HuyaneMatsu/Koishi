__all__ = ('Location', 'location_create')


from scarletio import RichType


class Location(metaclass = RichType, rich_type_feature_flags = ~0):
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
    
    level : `int`
        The level requirement for suggesting the location.
    """
    __slots__ = ('distance', 'id', 'level', 'name', 'target_ids')


def location_create(location_id, name, distance, target_ids, level):
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
    
    level : `int`
        The level requirement for suggesting the location.
    
    Returns
    -------
    location : ``Location``
    """
    location = object.__new__(Location)
    location.distance = distance
    location.id = location_id
    location.level = level
    location.name = name
    location.target_ids = target_ids
    return location
