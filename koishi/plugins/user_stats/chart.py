__all__ = ()

from math import floor

from hata import Color
from scarletio import to_json
from scarletio.web_common import quote

from ..user_stats_core import (
    USER_STAT_NAME_FULL_BEDROOM, USER_STAT_NAME_FULL_CHARM, USER_STAT_NAME_FULL_CUTENESS, USER_STAT_NAME_FULL_HOUSEWIFE,
    USER_STAT_NAME_FULL_LOYALTY
)

from .constants import (
    STAT_COLOR_BEDROOM, STAT_COLOR_CHARM, STAT_COLOR_CUTENESS, STAT_COLOR_HOUSEWIFE, STAT_COLOR_LOYALTY,
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


def get_user_stats_chart_color(user_stats):
    """
    Gets chart color for the given user.
    
    Parameters
    ----------
    user_stats : ``UserStats``
        The user's stats
    
    Returns
    -------
    color : ``Color``
    """
    user_id = user_stats.user_id
    stats_calculated = user_stats.stats_calculated
    stat_housewife = stats_calculated.stat_housewife
    stat_cuteness = stats_calculated.stat_cuteness
    stat_bedroom = stats_calculated.stat_bedroom
    stat_charm = stats_calculated.stat_charm
    stat_loyalty = stats_calculated.stat_loyalty
    
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


def get_chart_suggested_max(stat_housewife, stat_cuteness, stat_bedroom, stat_charm, stat_loyalty):
    """
    Gets the suggested max stats for the chart.
    
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
    suggested_max : `int`
    """
    return max(
        floor((stat_housewife + stat_cuteness + stat_bedroom + stat_charm + stat_loyalty) * (1.34 / 5.0)),
        stat_housewife,
        stat_cuteness,
        stat_bedroom,
        stat_charm,
        stat_loyalty,
        10,
    )


def get_user_stats_chart_url(user_stats, color):
    """
    Gets the url to the user's stats chart.
    
    Parameters
    ----------
    user_stats : ``UserStats``
        The user's stats
    
    color : ``Color`
        Color to use for the chart.
    
    Returns
    -------
    url : `str`
    """
    stats_calculated = user_stats.stats_calculated
    stat_housewife = stats_calculated.stat_housewife
    stat_cuteness = stats_calculated.stat_cuteness
    stat_bedroom = stats_calculated.stat_bedroom
    stat_charm = stats_calculated.stat_charm
    stat_loyalty = stats_calculated.stat_loyalty
    
    data = to_json({
        'type': 'radar',
        'data': {
            'labels': (
                USER_STAT_NAME_FULL_HOUSEWIFE,
                USER_STAT_NAME_FULL_CUTENESS,
                USER_STAT_NAME_FULL_BEDROOM,
                USER_STAT_NAME_FULL_CHARM,
                USER_STAT_NAME_FULL_LOYALTY,
            ),
            'datasets': [
                {
                    'data': [
                        stat_housewife,
                        stat_cuteness,
                        stat_bedroom,
                        stat_charm,
                        stat_loyalty,
                    ],
                    'borderColor': f'rgb({color.red} {color.green} {color.blue})',
                    'backgroundColor': f'rgba({color.red} {color.green} {color.blue} 0.2)',
                },
            ],
        },
        'options': {
            'scale': {
                'ticks': {
                    'suggestedMin': 0,
                    'suggestedMax': get_chart_suggested_max(
                        stat_housewife,
                        stat_cuteness,
                        stat_bedroom,
                        stat_charm,
                        stat_loyalty,
                    ),
                    'fontColor': 'white',
                    'backdropColor': 'transparent',
                },
                'angleLines': {
                    'color': 'white',
                },
                'pointLabels': {
                    'fontColor': 'white',
                },
                'gridLines': {
                    'color': 'white',
                },
            },
            'legend': {
                'display': False
            },
        }
    })
    
    return f'https://quickchart.io/chart?width=500&height=300&c={quote(data)}'
