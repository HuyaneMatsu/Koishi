import vampytest

from ..calculations import calculate_movement


def _iter_options():
    yield 0, 0, 0, 0, 0, 800
    yield 5, 5, 5, 5, 5, 1000
    yield 10, 10, 10, 10, 10, 1200


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__calculate_movement(stat_bedroom, stat_charm, stat_cuteness, stat_housewife, stat_loyalty):
    """
    Tests whether ``calculate_movement`` works as intended.
    
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
    output = calculate_movement(stat_bedroom, stat_charm, stat_cuteness, stat_housewife, stat_loyalty)
    vampytest.assert_instance(output, int)
    return output
