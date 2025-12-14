import vampytest

from ..helpers import get_upgrade_cost_cumulative


def _iter_options():
    yield (
        5,
        5,
        1,
        9,
        5,
        0,
        0,
        1,
        0,
        0,
        855,
    )
    
    yield (
        5,
        5,
        1,
        9,
        5,
        0,
        0,
        2,
        0,
        0,
        855 + 1346,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_upgrade_cost_cumulative(
    stat_housewife,
    stat_cuteness,
    stat_bedroom,
    stat_charm,
    stat_loyalty,
    modify_housewife_by,
    modify_cuteness_by,
    modify_bedroom_by,
    modify_charm_by,
    modify_loyalty_by,
):
    """
    Tests whether ``get_upgrade_cost_cumulative`` works as intended.
    
    Parameters
    ----------
    stat_housewife : `int`
        The user's current housewife stat.
    
    stat_cuteness : `int`
        The user's current cuteness stat.
    
    stat_bedroom : `int`
        The user's current bedroom stat.
    
    stat_charm : `int`
        The user's current charm stat.
    
    stat_loyalty : `int`
        The user's current loyalty stat.
    
    modify_housewife_by : `int`
        The amount to modify the housewife stat by.
    
    modify_cuteness_by : `int`
        The amount to modify the cuteness stat by.
    
    modify_bedroom_by : `int`
        The amount to modify the bedroom stat by.
    
    modify_charm_by : `int`
        The amount to modify the charm stat by.
    
    modify_loyalty_by : `int`
        The amount to modify the loyalty stat by.
    
    Returns
    -------
    output : `int`
    """
    output = get_upgrade_cost_cumulative(
        stat_housewife,
        stat_cuteness,
        stat_bedroom,
        stat_charm,
        stat_loyalty,
        modify_housewife_by,
        modify_cuteness_by,
        modify_bedroom_by,
        modify_charm_by,
        modify_loyalty_by,
    )
    vampytest.assert_instance(output, int)
    return output
