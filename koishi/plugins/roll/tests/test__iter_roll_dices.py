import vampytest

from ..helpers import iter_roll_dices

ADJUST = 0.00001


def _iter_options():
    yield (
        1,
        6,
        0,
        [
            1.0 / 6.0 + ADJUST,
        ],
        [
            2,
        ],
    )
    
    yield (
        2,
        6,
        0,
        [
            0.0 / 6.0 + ADJUST,
            5.0 / 6.0 + ADJUST,
        ],
        [
            1,
            6,
        ],
    )
    
    yield (
        2,
        6,
        100,
        [
            0.0 / 6.0 + ADJUST,
            5.0 / 6.0 + ADJUST,
            3.0 / 6.0 + ADJUST,
            2.0 / 6.0 + ADJUST,
        ],
        [
            6,
            4,
        ],
    )
    
    yield (
        2,
        6,
        -100,
        [
            0.0 / 6.0 + ADJUST,
            5.0 / 6.0 + ADJUST,
            3.0 / 6.0 + ADJUST,
            2.0 / 6.0 + ADJUST,
        ],
        [
            1,
            3,
        ],
    )
    
    yield (
        2,
        6,
        200,
        [
            0.0 / 6.0 + ADJUST,
            5.0 / 6.0 + ADJUST,
            3.0 / 6.0 + ADJUST,
            2.0 / 6.0 + ADJUST,
            4.0 / 6.0 + ADJUST,
            1.0 / 6.0 + ADJUST,
        ],
        [
            6,
            5,
        ],
    )
    
    yield (
        2,
        6,
        -200,
        [
            0.0 / 6.0 + ADJUST,
            5.0 / 6.0 + ADJUST,
            3.0 / 6.0 + ADJUST,
            2.0 / 6.0 + ADJUST,
            4.0 / 6.0 + ADJUST,
            1.0 / 6.0 + ADJUST,
        ],
        [
            1,
            2,
        ],
    )
    
    yield (
        2,
        6,
        20,
        [
            0.0 / 6.0 + ADJUST,
            10.0 / 100.0,
            3.0 / 6.0 + ADJUST,
            2.0 / 6.0 + ADJUST,
            30.0 / 100.0,
        ],
        [
            4,
            3,
        ],
    )
    
    yield (
        2,
        6,
        120,
        [
            0.0 / 6.0 + ADJUST,
            3.0 / 6.0 + ADJUST,
            10.0 / 100.0,
            5.0 / 6.0 + ADJUST,
            2.0 / 6.0 + ADJUST,
            1.0 / 6.0 + ADJUST,
            30.0 / 100.0,
        ],
        [
            6,
            3,
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__iter_roll_dices(dice_count, dice_sides, luck, randoms):
    """
    Tests whether ``iter_roll_dices`` works as intended.
    
    Parameters
    ----------
    dice_count : `int`
        Amount of dices to roll.
    
    dice_sides : `int`
        How much sides each side have.
    
    luck : `int`
        How lucky the user is.
    
    Returns
    -------
    output : `list<int>`
    """
    index = 0
    
    def random():
        nonlocal index
        nonlocal randoms
        
        try:
            value = randoms[index]
        except IndexError as exception:
            raise RuntimeError() from exception
        
        index += 1
        return value
    
    mocked = vampytest.mock_globals(
        iter_roll_dices,
        random = random,
    )
    
    output = [*mocked(dice_count, dice_sides, luck)]
    
    for element in output:
        vampytest.assert_instance(element, int)
    
    return output
