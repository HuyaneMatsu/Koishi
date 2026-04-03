__all__ = ()


def pack_action_types(action_types):
    """
    Packs the given action types.
    
    Parameters
    ----------
    action_types : `tuple<int>`
        The unpacked action types.
    
    Returns
    -------
    packed : `int`
    """
    packed = 0
    
    for action_type in action_types:
        packed |= (1 << action_type)
    
    return packed


def unpack_action_types(packed):
    """
    Unpacks the given packed action types.
    
    Parameters
    ----------
    packed : `int`
        The packed value.
    
    Returns
    -------
    action_types : `tuple<int>`
    """
    action_types_unpacked = []
    
    action_type = 0
    while packed:
        if packed & 1:
            action_types_unpacked.append(action_type)
        
        action_type += 1
        packed >>= 1
        continue
    
    return tuple(action_types_unpacked)
