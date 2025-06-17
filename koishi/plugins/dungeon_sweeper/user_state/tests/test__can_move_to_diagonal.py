import vampytest

from ...tile_bit_masks import (
    BIT_MASK_CHARACTER, BIT_MASK_BOX, BIT_MASK_FLOOR, BIT_MASK_HOLE, BIT_FLAG_NORTH, BIT_MASK_WALL
)

from ..game_state import (
    DIRECTION_MOVE_STATE_NONE, DIRECTION_MOVE_STATE_DIAGONAL_0, DIRECTION_MOVE_STATE_DIAGONAL_1, can_move_to_diagonal
)


def _iter_options():
    wall = BIT_MASK_WALL | BIT_FLAG_NORTH
    character = BIT_MASK_FLOOR | BIT_MASK_CHARACTER | BIT_FLAG_NORTH
    floor = BIT_MASK_FLOOR
    box = BIT_MASK_FLOOR | BIT_MASK_BOX
    hole = BIT_MASK_HOLE
    
    # ---- want but wall ---
    
    yield (
        'Want to go north -> east, but wall',
        [
            wall, wall, wall, wall,
            wall, character, floor, wall,
            wall, floor, floor, wall,
            wall, wall, wall, wall,
        ],
        5,
        -4,
        +1,
        DIRECTION_MOVE_STATE_NONE,
    )
    
    # ---- want and can ----
    
    yield (
        'Want to go north -> east, and can',
        [
            wall, wall, wall, wall,
            wall, floor, floor, wall,
            wall, character, wall, wall,
            wall, wall, wall, wall,
        ],
        9,
        -4,
        +1,
        DIRECTION_MOVE_STATE_DIAGONAL_0,
    )
    
    yield (
        'Want to go north -> east, and can (east -> north)',
        [
            wall, wall, wall, wall,
            wall, wall, floor, wall,
            wall, character, floor, wall,
            wall, wall, wall, wall,
        ],
        9,
        -4,
        +1,
        DIRECTION_MOVE_STATE_DIAGONAL_1,
    )
    
    # ---- can choose both push and non push ----
    
    yield (
        'Want to go north -> east, avoid pushing, and can',
        [
            wall, wall, wall, wall, wall,
            wall, floor, floor, floor, wall,
            wall, floor, floor, floor, wall,
            wall, character, box, floor, wall,
            wall, wall, wall, wall, wall,
        ],
        16,
        -5,
        +1,
        DIRECTION_MOVE_STATE_DIAGONAL_0,
    )
    
    yield (
        'Want to go north -> east, avoid pushing, and can (east -> north)',
        [
            wall, wall, wall, wall, wall,
            wall, floor, floor, floor, wall,
            wall, box, floor, floor, wall,
            wall, character, floor, floor, wall,
            wall, wall, wall, wall, wall,
        ],
        16,
        -5,
        +1,
        DIRECTION_MOVE_STATE_DIAGONAL_1,
    )
    
    # ---- only push ----
    
    yield (
        'Want to go north -> east, both is push, and can',
        [
            wall, wall, wall, wall, wall,
            wall, floor, floor, floor, wall,
            wall, box, box, floor, wall,
            wall, character, wall, floor, wall,
            wall, wall, wall, wall, wall,
        ],
        16,
        -5,
        +1,
        DIRECTION_MOVE_STATE_DIAGONAL_0,
    )
    yield (
        'Want to go north -> east, both is push, and  (east -> north)',
        [
            wall, wall, wall, wall, wall,
            wall, floor, floor, floor, wall,
            wall, wall, box, floor, wall,
            wall, character, box, floor, wall,
            wall, wall, wall, wall, wall,
        ],
        16,
        -5,
        +1,
        DIRECTION_MOVE_STATE_DIAGONAL_1,
    )


@vampytest._(vampytest.call_from(_iter_options()).named_first().returning_last())
def test__can_move_to_diagonal(map_, position, step_0, step_1):
    """
    Tests whether ``can_move_to_diagonal`` works as intended.
    
    Parameters
    ----------
    map_ : `list<int>`
        The map where the player is.
    
    position : `int`
        The player's position on the map.
    
    step_0 : `int`
        The step to do.
    
    step_1 : `int`
        The step to do.
    
    Returns
    -------
    output : `int`
    """
    output = can_move_to_diagonal(map_, position, step_0, step_1)
    vampytest.assert_instance(output, int)
    return output
