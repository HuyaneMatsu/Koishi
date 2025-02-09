__all__ = ('get_relationship_divorce_reduction_required_balance',)


def get_relationship_divorce_reduction_required_balance(user_id, divorce_count):
    """
    Gets how much balance is to hire ninjas to locate and burn relationship divorce papers.
    
    Parameters
    ----------
    user_id : `int`
        User identifier.
    
    divorce_count : `int`
        The amount of divorces of the user.
    
    Returns
    -------
    required_balance : `int`
    """
    return (4096 * divorce_count) + (user_id >> 22) % (8192 * divorce_count)
