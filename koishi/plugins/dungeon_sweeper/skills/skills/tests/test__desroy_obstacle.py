import vampytest


from ....chapters import CHAPTER_DEFAULT, Stage
from ....move_directions import (
    MOVE_DIRECTION_EAST, MOVE_DIRECTION_NORTH, MOVE_DIRECTION_SOUTH, MOVE_DIRECTION_WEST, MoveDirections
)
from ....tile_bit_masks import (
    BIT_FLAG_EAST, BIT_FLAG_NORTH, BIT_FLAG_SOUTH, BIT_FLAG_WEST, BIT_MASK_BOX, BIT_MASK_CHARACTER, BIT_MASK_FLOOR,
    BIT_MASK_OBSTACLE, BIT_MASK_OBSTACLE_DESTROYED, BIT_MASK_WALL
)
from ....user_state import HistoryElement, GameState

from ..destroy_obstacle import SKILL_DESTROY_OBSTACLE


def _build_default_stage():
    """
    Builds a default stage to use for testing.
    
    Returns
    -------
    stage : ``Stage``
    """
    wall = BIT_MASK_WALL | BIT_FLAG_NORTH
    character = BIT_MASK_FLOOR | BIT_MASK_CHARACTER | BIT_FLAG_NORTH
    floor = BIT_MASK_FLOOR
    
    return Stage(
        CHAPTER_DEFAULT.id,
        999,
        
        0,
        0,
        0,
        0,
        
        5,
        [
            wall    , wall  , wall      , wall  , wall  ,
            wall    , floor , floor     , floor , wall  ,
            wall    , floor , character , floor , wall  ,
            wall    , floor , floor     , floor , wall  ,
            wall    , wall  , wall      , wall  , wall  ,
        ],
        5,
        12,
        1,
    )


def _iter_options__can_activate():
    stage = _build_default_stage()
    
    yield (
        'cannot',
        stage,
        False,
    )
    
    stage = _build_default_stage()
    stage.map[7] = BIT_MASK_OBSTACLE
    
    yield (
        'north',
        stage,
        True,
    )
    
    stage = _build_default_stage()
    stage.map[13] = BIT_MASK_OBSTACLE
    
    yield (
        'east',
        stage,
        True,
    )
    
    stage = _build_default_stage()
    stage.map[17] = BIT_MASK_OBSTACLE
    
    yield (
        'south',
        stage,
        True,
    )
    
    stage = _build_default_stage()
    stage.map[11] = BIT_MASK_OBSTACLE
    
    yield (
        'west',
        stage,
        True,
    )
    
    stage = _build_default_stage()
    stage.map[7] = BIT_MASK_FLOOR | BIT_MASK_BOX
    
    yield (
        'cannot, test with box',
        stage,
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__can_activate()).named_first().returning_last())
def test__SKILL_DESTROY_OBSTACLE__can_activate(stage):
    """
    Tests whether ``SKILL_DESTROY_OBSTACLE.can_activate`` works as intended.
    
    Parameters
    ----------
    stage : ``Stage``
        Stage to create game state with.
    
    Returns
    -------
    output : `bool`
    """
    game_state = GameState(stage, -1)
    output = SKILL_DESTROY_OBSTACLE.can_activate(game_state)
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__get_directions():
    stage = _build_default_stage()
    directions = MoveDirections()
    
    yield (
        'cannot',
        stage,
        directions,
    )
    
    stage = _build_default_stage()
    stage.map[7] = BIT_MASK_OBSTACLE
    directions = MoveDirections()
    directions.set(MOVE_DIRECTION_NORTH, True)
    
    yield (
        'north',
        stage,
        directions,
    )
    
    stage = _build_default_stage()
    stage.map[13] = BIT_MASK_OBSTACLE
    directions = MoveDirections()
    directions.set(MOVE_DIRECTION_EAST, True)
    
    yield (
        'east',
        stage,
        directions,
    )
    
    stage = _build_default_stage()
    stage.map[17] = BIT_MASK_OBSTACLE
    directions = MoveDirections()
    directions.set(MOVE_DIRECTION_SOUTH, True)
    
    yield (
        'south',
        stage,
        directions,
    )
    
    stage = _build_default_stage()
    stage.map[11] = BIT_MASK_OBSTACLE
    directions = MoveDirections()
    directions.set(MOVE_DIRECTION_WEST, True)
    
    yield (
        'west',
        stage,
        directions,
    )
    
    stage = _build_default_stage()
    stage.map[7] = BIT_MASK_FLOOR | BIT_MASK_BOX
    directions = MoveDirections()
    
    yield (
        'cannot, test with box',
        stage,
        directions,
    )


