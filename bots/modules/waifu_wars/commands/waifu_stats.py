from hata import Client, Embed
from scarletio import to_json
from scarletio.web_common import quote
from hata.ext.extension_loader import import_extension

WAIFU_SCORE_GRAPH_CHART_LABELS, get_user_graph_colors, get_embed_color = \
    import_extension('..core.constants', 'WAIFU_SCORE_GRAPH_CHART_LABELS', 'get_user_graph_colors', 'get_embed_color')

SLASH_CLIENT: Client

WAIFU_SCORE_GRAPH_CHART_OPTIONS = {
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
        'display': False
    },
}


@SLASH_CLIENT.interactions(is_global=True)
async def waifu_stats(
    event,
    user: ('user', 'Select someone else?') = None,
):
    if user is None:
        user = event.user
    
    user_id = user.id
    
    waifu_stats = await user.waifu_stats
    red, green, blue = get_user_graph_colors(user_id)
    color = get_embed_color(user_id)
    
    data = to_json({
        'type': 'radar',
        'data': {
            'labels': WAIFU_SCORE_GRAPH_CHART_LABELS,
            'datasets': [
                {
                    'data': [
                        waifu_stats.stat_housewife,
                        waifu_stats.stat_cuteness,
                        waifu_stats.stat_bedroom,
                        waifu_stats.stat_charm,
                        waifu_stats.stat_loyalty,
                    ],
                    'borderColor': f'rgb({red} {green} {blue})',
                    'backgroundColor': f'rgba({red} {green} {blue} 0.2)',
                },
            ],
        },
        'options': WAIFU_SCORE_GRAPH_CHART_OPTIONS,
    })
    
    chart_url = f'https://quickchart.io/chart?width=500&height=300&c={quote(data)}'
    
    return Embed(
        f'{user:f}\'s waifu score',
        color = color,
    ).add_image(
        chart_url,
    )
