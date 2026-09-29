__all__ = ('Target', 'target_create')


from scarletio import RichType


class Target(metaclass = RichType, rich_type_feature_flags = ~0):
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


def target_create(target_id, name, duration_suggestion_set_id, action_ids):
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
    
    Returns
    -------
    target : ``Target``
    """
    target = object.__new__(Target)
    target.action_ids = action_ids
    target.id = target_id
    target.duration_suggestion_set_id = duration_suggestion_set_id
    target.name = name
    return target