@vampytest._(vampytest.call_from(_iter_options__get_directions()).named_first().returning_last())
def test__SKILL_DESTROY_OBSTACLE__get_directions(stage):
    """
    Tests whether ``SKILL_DESTROY_OBSTACLE.get_directions`` works as intended.
    
    Parameters
    ----------
    stage : ``Stage``
        Stage to create game state with.
    
    Returns
    -------
    output : ``MoveDirections``
    """
    game_state = GameState(stage, -1)
    output = SKILL_DESTROY_OBSTACLE.get_directions(game_state)
    vampytest.assert_instance(output, MoveDirections)
    return output


def _iter_options__use():
    stage = _build_default_stage()
    
    yield (
        'cannot',
        stage,
        -5,
        BIT_FLAG_NORTH,
        (
            False,
            stage.map.copy(),
            stage.start_position,
            True,
            [],
        ),
    )
    
    stage = _build_default_stage()
    stage.map[7] = BIT_MASK_OBSTACLE
    
    map_ = stage.map.copy()
    map_[7] = BIT_MASK_OBSTACLE_DESTROYED
    map_[12] = BIT_MASK_FLOOR | BIT_MASK_CHARACTER | BIT_FLAG_NORTH
    history = [
        HistoryElement(
            12,
            True,
            (
                (12, stage.map[12]),
                (7, stage.map[7]),
            ),
        ),
    ]
    
    yield (
        'north',
        stage,
        -5,
        BIT_FLAG_NORTH,
        (
            True,
            map_,
            stage.start_position,
            False,
            history,
        ),
    )
    
    stage = _build_default_stage()
    stage.map[13] = BIT_MASK_OBSTACLE
    
    map_ = stage.map.copy()
    map_[13] = BIT_MASK_OBSTACLE_DESTROYED
    map_[12] = BIT_MASK_FLOOR | BIT_MASK_CHARACTER | BIT_FLAG_EAST
    history = [
        HistoryElement(
            12,
            True,
            (
                (12, stage.map[12]),
                (13, stage.map[13]),
            ),
        ),
    ]
    
    yield (
        'east',
        stage,
        +1,
        BIT_FLAG_EAST,
        (
            True,
            map_,
            stage.start_position,
            False,
            history,
        ),
    )
    
    stage = _build_default_stage()
    stage.map[17] = BIT_MASK_OBSTACLE
    
    map_ = stage.map.copy()
    map_[17] = BIT_MASK_OBSTACLE_DESTROYED
    map_[12] = BIT_MASK_FLOOR | BIT_MASK_CHARACTER | BIT_FLAG_SOUTH
    history = [
        HistoryElement(
            12,
            True,
            (
                (12, stage.map[12]),
                (17, stage.map[17]),
            ),
        ),
    ]
    
    yield (
        'south',
        stage,
        +5,
        BIT_FLAG_SOUTH,
        (
            True,
            map_,
            stage.start_position,
            False,
            history,
        ),
    )
    
    stage = _build_default_stage()
    stage.map[11] = BIT_MASK_OBSTACLE
    
    map_ = stage.map.copy()
    map_[11] = BIT_MASK_OBSTACLE_DESTROYED
    map_[12] = BIT_MASK_FLOOR | BIT_MASK_CHARACTER | BIT_FLAG_WEST
    history = [
        HistoryElement(
            12,
            True,
            (
                (12, stage.map[12]),
                (11, stage.map[11]),
            ),
        ),
    ]
    
    yield (
        'west',
        stage,
        -1,
        BIT_FLAG_WEST,
        (
            True,
            map_,
            stage.start_position,
            False,
            history,
        ),
    )
    
    stage = _build_default_stage()
    stage.map[7] = BIT_MASK_FLOOR | BIT_MASK_BOX
    
    yield (
        'cannot, test with box',
        stage,
        -5,
        BIT_FLAG_NORTH,
        (
            False,
            stage.map.copy(),
            stage.start_position,
            True,
            [],
        ),
    )


@vampytest._(vampytest.call_from(_iter_options__use()).named_first().returning_last())
def test__SKILL_DESTROY_OBSTACLE__use(stage, step, align):
    """
    Tests whether ``SKILL_DESTROY_OBSTACLE.use`` works as intended.
    
    Parameters
    ----------
    stage : ``Stage``
        Stage to create game state with.
    
    step : `int`
        Difference between 2 adjacent tile-s translated to 1 dimension based on the map's size.
    
    align : `int`
        The character's new align if the move is successful.
    
    Returns
    -------
    output : ``(bool, list<str>, int, bool, list<HistoryElement>)``
    """
    game_state = GameState(stage, -1)
    output = SKILL_DESTROY_OBSTACLE.use(game_state, step, align)
    vampytest.assert_instance(output, bool)
    
    return (
        output,
        game_state.map,
        game_state.position,
        game_state.has_skill,
        game_state.history,
    )
