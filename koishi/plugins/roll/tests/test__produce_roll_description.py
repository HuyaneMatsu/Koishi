import vampytest

from ..content_building import produce_roll_description


def _iter_options():
    yield (
        2,
        6,
        0,
        0,
        [2, 4],
        6,
        (
            'Rolling 2d6\n'
            'Rolls: 2, 4\n'
            'Result: **6**'
        ),
    )
    
    yield (
        2,
        6,
        2,
        0,
        [2, 4],
        8,
        (
            'Rolling 2d6+2\n'
            'Rolls: 2, 4\n'
            'Result: **8**'
        ),
    )
    
    yield (
        2,
        6,
        -2,
        0,
        [2, 4],
        4,
        (
            'Rolling 2d6-2\n'
            'Rolls: 2, 4\n'
            'Result: **4**'
        ),
    )
    
    yield (
        2,
        6,
        0,
        40,
        [2, 4],
        6,
        (
            'Rolling 2d6 with 40 luck\n'
            'Rolls: 2, 4\n'
            'Result: **6**'
        ),
    )
    
    yield (
        2,
        6,
        0,
        -40,
        [2, 4],
        6,
        (
            'Rolling 2d6 with -40 luck\n'
            'Rolls: 2, 4\n'
            'Result: **6**'
        ),
    )
    
    yield (
        1,
        6,
        0,
        0,
        [4],
        4,
        (
            'Rolling 1d6\n'
            'Result: **4**'
        ),
    )
    
    yield (
        0,
        0,
        0,
        0,
        [],
        0,
        (
            'Result: **0**'
        ),
    )
    
    yield (
        0,
        0,
        +8,
        0,
        [],
        8,
        (
            'Rolling +8\n'
            'Result: **8**'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_roll_description(dice_count, dice_sides, fix_amount, luck, rolls, result):
    """
    Tests whether ``produce_roll_description`` works as intended.
    
    Parameters
    ----------
    dice_count : `int`
        Amount of dices to roll.
    
    dice_sides : `int`
        How much sides each side have.
    
    fix_amount : `int`
        Added or subtracted amount.
    
    luck : `int`
        How lucky the user is.
    
    rolls : `list<int>`
        Rolls.
    
    result : `int`
        The sum of all rolls and the fix amount.
    
    Returns
    --------
    output : `str`
    """
    parts = [*produce_roll_description(dice_count, dice_sides, fix_amount, luck, rolls, result)]
    
    for part in parts:
        vampytest.assert_instance(part, str)
    
    return ''.join(parts)
