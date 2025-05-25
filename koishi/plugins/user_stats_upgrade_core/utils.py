__all__ = ('calculate_stat_upgrade_cost',)

from math import floor, log


def calculate_stat_upgrade_cost(total_points, next_point):
    """
    Calculates upgrading a stat for the given level.
    
    Parameters
    ----------
    total_points : `int`
        The user's total stat points.
    
    next_point
        The next point in the specific stat.
    
    Returns
    -------
    stat_upgrade_cost : `int`
    """
    next_point = (2 + next_point * 5)
    return floor(total_points * next_point * log(total_points * next_point) * 0.5)
