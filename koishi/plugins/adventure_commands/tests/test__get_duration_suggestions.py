import vampytest

from ..duration_suggesting import get_duration_suggestions


def _iter_options():
    hour = 3600
    
    yield (
        (
            hour * 4,
            hour * 6,
            hour * 8,
            hour * 12,
            hour * 16,
        ),
        None,
        [
            ('4h', format(hour * 4, 'x')),
            ('6h', format(hour * 6, 'x')),
            ('8h', format(hour * 8, 'x')),
            ('12h', format(hour * 12, 'x')),
            ('16h', format(hour * 16, 'x')),
        ],
    )
    
    yield (
        (
            hour * 4,
            hour * 6,
            hour * 8,
            hour * 12,
            hour * 16,
        ),
        '1h',
        [
            ('12h', format(hour * 12, 'x')),
            ('16h', format(hour * 16, 'x')),
        ],
    )
    
    yield (
        (
            hour * 4,
            hour * 6,
            hour * 8,
            hour * 12,
            hour * 16,
        ),
        '20h',
        [],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_duration_suggestions(durations, value):
    """
    Gets the duration suggestions.
    
    Parameters
    ----------
    durations : `tuple<int>`
        Durations to get suggestions for.
    
    value : `None | str`
        Value to match for.
    
    Returns
    -------
    output : `list<(str, str)>`
    """
    output = get_duration_suggestions(durations, value)
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, tuple)
        vampytest.assert_eq(len(element), 2)
        vampytest.assert_instance(element[0], str)
        vampytest.assert_instance(element[1], str)
    
    return output
