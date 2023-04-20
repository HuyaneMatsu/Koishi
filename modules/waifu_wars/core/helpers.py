__all__ = ()

from math import floor, log

from hata import Color

from .constants import (
    STAT_COLOR_BEDROOM, STAT_COLOR_CHARM, STAT_COLOR_CUTENESS, STAT_COLOR_HOUSEWIFE, STAT_COLOR_LOYALTY
)


def get_default_color(user_id):
    """
    Gets default color for the given user identifier.
    
    Parameters
    ----------
    user_id : `int`
        A user's identifier.
    
    Returns
    -------
    color : ``Color``
    """
    return Color((user_id >> 22) & 0xffffff)


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
    return floor(total_points * next_point * log(total_points) * log(next_point) * 0.5)


def get_user_chart_color(user_id, stat_housewife, stat_cuteness, stat_bedroom, stat_charm, stat_loyalty):
    """
    Gets chart color for the given user.
    
    Parameters
    ----------
    user_id : `int`
        The user's identifier.  
    stat_housewife : `int`
        The user's housewife stat.
    stat_cuteness : `int`
        The user's cuteness stat.
    stat_bedroom : `int`
        The user's bedroom stat.
    stat_charm : `int`
        The user's charm stat.
    stat_loyalty : `int`
        The user's loyalty stat.
    
    Returns
    -------
    color : ``Color``
    """
    stat_max = max(stat_housewife, stat_cuteness, stat_bedroom, stat_charm, stat_loyalty)
    if stat_max == 0:
        return get_default_color(user_id)
    
    stat_min = min(stat_housewife, stat_cuteness, stat_bedroom, stat_charm, stat_loyalty)
    
    absorption = (stat_max + stat_min) * (1.0 / 3.0)
    
    stat_housewife = max(stat_housewife - absorption, 0.0)
    stat_cuteness = max(stat_cuteness - absorption, 0.0)
    stat_bedroom = max(stat_bedroom - absorption, 0.0)
    stat_charm = max(stat_charm - absorption, 0.0)
    stat_loyalty = max(stat_loyalty - absorption, 0.0)
    stat_default = max((stat_min - absorption) * 2.0, 0.0)
    
    stat_total = stat_housewife + stat_cuteness + stat_bedroom + stat_charm + stat_loyalty + stat_default
    default_color = get_default_color(user_id)
    
    return Color.from_rgb(
        floor((
            stat_housewife * STAT_COLOR_HOUSEWIFE.red +
            stat_cuteness * STAT_COLOR_CUTENESS.red +
            stat_bedroom * STAT_COLOR_BEDROOM.red +
            stat_charm * STAT_COLOR_CHARM.red +
            stat_loyalty * STAT_COLOR_LOYALTY.red +
            stat_default * default_color.red
        ) / stat_total),
        floor((
            stat_housewife * STAT_COLOR_HOUSEWIFE.green +
            stat_cuteness * STAT_COLOR_CUTENESS.green +
            stat_bedroom * STAT_COLOR_BEDROOM.green +
            stat_charm * STAT_COLOR_CHARM.green +
            stat_loyalty * STAT_COLOR_LOYALTY.green +
            stat_default * default_color.green
        ) / stat_total),
        floor((
            stat_housewife * STAT_COLOR_HOUSEWIFE.blue +
            stat_cuteness * STAT_COLOR_CUTENESS.blue +
            stat_bedroom * STAT_COLOR_BEDROOM.blue +
            stat_charm * STAT_COLOR_CHARM.blue +
            stat_loyalty * STAT_COLOR_LOYALTY.blue +
            stat_default * default_color.blue
        ) / stat_total),
    )
