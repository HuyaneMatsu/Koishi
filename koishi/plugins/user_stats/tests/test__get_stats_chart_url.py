import vampytest
from scarletio import from_json
from scarletio.web_common import URL
from hata import Color

from ...stats_core import Stats

from ..embed_builders import get_stats_chart_url


def _iter_options():
    stats = Stats(202503120010)
    stats.stat_housewife = 5
    stats.stat_cuteness = 6
    stats.stat_bedroom = 7
    stats.stat_charm = 8
    stats.stat_loyalty = 9
    
    yield (
        stats,
        Color(0xff55aa),
        {
            'type': 'radar',
            'data': {
                'labels': [
                    'Housewife capabilities',
                    'Cuteness',
                    'Bedroom skills',
                    'Charm',
                    'Loyalty',
                ],
                'datasets': [
                    {
                        'data': [5, 6, 7, 8, 9],
                        'borderColor': 'rgb(255 85 170)',
                        'backgroundColor': 'rgba(255 85 170 0.2)',
                    },
                ],
            },
            'options': {
                'scale': {
                    'ticks': {
                        'suggestedMin': 0,
                        'suggestedMax': 10,
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
                    'display': False,
                },
            },
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_stats_chart_url(stats, color):
    """
    Tests whether ``get_stats_chart_url`` works as intended.
    
    Parameters
    ----------
    stats : ``Stats``
        The user's stats
    
    color : ``Color``
        Color to use for the chart.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    url = get_stats_chart_url(stats, color)
    vampytest.assert_instance(url, str)
    url = URL(url, True)
    query = url.query
    vampytest.assert_is_not(query, None)
    chart_raw_data = query.get('c', None)
    vampytest.assert_is_not(chart_raw_data, None)
    return from_json(chart_raw_data)
