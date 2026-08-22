import vampytest

from ..helpers import parse_dice_string


def _iter_options():
    yield (
        None,
        (1, 6, 0),
    )
    
    yield (
        'shrimp',
        None,
    )
    
    yield (
        '30',
        (30, 6, 0),
    )
    
    yield (
        '+8',
        (0, 0, 8),
    )
    
    yield (
        '-8',
        (0, 0, -8),
    )
    
    yield (
        '1d',
        (1, 6, 0),
    )
    
    yield (
        'd7',
        (1, 7, 0),
    )
    
    yield (
        'd7',
        (1, 7, 0),
    )
    
    yield (
        '2d7',
        (2, 7, 0),
    )
    
    yield (
        '2d7+8',
        (2, 7, 8),
    )
    
    yield (
        '2d7-8',
        (2, 7, -8),
    )
    
    yield (
        'd',
        (1, 6, 0),
    )
    
    yield (
        'd+8',
        (1, 6, 8),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_dice_string(dice_string):
    """
    Tests whether ``parse_dice_string`` works as intended.
    
    Parameters
    ----------
    dice_string : `None | str`
        Dice string to parse.
    
    Returns
    -------
    output : `None | (int, int, int)`
    """
    output = parse_dice_string(dice_string)
    vampytest.assert_instance(output, tuple, nullable = True)
    return output
