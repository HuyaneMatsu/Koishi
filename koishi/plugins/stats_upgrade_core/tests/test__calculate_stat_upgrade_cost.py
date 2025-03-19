import vampytest

from ..utils import calculate_stat_upgrade_cost


def _iter_options():
    yield 25, 1, 451
    yield 25, 2, 855
    yield 24, 2, 815


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__calculate_stat_upgrade_cost(total_points, next_point):
    """
    Tests whether ``calculate_stat_upgrade_cost`` works as intended.
    
    Parameters
    ----------
    total_points : `int`
        The user's total stat points.
    
    next_point
        The next point in the specific stat.
    
    Returns
    -------
    output : `int`
    """
    output = calculate_stat_upgrade_cost(total_points, next_point)
    vampytest.assert_instance(output, int)
    return output   
