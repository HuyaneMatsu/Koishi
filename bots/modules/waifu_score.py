from hata import Client, Embed
from scarletio import to_json
from scarletio.web_common import quote
from math import floor
from hashlib import md5

SLASH_CLIENT: Client

WAIFU_SCORE_GRAPH_CHART_LABELS = ['Housewife capabilities', 'Cuteness', 'Bedroom skills', 'Charm', 'Loyalty']

def create_mask(string):
    string = string.casefold().replace(' ', '')
    return int.from_bytes(md5(string.encode()).digest(), 'big') & 0xffffffffffffffff


MASK_MAP = [create_mask(string) for string in WAIFU_SCORE_GRAPH_CHART_LABELS]

STAT_COUNT = len(WAIFU_SCORE_GRAPH_CHART_LABELS)

def get_multiplier_fields(value):
    positive = [(value - 1) % STAT_COUNT, (value + 1) % STAT_COUNT]
    negative = [index for index in range(STAT_COUNT) if (index != value) and (value not in positive)]
    
    return positive, negative

def generate_multiplier_fields():
    return {index: get_multiplier_fields(index) for index in range(STAT_COUNT)}

MULTIPLIER_FIELDS = generate_multiplier_fields()
MULTIPLIER_FACTOR = 1.0 / 4.0
MAX_MULTIPLIER = 10.0 * MULTIPLIER_FACTOR


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
async def waifu_score(
    event,
    user: ('user', 'Select someone else?') = None,
):
    if user is None:
        user = event.user
    
    user_id = user.id
    
    color_mask = (user_id >> 22) & 0xffffff
    user_mask = (user_id >> (22 + 24)) | (color_mask << 21)
    
    stats = [(mask & user_mask) % 11 for mask in MASK_MAP]
    
    
    bonuses = [0.0 for x in range(STAT_COUNT)]
    
    for index in range(STAT_COUNT):
        bonus = stats[index] * MULTIPLIER_FACTOR
        positive, negative = MULTIPLIER_FIELDS[index]
        
        local_bonus = (bonus / len(positive))
        for index in positive:
            bonuses[index] += local_bonus
        
        bonus = MAX_MULTIPLIER - bonus
        
        local_bonus = (bonus / len(negative))
        for index in negative:
            bonuses[index] += local_bonus
    
    for index in range(STAT_COUNT):
        bonus = bonuses[index]
        bonus = floor(bonus)
        
        value = stats[index]
        
        value = value + bonus
        if value > 10:
            value = 10
        
        stats[index] = value
    
    red = str((color_mask & 0xff0000) >> 16)
    green = str((color_mask & 0x00ff00) >> 8)
    blue = str(color_mask & 0x0000ff)
    
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
        'options': WAIFU_SCORE_GRAPH_CHART_OPTIONS,
    })

    chart_url = f'https://quickchart.io/chart?width=500&height=300&c={quote(data)}'
    
    return Embed(
        f'{user:f}\'s waifu score',
        color = color_mask,
    ).add_image(
        chart_url,
    )
