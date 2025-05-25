__all__ = ()


def generate_user_stats_defaults(user_id):
    """
    Generates the default stats for the given user identifier.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    user_id : `int`
        The user's identifier.
    
    Yields
    ------
    stat_default : `int`
    """
    mask = ((user_id & 0x1ffffc00000000000) >> 46) | ((user_id & 0x3fffffc00000) >> 3)
    for shift in range(0, 20, 4):
        yield min(((mask >> shift) & 0b1111) + 1, 10)
