__all__ = ('WAIFU_SCORE_GRAPH_CHART_LABELS', )

from math import log2, floor

STAT_COUNT = 5
WAIFU_SCORE_GRAPH_CHART_LABELS = ['Housewife capabilities', 'Cuteness', 'Bedroom skills', 'Charm', 'Loyalty']

STAT_MASKS = [
    219902325437,
    219902325439,
    219902325491,
    219902325497,
    219902325523,
]


def get_embed_color(user_id):
    return (user_id >> 22) & 0xffffff

def get_user_graph_colors(user_id):
    return (
        str((user_id >> 38) & 0xff),
        str((user_id >> 30) & 0xff),
        str((user_id >> 22) & 0xff),
    )

def get_multiplier_fields(value):
    positive = [(value - 1) % STAT_COUNT, (value + 1) % STAT_COUNT]
    negative = [index for index in range(STAT_COUNT) if (index != value) and (value not in positive)]
    
    return positive, negative


def generate_multiplier_fields():
    return {index: get_multiplier_fields(index) for index in range(STAT_COUNT)}


MULTIPLIER_FIELDS = generate_multiplier_fields()
MULTIPLIER_FACTOR = 1.0 / 4.0
MAX_MULTIPLIER = 10.0 * MULTIPLIER_FACTOR


def get_default_user_stats(user_id):
    # structure:
    # 1 bit +/-
    # 41 date
    # 22 bit server info
    
    # We use only the date one, so everything we use is shifted by 22 bits
    # then we cut down the last 24 bits of the date and switch it with the first 19
    mask = ((user_id & 0x1ffffc00000000000) >> 46) | ((user_id & 0x3fffffc00000) >> 3)
    
    stats = [(mask & stat_mask) % 11 for stat_mask in STAT_MASKS]
    
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
    
    return stats


def calculate_stat_upgrade_cost(all_, next_):
    return (next_ * 100) * log2(2.0 + all_)
