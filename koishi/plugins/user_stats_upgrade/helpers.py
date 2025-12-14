__all__ = ()

from math import floor, log


def get_upgrade_cost_single(cumulative_stats, stat_incremented):
    """
    Calculates upgrading a stat for the given level.
    
    Parameters
    ----------
    cumulative_stats : `int`
        The user's total stat points.
    
    stat_incremented : `int`
        The next point in the specific stat.
    
    Returns
    -------
    stat_upgrade_cost : `int`
    """
    stat_incremented = (2 + stat_incremented * 5)
    return floor(cumulative_stats * stat_incremented * log(cumulative_stats * stat_incremented) * 0.5)


def get_upgrade_cost_cumulative(
    stat_housewife,
    stat_cuteness,
    stat_bedroom,
    stat_charm,
    stat_loyalty,
    modify_housewife_by,
    modify_cuteness_by,
    modify_bedroom_by,
    modify_charm_by,
    modify_loyalty_by,
):
    """
    calculates the upgrade cost.
    
    Parameters
    ----------
    stat_housewife : `int`
        The user's current housewife stat.
    
    stat_cuteness : `int`
        The user's current cuteness stat.
    
    stat_bedroom : `int`
        The user's current bedroom stat.
    
    stat_charm : `int`
        The user's current charm stat.
    
    stat_loyalty : `int`
        The user's current loyalty stat.
    
    modify_housewife_by : `int`
        The amount to modify the housewife stat by.
    
    modify_cuteness_by : `int`
        The amount to modify the cuteness stat by.
    
    modify_bedroom_by : `int`
        The amount to modify the bedroom stat by.
    
    modify_charm_by : `int`
        The amount to modify the charm stat by.
    
    modify_loyalty_by : `int`
        The amount to modify the loyalty stat by.
    
    Returns
    -------
    upgrade_cost_cumulative : `int`
    """
    cumulative_stats = stat_housewife + stat_cuteness + stat_bedroom + stat_charm + stat_loyalty
    upgrade_cost_cumulative = 0
    
    for _ in range(modify_housewife_by):
        stat_housewife += 1
        upgrade_cost_cumulative += get_upgrade_cost_single(cumulative_stats, stat_housewife)
        cumulative_stats += 1
    
    for _ in range(modify_cuteness_by):
        stat_cuteness += 1
        upgrade_cost_cumulative += get_upgrade_cost_single(cumulative_stats, stat_cuteness)
        cumulative_stats += 1
    
    for _ in range(modify_bedroom_by):
        stat_bedroom += 1
        upgrade_cost_cumulative += get_upgrade_cost_single(cumulative_stats, stat_bedroom)
        cumulative_stats += 1
    
    for _ in range(modify_charm_by):
        stat_charm += 1
        upgrade_cost_cumulative += get_upgrade_cost_single(cumulative_stats, stat_charm)
        cumulative_stats += 1
    
    for _ in range(modify_loyalty_by):
        stat_loyalty += 1
        upgrade_cost_cumulative += get_upgrade_cost_single(cumulative_stats, stat_loyalty)
        cumulative_stats += 1
    
    return upgrade_cost_cumulative
