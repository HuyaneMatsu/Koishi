__all__ = ()

def accumulate_item_weight(*items):
    """
    Accumulates the weights of the given items.
    
    Parameters
    ----------
    *items : ``None | Item``
        Items to accumulate their wight of.
    
    Returns
    -------
    accumulated_item_weight : `int`
    """
    accumulated_item_weight = 0
    for item in items:
        if (item is not None):
            accumulated_item_weight += item.weight
    
    return accumulated_item_weight


def calculate_inventory(stat_bedroom, stat_charm, stat_cuteness, stat_housewife, stat_loyalty):
    """
    Calculates the inventory for the given stats.
    
    Parameters
    ----------
    stat_bedroom : `int`
        The user's bedroom skills.
    
    stat_charm : `int`
        The user's charm.
    
    stat_cuteness : `int`
        The user's cuteness.
    
    stat_housewife : `int`
        The user's housewife capabilities.
    
    stat_loyalty : `int`
        The user's loyalty.
    
    Returns
    -------
    inventory : `int`
    """
    return 25000 + stat_bedroom * 750 + stat_charm * 750 + stat_housewife * 1000


def calculate_fishing(stat_bedroom, stat_charm, stat_cuteness, stat_housewife, stat_loyalty):
    """
    Calculates the fishing for the given stats.
    
    Parameters
    ----------
    stat_bedroom : `int`
        The user's bedroom skills.P
    
    stat_charm : `int`
        The user's charm.
    
    stat_cuteness : `int`
        The user's cuteness.
    
    stat_housewife : `int`
        The user's housewife capabilities.
    
    stat_loyalty : `int`
        The user's loyalty.
    
    Returns
    -------
    fishing : `int`
    """
    return 10 + (stat_housewife * 3 + stat_loyalty * 4 + stat_bedroom * 3) // 10 
