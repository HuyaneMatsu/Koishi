import vampytest

from ...item_core import ITEM_ID_FISHING_ROD
from ...user_stats_core import UserStats

from ..content_building import produce_user_stats_secondary_description


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
            'Health: 184\n'
            'Energy: 186\n'
            'Movement: 1.2 (m/s)\n'
            'Inventory: 46.982 (kg)\n'
            '\n'
            'Butchering: 19 (+28%)\n'
            'Fishing: 14 (+15%)\n'
            'Foraging: 18 (+26%)\n'
            'Gardening: 19 (+28%)\n'
            'Hunting: 17 (+23%)'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_user_stats_secondary_description(user_stats):
    """
    Tests whether ``produce_user_stats_secondary_description`` works as intended.
    
    Parameters
    ----------
    user_stats : ``UserStats``
        The user's stats
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_user_stats_secondary_description(user_stats)]
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
