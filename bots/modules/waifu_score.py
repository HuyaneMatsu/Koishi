from hata import Client, Embed
from bot_utils.constants import GUILD__SUPPORT
from random import Random
from hata.ext.extension_loader import require
from scarletio import to_json
from scarletio.web_common import quote

require('Marisa')

SLASH_CLIENT: Client

RANDOM_GENERATOR = Random()

WAIFU_SCORE_GRAPH_CHART_LABELS = ['Funny', 'Caring', 'Loyal', 'Creative', 'Horny', 'Smart', 'Attractive']

WAIFU_SCORE_GRAPH_CHART_OPTIONS = {
    'scale': {
        'ticks': {
            'suggestedMin': 2,
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


@SLASH_CLIENT.interactions(guild=GUILD__SUPPORT, name="waifu-score-preview")
async def waifu_score(
    client,
    event,
):
    user_id = event.user.id
    
    RANDOM_GENERATOR.seed(user_id)
    
    stats = [RANDOM_GENERATOR.randint(0, 10) for _ in range(7)]
    
    extra_index = RANDOM_GENERATOR.randint(0, 6)
    value = stats[extra_index] + RANDOM_GENERATOR.randint(0, 10)
    if value > 10:
        value = 10
    stats[extra_index] = value
    
    color_base = user_id >> 22
    
    red = str(color_base & 0xff0000)
    green = str(color_base & 0x00ff00)
    blue = str(color_base & 0x0000ff)
    
    data = to_json({
        'type': 'radar',
        'data': {
            'labels': WAIFU_SCORE_GRAPH_CHART_LABELS,
            'datasets': [
                {
                    'data': stats,
                    'borderColor': f'rgb({red} {green} {blue})',
                    'backgroundColor': f'rgba({red} {green} {blue} 0.2)',
                },
            ],
        },
        'options': GUILD__SUPPORT
    })

    chart_url = f'https://quickchart.io/chart?width=500&height=300&c={quote(data)}'
    
    return Embed(
        f'{event.user:f}\'s waifu score'
    ).add_image(
        chart_url,
    )
