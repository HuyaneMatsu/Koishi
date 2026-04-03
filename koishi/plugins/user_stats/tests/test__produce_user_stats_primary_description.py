import vampytest

from ...item_core import ITEM_ID_FISHING_ROD
from ...user_stats_core import UserStats

from ..content_building import produce_user_stats_primary_description


def _iter_options():
    user_id = 202512270002
    user_stats = UserStats(
        user_id,
    )
    user_stats.stat_housewife = 10
    user_stats.stat_cuteness = 9
    user_stats.stat_bedroom = 8
    user_stats.stat_charm = 7
    user_stats.stat_loyalty = 6
    user_stats.item_id_weapon = ITEM_ID_FISHING_ROD
    
    yield (
        user_stats,
        (
            'Housewife-capabilities: 11 (10 + 1)\n'
            'Cuteness: 9\n'
            'Bedroom-skills: 9 (8 + 1)\n'
            'Charm: 7\n'
            'Loyalty: 7 (6 + 1)'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_user_stats_primary_description(user_stats):
    """
    Tests whether ``produce_user_stats_primary_description`` works as intended.
    
    Parameters
    ----------
    user_stats : ``UserStats``
        The user's stats
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_user_stats_primary_description(user_stats)]
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
