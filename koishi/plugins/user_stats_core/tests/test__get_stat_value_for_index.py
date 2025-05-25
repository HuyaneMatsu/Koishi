import vampytest

from ..user_stats import UserStats
from ..utils import get_user_stat_value_for_index


def _iter_options():
    yield (
        202503150020,
        (lambda stats : UserStats.stat_housewife.__set__(stats, 56)),
        -1,
        56,
    )
    
    yield (
        202503150021,
        (lambda stats : UserStats.stat_housewife.__set__(stats, 56)),
        0,
        56,
    )
    
    yield (
        202503150022,
        (lambda stats : UserStats.stat_cuteness.__set__(stats, 56)),
        1,
        56,
    )
    
    yield (
        202503150023,
        (lambda stats : UserStats.stat_bedroom.__set__(stats, 56)),
        2,
        56,
    )
    
    yield (
        202503150024,
        (lambda stats : UserStats.stat_charm.__set__(stats, 56)),
        3,
        56,
    )
    
    yield (
        202503150025,
        (lambda stats : UserStats.stat_loyalty.__set__(stats, 56)),
        4,
        56,
    )
    
    yield (
        202503150026,
        (lambda stats : UserStats.stat_housewife.__set__(stats, 56)),
        5,
        56,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_user_stat_value_for_index(user_id, prepare_function, stat_index):
    """
    Tests whether ``get_user_stat_value_for_index`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        User identifier to create function for.
    
    prepare_function : `FunctionType`
        Function to prepare the stats with.
    
    stat_index : `int`
        The stat's index.
    
    Returns
    -------
    output : `str`
    """
    stats = UserStats(user_id)
    prepare_function(stats)
    
    output = get_user_stat_value_for_index(stats, stat_index)
    vampytest.assert_instance(output, int)
    return output
