__all__ = ('goal_deserialise', 'goal_listing_deserialise', 'goal_listing_serialise', 'goal_serialise')

from .goal import GOAL_BEHAVIOUR_ITEM_EXACT


PARSERS = {
    behaviour.type: behaviour.deserialise
    for behaviour in (
        GOAL_BEHAVIOUR_ITEM_EXACT,
    )
}


def goal_deserialise(data):
    """
    Deserialises the goal.
    
    Parameters
    ----------
    data : `bytes`
        Data to parse from.
    
    Returns
    -------
    goal : ``None | Goal``
    """
    data = memoryview(data)
    goal_type = data[0]
    try:
        deserialise = PARSERS[goal_type]
    except KeyError:
        return None
    
    output = deserialise(data, 1)
    if (output is None):
        return None
    
    return output[0]


def goal_listing_deserialise(data):
    """
    Deserialises the goal_listing.
    
    Parameters
    ----------
    data : `bytes`
        Data to parse from.
    
    Returns
    -------
    goal_listing : ``None | list<Goal>``
    """
    goal_listing = []
    chunk_start = 0
    data_length = len(data)
    data = memoryview(data)
    
    while True:
        goal_type = data[chunk_start]
        try:
            deserialise = PARSERS[goal_type]
        except KeyError:
            return None
        
        output = deserialise(data, chunk_start + 1)
        if (output is None):
            return None
        
        goal, chunk_start = output
        goal_listing.append(goal)
        
        # If we ar at the end of the data, break out.
        if chunk_start >= data_length:
            break
    
    return goal_listing


def goal_serialise(goal):
    """
    Serialises the goal.
    
    Parameters
    ----------
    goal : ``Goal``
        Goal to serialise.
    
    Returns
    -------
    data : `bytes`
    """
    return b''.join([
        goal.behaviour.type.to_bytes(1, 'little'),
        *goal.behaviour.serialise(goal.configuration)
    ])


def goal_listing_serialise(goal_listing):
    """
    Serialises the goal.
    
    Parameters
    ----------
    goal_listing : ``list<Goal>``
        Goal listing to serialise.
    
    Returns
    -------
    data : `bytes`
    """
    parts = []
    
    for goal in goal_listing:
        parts.append(goal.behaviour.type.to_bytes(1, 'little'))
        parts.extend(goal.behaviour.serialise(goal.configuration))
    
    return b''.join(parts)
