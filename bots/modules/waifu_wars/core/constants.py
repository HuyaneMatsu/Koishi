__all__ = ('WAIFU_SCORE_GRAPH_CHART_LABELS', )

from math import log2

WAIFU_SCORE_GRAPH_CHART_LABELS = ['Housewife capabilities', 'Cuteness', 'Bedroom skills', 'Charm', 'Loyalty']


def get_embed_color(user_id):
    return (user_id >> 22) & 0xffffff

def get_user_graph_colors(user_id):
    return (
        str((user_id >> 38) & 0xff),
        str((user_id >> 30) & 0xff),
        str((user_id >> 22) & 0xff),
    )

def calculate_stat_upgrade_cost(all_, next_):
    return (next_ * 100) * log2(2.0 + all_)
