import vampytest

from hata import Color

from ...stats_core import Stats

from ..embed_builders import get_user_chart_color


def _iter_options():
    expected_output = 0x123425
    stats = Stats((((5566 << 24) | expected_output) << 22) | 4555)
    stats.stat_housewife = 0
    stats.stat_cuteness = 0
    stats.stat_bedroom = 0
    stats.stat_charm = 0
    stats.stat_loyalty = 0
    
    yield (
        stats,
        Color(expected_output),
    )
    
    stats = Stats(202503120000)
    stats.stat_housewife = 10
    stats.stat_cuteness = 0
    stats.stat_bedroom = 0
    stats.stat_charm = 0
    stats.stat_loyalty = 0
    
    yield (
        stats,
        Color(0xff9900),
    )
    
    stats = Stats(202503120001)
    stats.stat_housewife = 0
    stats.stat_cuteness = 10
    stats.stat_bedroom = 0
    stats.stat_charm = 0
    stats.stat_loyalty = 0
    
    yield (
        stats,
        Color(0xff0099),
    )
    
    stats = Stats(202503120002)
    stats.stat_housewife = 0
    stats.stat_cuteness = 0
    stats.stat_bedroom = 10
    stats.stat_charm = 0
    stats.stat_loyalty = 0
    
    yield (
        stats,
        Color(0x3300ff),
    )
    
    stats = Stats(202503120003)
    stats.stat_housewife = 0
    stats.stat_cuteness = 0
    stats.stat_bedroom = 0
    stats.stat_charm = 10
    stats.stat_loyalty = 0
    
    yield (
        stats,
        Color(0x00ffff),
    )
    
    stats = Stats(202503120004)
    stats.stat_housewife = 0
    stats.stat_cuteness = 0
    stats.stat_bedroom = 0
    stats.stat_charm = 0
    stats.stat_loyalty = 10
    
    yield (
        stats,
        Color(0x33ff00),
    )
    
    stats = Stats(202503120005)
    stats.stat_housewife = 10
    stats.stat_cuteness = 10
    stats.stat_bedroom = 10
    stats.stat_charm = 10
    stats.stat_loyalty = 10
    
    yield (
        stats,
        Color(0x57948a),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_user_chart_color(stats):
    """
    Tests whether ``get_user_chart_color`` works as intended.
    
    Parameters
    ----------
    stats : ``Stats``
        The user's stats
    
    Returns
    -------
    output : ``Color``
    """
    output = get_user_chart_color(stats)
    vampytest.assert_instance(output, Color)
    return output
