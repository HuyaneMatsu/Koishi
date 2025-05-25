import vampytest

from ..user_stats import UserStats
from ..utils import set_user_stat_value_for_index


def _iter_options():
    yield (
        202503150030,
        (lambda stat : stat.stat_housewife),
        -1,
        56,
        56,
    )
    
    yield (
        202503150031,
        (lambda stat : stat.stat_housewife),
        0,
        56,
        56,
    )
    
    yield (
        202503150032,
        (lambda stat : stat.stat_cuteness),
        1,
        56,
        56,
    )
    
    yield (
        202503150033,
        (lambda stat : stat.stat_bedroom),
        2,
        56,
        56,
    )
    
    yield (
        202503150034,
        (lambda stat : stat.stat_charm),
        3,
        56,
        56,
    )
    
    yield (
        202503150035,
        (lambda stat : stat.stat_loyalty),
        4,
        56,
        56,
    )
    
    yield (
        202503150036,
        (lambda stat : stat.stat_housewife),
        5,
        56,
        56,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__set_user_stat_value_for_index(user_id, getter_function, stat_index, value):
    """
    Tests whether ``set_user_stat_value_for_index`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        User identifier to create function for.
    
    getter_function : `FunctionType`
        Function to get the set stat with.
    
    stat_index : `int`
        The stat's index.
    
    value : `int`
        The value to set.
    
    Returns
    -------
    output : `str`
    """
    stats = UserStats(user_id)
    
    set_user_stat_value_for_index(stats, stat_index, value)
    
    output = getter_function(stats)
    vampytest.assert_instance(output, int)
    return output
