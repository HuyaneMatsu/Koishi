import vampytest

from ..parsing import parse_duration


def _iter_options():
    yield (
        None,
        0,
    )
    
    yield (
        '',
        0,
    )
    
    yield (
        '56',
        56,
    )
    
    yield (
        '56s',
        56,
    )
    
    yield (
        '56S',
        56,
    )
    
    yield (
        '56 s',
        56,
    )
    
    yield (
        '56 S',
        56,
    )
    
    yield (
        '56m',
        56 * 60,
    )
    
    yield (
        '56M',
        56 * 60,
    )
    
    yield (
        '56 m',
        56 * 60,
    )
    
    yield (
        '56 M',
        56 * 60,
    )
    
    yield (
        '56h',
        56 * 3600,
    )
    
    yield (
        '56H',
        56 * 3600,
    )
    
    yield (
        '56 h',
        56 * 3600,
    )
    
    yield (
        '56 H',
        56 * 3600,
    )
    
    yield (
        '56d',
        56 * 86400,
    )
    
    yield (
        '56D',
        56 * 86400,
    )
    
    yield (
        '56 d',
        56 * 86400,
    )
    
    yield (
        '56 D',
        56 * 86400,
    )
    
    yield (
        '56w',
        56 * 604800,
    )
    
    yield (
        '56W',
        56 * 604800,
    )
    
    yield (
        '56 w',
        56 * 604800,
    )
    
    yield (
        '56 W',
        56 * 604800,
    )
    
    yield (
        '2w 3d 4h 5m 6s 7',
        2 * 604800 + 3 * 86400 + 4 * 3600 + 5 * 60 + 6 * 1 + 7 * 1,
    )
    
    yield (
        '7 6s 5m 4h 3d 2w',
        7 * 1 + 6 * 1 + 5 * 60 + 4 * 3600 + 3 * 86400 + 2 * 604800,
    )
    
    yield (
        'nyan',
        0,
    )
    
    yield (
        '    6     m   ',
        6 * 60,
    )
    
    yield (
        '5 mokou',
        5 * 60,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_duration(value):
    """
    Tests whether ``parse_duration`` works as intended.
    
    Parameters
    ----------
    value : `None | str`
        Duration value.
    
    Returns
    -------
    output : `int`
    """
    output = parse_duration(value)
    vampytest.assert_instance(output, int)
    return output
