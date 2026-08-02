import vampytest

from ..content_building import produce_duration


def _iter_options():
    yield (
        0,
        '0s',
    )
    
    yield (
        1,
        '1s'
    )
    
    yield (
        59,
        '59s'
    )
    
    yield (
        1 * 60 + 1,
        '1m 1s',
    )
    
    yield (
        59 * 60,
        '59m',
    )
    
    yield (
        1 * 3600 + 1 * 60,
        '1h 1m'
    )
    
    yield (
        23 * 3600,
        '23h',
    )
    
    yield (
        1 * 86400 + 1 * 3600,
        '1d 1h',
    )
    
    yield (
        6 * 86400,
        '6d',
    )
    
    yield (
        1 * 604800 + 1 * 86400,
        '1w 1d',
    )
    
    yield (
        4 * 604800,
        '4w',
    )
    
    yield (
        1 * 604800 + 1 * 86400 + 1 * 3600 + 1 * 60 + 1,
        '1w 1d 1h 1m 1s',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_duration(duration):
    """
    Tests whether ``produce_duration`` works as intended.

    Parameters
    ----------
    duration : `int`
        Duration to produce suggestion for.

    Returns
    -------
    output : `str`
    """
    output = [*produce_duration(duration)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
