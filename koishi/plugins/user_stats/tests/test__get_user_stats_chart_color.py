import vampytest

from hata import Color

from ...user_stats_core import UserStats

from ..chart import get_user_stats_chart_color


def _iter_options():
    expected_output = 0x123425
    user_stats = UserStats((((5566 << 24) | expected_output) << 22) | 4555)
    user_stats.stat_housewife = 0
    user_stats.stat_cuteness = 0
    user_stats.stat_bedroom = 0
    user_stats.stat_charm = 0
    user_stats.stat_loyalty = 0
    
    yield (
        user_stats,
        Color(expected_output),
    )
    
    user_stats = UserStats(202503120000)
    user_stats.stat_housewife = 10
    user_stats.stat_cuteness = 0
    user_stats.stat_bedroom = 0
    user_stats.stat_charm = 0
    user_stats.stat_loyalty = 0
    
    yield (
        user_stats,
        Color(0xff9900),
    )
    
    user_stats = UserStats(202503120001)
    user_stats.stat_housewife = 0
    user_stats.stat_cuteness = 10
    user_stats.stat_bedroom = 0
    user_stats.stat_charm = 0
    user_stats.stat_loyalty = 0
    
    yield (
        user_stats,
        Color(0xff0099),
    )
    
    user_stats = UserStats(202503120002)
    user_stats.stat_housewife = 0
    user_stats.stat_cuteness = 0
    user_stats.stat_bedroom = 10
    user_stats.stat_charm = 0
    user_stats.stat_loyalty = 0
    
    yield (
        user_stats,
        Color(0x3300ff),
    )
    
    user_stats = UserStats(202503120003)
    user_stats.stat_housewife = 0
    user_stats.stat_cuteness = 0
    user_stats.stat_bedroom = 0
    user_stats.stat_charm = 10
    user_stats.stat_loyalty = 0
    
    yield (
        user_stats,
        Color(0x00ffff),
    )
    
    user_stats = UserStats(202503120004)
    user_stats.stat_housewife = 0
    user_stats.stat_cuteness = 0
    user_stats.stat_bedroom = 0
    user_stats.stat_charm = 0
    user_stats.stat_loyalty = 10
    
    yield (
        user_stats,
        Color(0x33ff00),
    )
    
    user_stats = UserStats(202503120005)
    user_stats.stat_housewife = 10
    user_stats.stat_cuteness = 10
    user_stats.stat_bedroom = 10
    user_stats.stat_charm = 10
    user_stats.stat_loyalty = 10
    
    yield (
        user_stats,
        Color(0x57948a),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_user_stats_chart_color(user_stats):
    """
    Tests whether ``get_user_stats_chart_color`` works as intended.
    
    Parameters
    ----------
    user_stats : ``UserStats``
        The user's stats
    
    Returns
    -------
    output : ``Color``
    """
    output = get_user_stats_chart_color(user_stats)
    vampytest.assert_instance(output, Color)
    return output
