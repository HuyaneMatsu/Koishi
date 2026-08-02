import vampytest

from ..content_building import produce_duration_sophisticated


def _iter_options():
    yield (
        0,
        '0 second',
    )
    
    yield (
        1,
        '1 second'
    )
    
    yield (
        59,
        '59 seconds'
    )
    
    yield (
        1 * 60 + 1,
        '1 minute, 1 second',
    )
    
    yield (
        59 * 60,
        '59 minutes',
    )
    
    yield (
        1 * 3600 + 1 * 60,
        '1 hour, 1 minute'
    )
    
    yield (
        23 * 3600,
        '23 hours',
    )
    
    yield (
        1 * 86400 + 1 * 3600,
        '1 day, 1 hour',
    )
    
    yield (
        6 * 86400,
        '6 days',
    )
    
    yield (
        1 * 604800 + 1 * 86400,
        '1 week, 1 day',
    )
    
    yield (
        4 * 604800,
        '4 weeks',
    )
    
    yield (
        1 * 604800 + 1 * 86400 + 1 * 3600 + 1 * 60 + 1,
        '1 week, 1 day, 1 hour, 1 minute, 1 second',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_duration_sophisticated(duration):
    """
    Tests whether ``produce_duration_sophisticated`` works as intended.

    Parameters
    ----------
    duration : `int`
        Duration to produce suggestion for.

    Returns
    -------
    output : `str`
    """
    output = [*produce_duration_sophisticated(duration)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
