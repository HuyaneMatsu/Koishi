import vampytest

from ...user_stats_core import UserStats

from ..embed_builders import get_stats_description


def _iter_options():
    stats = UserStats(202503120010)
    stats.stat_housewife = 5
    stats.stat_cuteness = 6
    stats.stat_bedroom = 7
    stats.stat_charm = 8
    stats.stat_loyalty = 9
    
    yield (
        stats,
        (
            '```\n'
            '+------------------------+--------+\n'
            '| Stat                   | Amount |\n'
            '+========================+========+\n'
            '| Housewife capabilities | 5      |\n'
            '+------------------------+--------+\n'
            '| Cuteness               | 6      |\n'
            '+------------------------+--------+\n'
            '| Bedroom skills         | 7      |\n'
            '+------------------------+--------+\n'
            '| Charm                  | 8      |\n'
            '+------------------------+--------+\n'
            '| Loyalty                | 9      |\n'
            '+------------------------+--------+\n'
            '```'
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_stats_description(stats):
    """
    Tests whether ``get_stats_description`` works as intended.
    
    Parameters
    ----------
    stats : ``UserStats``
        The user's stats
    
    Returns
    -------
    output : `str`
    """
    output = get_stats_description(stats)
    vampytest.assert_instance(output, str)
    return output
