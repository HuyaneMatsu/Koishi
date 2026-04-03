import vampytest

from ..calculations import calculate_health


def _iter_options():
    yield 0, 0, 0, 0, 0, 100
    yield 5, 5, 5, 5, 5, 150
    yield 10, 10, 10, 10, 10, 200


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__calculate_health(stat_bedroom, stat_charm, stat_cuteness, stat_housewife, stat_loyalty):
    """
    Tests whether ``calculate_health`` works as intended.
    
    Parameters
    ----------
    stat_bedroom : `int`
        The user's bedroom skills.
    
    stat_charm : `int`
        The user's charm.
    
    stat_cuteness : `int`
        The user's cuteness.
    
    stat_housewife : `int`
        The user's housewife capabilities.
    
    stat_loyalty : `int`
        The user's loyalty.
    
    Returns
    -------
    output : `int`
    """
    output = calculate_health(stat_bedroom, stat_charm, stat_cuteness, stat_housewife, stat_loyalty)
    vampytest.assert_instance(output, int)
    return output
