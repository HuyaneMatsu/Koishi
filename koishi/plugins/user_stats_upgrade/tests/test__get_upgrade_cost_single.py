import vampytest

from ..helpers import get_upgrade_cost_single


def _iter_options():
    yield 25, 1, 451
    yield 25, 2, 855
    yield 24, 2, 815


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_upgrade_cost_single(cumulative_stats, stat_incremented):
    """
    Tests whether ``get_upgrade_cost_single`` works as intended.
    
    Parameters
    ----------
    cumulative_stats : `int`
        The user's total stat points.
    
    stat_incremented : `int`
        The next point in the specific stat.
    
    Returns
    -------
    output : `int`
    """
    output = get_upgrade_cost_single(cumulative_stats, stat_incremented)
    vampytest.assert_instance(output, int)
    return output   
