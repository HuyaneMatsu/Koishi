import vampytest

from ...chapters import CHAPTER_DEFAULT, Stage
from ...move_directions import (
    MOVE_DIRECTION_SOUTH, MOVE_DIRECTION_SOUTH_TO_EAST, MOVE_DIRECTION_WEST, MOVE_DIRECTION_WEST_TO_SOUTH,
    MOVE_DIRECTION_WEST_TO_NORTH, MoveDirections
)
from ...tile_bit_masks import (
    BIT_FLAG_NORTH, BIT_MASK_BOX, BIT_MASK_CHARACTER, BIT_MASK_FLOOR, BIT_MASK_HOLE, BIT_MASK_TARGET_ON_FLOOR,
    BIT_MASK_WALL
)
from ..game_state import GameState, get_move_directions


def _iter_options():
    wall = BIT_MASK_WALL | BIT_FLAG_NORTH
    character = BIT_MASK_FLOOR | BIT_MASK_CHARACTER | BIT_FLAG_NORTH
    target = BIT_MASK_TARGET_ON_FLOOR
    floor = BIT_MASK_FLOOR
    box = BIT_MASK_FLOOR | BIT_MASK_BOX
    hole = BIT_MASK_HOLE
    
    stage = Stage(
        CHAPTER_DEFAULT.id,
        999,
        
        0,
        0,
        0,
        0,
        
        5,
        [
            wall    , wall  , wall  , wall      , wall  , wall  , wall  ,
            wall    , floor , floor , floor     , box   , target, wall  ,
            wall    , floor , floor , wall      , wall  , wall  , wall  ,
            wall    , floor , floor , character , box   , box   , wall  ,
            wall    , floor , floor , box       , floor , floor , wall  ,
            wall    , floor , floor , hole      , floor , floor , wall  ,
            wall    , wall  ,  wall , wall      , wall  , wall  , wall  ,
        ],
        7,
        24,
        1,
    )
    
    move_directions = MoveDirections()
    move_directions.set(MOVE_DIRECTION_SOUTH, True)
    move_directions.set(MOVE_DIRECTION_WEST, True)
    
    move_directions.set(MOVE_DIRECTION_SOUTH_TO_EAST, True)
    move_directions.set(MOVE_DIRECTION_WEST_TO_SOUTH, True)
    move_directions.set(MOVE_DIRECTION_WEST_TO_NORTH, True)
    
    yield (
        'north blocked with wall, east blocked with box, south is box push, west is passable',
        stage,
        move_directions,
    )


@vampytest._(vampytest.call_from(_iter_options()).named_first().returning_last())
def test__get_move_directions(stage):
    """
    Tests whether ``get_move_directions`` works as intended.
    
    Parameters
    ----------
    stage : ``Stage``
        Stage to create game state with.
    
    Returns
    -------
    output : ``MoveDirections``
    """
    game_state = GameState(stage, -1)
    output = get_move_directions(game_state)
    vampytest.assert_instance(output, MoveDirections)
    return output
