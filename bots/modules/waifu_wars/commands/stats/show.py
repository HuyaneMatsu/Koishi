__all__ = ('show',)

from math import floor

from hata import Embed
from scarletio import to_json
from scarletio.web_common import quote

from ...core.constants import STAT_NAMES_FULL
from ...core.helpers import get_user_chart_color
from ...core.table_building import build_table_into


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
        max(stat_housewife, stat_cuteness, stat_bedroom, stat_charm, stat_loyalty),
        10,
    )


def get_waifu_stats_chart_url_and_color(waifu_stats):
    """
    Gets the url to the user's waifu chart.
    
    Parameters
    ----------
    waifu_stats : ``WaifuStats``
        A user's waifu stats.
    
    Returns
    -------
    url : `str`
    color : `int`
    """
    stat_housewife = waifu_stats.stat_housewife
    stat_cuteness = waifu_stats.stat_cuteness
    stat_bedroom = waifu_stats.stat_bedroom
    stat_charm = waifu_stats.stat_charm
    stat_loyalty = waifu_stats.stat_loyalty
    
    chart_color = get_user_chart_color(
        waifu_stats.user_id,
        stat_housewife,
        stat_cuteness,
        stat_bedroom,
        stat_charm,
        stat_loyalty,
    )
    
    data = to_json({
        'type': 'radar',
        'data': {
            'labels': STAT_NAMES_FULL,
            'datasets': [
                {
                    'data': [
                        stat_housewife,
                        stat_cuteness,
                        stat_bedroom,
                        stat_charm,
                        stat_loyalty,
                    ],
                    'borderColor': f'rgb({chart_color.red} {chart_color.green} {chart_color.blue})',
                    'backgroundColor': f'rgba({chart_color.red} {chart_color.green} {chart_color.blue} 0.2)',
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
    
    return f'https://quickchart.io/chart?width=500&height=300&c={quote(data)}', chart_color


def get_waifu_stats_description(waifu_stats):
    """
    Gets description for the user's stats.
    
    Parameters
    ----------
    waifu_stats : ``WaifuStats``
        A user's waifu stats.
    
    Returns
    -------
    description : `str`
    """
    into = ['```\n']
    build_table_into(
        into,
        (
            'Stat',
            'Amount'
        ),
        (
            STAT_NAMES_FULL,
            [
                str(waifu_stats.stat_housewife),
                str(waifu_stats.stat_cuteness),
                str(waifu_stats.stat_bedroom),
                str(waifu_stats.stat_charm),
                str(waifu_stats.stat_loyalty),
            ],
        ),
    )
    into.append('```\n')
    return ''.join(into)
    

async def show(
    event,
    user: ('user', 'Select someone else?') = None,
):
    """
    Shows your waifu stats.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    user : `None`, ``ClientUserBase`` = `None`, Optional
        The selected user.
    
    Returns
    -------
    response : ``Embed``
    """
    if user is None:
        user = event.user
    
    waifu_stats = await user.waifu_stats
    chart_url, color = get_waifu_stats_chart_url_and_color(waifu_stats)
    
    return Embed(
        f'{user:f}\'s waifu stats',
        get_waifu_stats_description(waifu_stats),
        color = color,
    ).add_image(
        chart_url,
    )
