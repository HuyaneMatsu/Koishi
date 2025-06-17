import vampytest

from ...tile_bit_masks import (
    BIT_MASK_CHARACTER, BIT_MASK_BOX, BIT_MASK_FLOOR, BIT_MASK_HOLE, BIT_FLAG_NORTH, BIT_MASK_WALL
)

from ..game_state import DIRECTION_MOVE_STATE_CAN, DIRECTION_MOVE_STATE_NONE, DIRECTION_MOVE_STATE_PUSH, can_move_to


def _iter_options():
    wall = BIT_MASK_WALL | BIT_FLAG_NORTH
    character = BIT_MASK_FLOOR | BIT_MASK_CHARACTER | BIT_FLAG_NORTH
    floor = BIT_MASK_FLOOR
    box = BIT_MASK_FLOOR | BIT_MASK_BOX
    hole = BIT_MASK_HOLE
    
    # ---- want but wall ---
    
    yield (
        'Want to go north, but wall',
        [
            wall, wall, wall,
            wall, character, wall,
            wall, floor, wall,
            wall, wall, wall,
        ],
        4,
        -3,
        DIRECTION_MOVE_STATE_NONE,
    )
    
    # ---- want and can ----
    
    yield (
        'Want to go north, and can',
        [
            wall, wall, wall,
            wall, floor, wall,
            wall, character, wall,
            wall, wall, wall,
        ],
        7,
        -3,
        DIRECTION_MOVE_STATE_CAN,
    )
    
    # ---- box want but wall after ---
    
    yield (
        'Want to push box north, but wall after',
        [
            wall, wall, wall,
            wall, box, wall,
            wall, character, wall,
            wall, floor, wall,
            wall, wall, wall,
        ],
        7,
        -3,
        DIRECTION_MOVE_STATE_NONE,
    )
    
    # ---- box want and floor after ---
    
    yield (
        'Want to push box north, and floor after',
        [
            wall, wall, wall,
            wall, floor, wall,
            wall, box, wall,
            wall, character, wall,
            wall, wall, wall,
        ],
        10,
        -3,
        DIRECTION_MOVE_STATE_PUSH,
    )
    
    # ---- box want and hole after ---
    
    yield (
        'Want to push box north, and hole after',
        [
            wall, wall, wall,
            wall, hole, wall,
            wall, box, wall,
            wall, character, wall,
            wall, wall, wall,
        ],
        10,
        -3,
        DIRECTION_MOVE_STATE_PUSH,
    )


@vampytest._(vampytest.call_from(_iter_options()).named_first().returning_last())
def test__can_move_to(map_, position, step):
    """
    Tests whether ``can_move_to`` works as intended.
    
    Parameters
    ----------
    map_ : `list<int>`
        The map where the player is.
    
    position : `int`
        The player's position on the map.
    
    step : `int`
        The step to do.
    
    Returns
    -------
    output : `int`
    """
    output = can_move_to(map_, position, step)
    vampytest.assert_instance(output, int)
    return output
