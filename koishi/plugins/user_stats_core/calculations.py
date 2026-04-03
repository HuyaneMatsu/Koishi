__all__ = ()

#   +---------------+-----------+-----------+-----------+-----------+-----------+
#   | name          | bedroom   | charm     | cuteness  | housewife | loyalty   |
#   +===============+===========+===========+===========+===========+===========+
#   | fishing       | 3         | 0         | 0         | 3         | 4         |
#   +---------------+-----------+-----------+-----------+-----------+-----------+
#   | gardening     | 0         | 0         | 2         | 6         | 2         |
#   +---------------+-----------+-----------+-----------+-----------+-----------+
#   | foraging      | 2         | 3         | 3         | 2         | 0         |
#   +---------------+-----------+-----------+-----------+-----------+-----------+
#   | butchering    | 3         | 0         | 3         | 4         | 0         |
#   +---------------+-----------+-----------+-----------+-----------+-----------+
#   | hunting       | 0         | 6         | 0         | 0         | 4         |
#   +---------------+-----------+-----------+-----------+-----------+-----------+
#   | inventory     | 3         | 3         | 0         | 4         | 0         |
#   +---------------+-----------+-----------+-----------+-----------+-----------+
#   | movement      | 2         | 0         | 4         | 2         | 2         |
#   +---------------+-----------+-----------+-----------+-----------+-----------+
#   | health        | 3         | 0         | 0         | 2         | 2         |
#   +---------------+-----------+-----------+-----------+-----------+-----------+
#   | energy        | 0         | 4         | 4         | 2         | 0         |
#   +---------------+-----------+-----------+-----------+-----------+-----------+
#   | total         | 16        | 16        | 16        | 23        | 14        |
#   +---------------+-----------+-----------+-----------+-----------+-----------+


def calculate_fishing(stat_bedroom, stat_charm, stat_cuteness, stat_housewife, stat_loyalty):
    """
    Calculates the fishing for the given stats.
    
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
    fishing : `int`
    """
    return 10 + (stat_bedroom * 3 + stat_housewife * 3 + stat_loyalty * 4) // 10 


def calculate_gardening(stat_bedroom, stat_charm, stat_cuteness, stat_housewife, stat_loyalty):
    """
    Calculates the gardening for the given stats.
    
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
    gardening : `int`
    """
    return 10 + (stat_cuteness * 2 + stat_housewife * 6 + stat_loyalty * 2) // 10 


def calculate_foraging(stat_bedroom, stat_charm, stat_cuteness, stat_housewife, stat_loyalty):
    """
    Calculates the foraging for the given stats.
    
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
    foraging : `int`
    """
    return 10 + (stat_bedroom * 2 + stat_charm * 3 + stat_cuteness * 3 + stat_housewife * 2) // 10 


def calculate_butchering(stat_bedroom, stat_charm, stat_cuteness, stat_housewife, stat_loyalty):
    """
    Calculates the butchering for the given stats.
    
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
    butchering : `int`
    """
    return 10 + (stat_bedroom * 3 + stat_cuteness * 3 + stat_housewife * 4) // 10 


def calculate_hunting(stat_bedroom, stat_charm, stat_cuteness, stat_housewife, stat_loyalty):
    """
    Calculates the hunting for the given stats.
    
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
    hunting : `int`
    """
    return 10 + (stat_charm * 6 + stat_loyalty * 4) // 10 


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


def calculate_movement(stat_bedroom, stat_charm, stat_cuteness, stat_housewife, stat_loyalty):
    """
    Calculates the movement for the given stats.
    
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
    movement : `int`
    """
    return 800 + stat_bedroom * 8 + stat_cuteness * 16 + stat_housewife * 8 + stat_loyalty * 8


def calculate_health(stat_bedroom, stat_charm, stat_cuteness, stat_housewife, stat_loyalty):
    """
    Calculates the health for the given stats.
    
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
    health : `int`
    """
    return 100 + stat_bedroom * 3 + stat_housewife * 2 + stat_loyalty * 5


def calculate_energy(stat_bedroom, stat_charm, stat_cuteness, stat_housewife, stat_loyalty):
    """
    Calculates the energy for the given stats.
    
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
    energy : `int`
    """
    return 100 + stat_charm * 4 + stat_cuteness * 4 + stat_housewife * 2
