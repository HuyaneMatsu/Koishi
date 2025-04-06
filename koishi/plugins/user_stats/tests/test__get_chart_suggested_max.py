import vampytest

from ..embed_builders import get_chart_suggested_max


def _iter_options():
    # min 10
    yield (
        1,
        1,
        1,
        1,
        1,
        10,
    )
    
    # min the max stat
    yield (
        1,
        1,
        1,
        1,
        11,
        11,
    )
    
    # increase by 1.34 if balanced
    yield (
        10,
        10,
        10,
        10,
        10,
        13,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_chart_suggested_max(stat_housewife, stat_cuteness, stat_bedroom, stat_charm, stat_loyalty):
    """
    Tests whether ``get_chart_suggested_max`` works as intended.
    
    Parameters
    ----------
    stat_housewife : `int`
        The user's housewife stat.
    
    stat_cuteness : `int`
        The user's cuteness stat.
    
    stat_bedroom : `int`
        The user's bedroom stat.
    
    stat_charm : `int`
        The user's charm stat.
    
    stat_loyalty : `int`
        The user's loyalty stat.
    
    Returns
    -------
    output : `int`
    """
    output = get_chart_suggested_max(stat_housewife, stat_cuteness, stat_bedroom, stat_charm, stat_loyalty)
    vampytest.assert_instance(output, int)
    return output
