import vampytest


from ....chapters import CHAPTER_DEFAULT, Stage
from ....move_directions import (
    MOVE_DIRECTION_EAST, MOVE_DIRECTION_NORTH, MOVE_DIRECTION_SOUTH, MOVE_DIRECTION_WEST, MoveDirections
)
from ....tile_bit_masks import (
    BIT_FLAG_EAST, BIT_FLAG_NORTH, BIT_FLAG_SOUTH, BIT_FLAG_WEST, BIT_MASK_BOX, BIT_MASK_CHARACTER, BIT_MASK_FLOOR,
    BIT_MASK_HOLE, BIT_MASK_WALL
)
from ....user_state import HistoryElement, GameState

from ..teleport_over_occupied import SKILL_TELEPORT_OVER_OCCUPIED


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
            wall    , wall  , wall  , wall      , wall  , wall  , wall  ,
            wall    , floor , floor , floor     , floor , floor , wall  ,
            wall    , floor , floor , floor     , floor , floor , wall  ,
            wall    , floor , floor , character , floor , floor , wall  ,
            wall    , floor , floor , floor     , floor , floor , wall  ,
            wall    , floor , floor , floor     , floor , floor , wall  ,
            wall    , floor , floor , floor     , floor , floor , wall  ,
            wall    , wall  , wall  , wall      , wall  , wall  , wall  ,
        ],
        7,
        24,
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
    stage.map[17] = BIT_MASK_FLOOR | BIT_MASK_BOX
    
    yield (
        'north',
        stage,
        True,
    )
    
    stage = _build_default_stage()
    stage.map[25] = BIT_MASK_FLOOR | BIT_MASK_BOX
    
    yield (
        'east',
        stage,
        True,
    )
    
    stage = _build_default_stage()
    stage.map[31] = BIT_MASK_FLOOR | BIT_MASK_BOX
    
    yield (
        'south',
        stage,
        True,
    )
    
    stage = _build_default_stage()
    stage.map[23] = BIT_MASK_FLOOR | BIT_MASK_BOX
    
    yield (
        'west',
        stage,
        True,
    )
    
    stage = _build_default_stage()
    stage.map[17] = BIT_MASK_HOLE
    
    yield (
        'cannot, test with hole',
        stage,
        False,
    )
    
    stage = _build_default_stage()
    stage.map[17] = BIT_MASK_WALL | BIT_FLAG_NORTH
    
    yield (
        'north, wall',
        stage,
        True,
    )
    
    stage = _build_default_stage()
    stage.map[31] = BIT_MASK_FLOOR | BIT_MASK_BOX
    stage.map[38] = BIT_MASK_FLOOR | BIT_MASK_BOX
    
    yield (
        'south, double box',
        stage,
        True,
    )
    
    stage = _build_default_stage()
    stage.map[31] = BIT_MASK_WALL | BIT_FLAG_NORTH
    stage.map[38] = BIT_MASK_WALL | BIT_FLAG_NORTH
    
    yield (
        'south, double wall',
        stage,
        True,
    )
    
    stage = _build_default_stage()
    stage.map[31] = BIT_MASK_WALL | BIT_FLAG_NORTH
    stage.map[38] = BIT_MASK_FLOOR | BIT_MASK_BOX
    
    yield (
        'south, wall and box',
        stage,
        True,
    )
    
    stage = _build_default_stage()
    stage.map[31] = BIT_MASK_WALL | BIT_FLAG_NORTH
    stage.map[38] = BIT_MASK_HOLE
    
    yield (
        'cannot, wall then hole',
        stage,
        False,
    )
    
    stage = _build_default_stage()
    stage.map[17] = BIT_MASK_WALL | BIT_FLAG_NORTH
    stage.map[10] = BIT_MASK_WALL | BIT_FLAG_NORTH
    
    yield (
        'cannot, wall thill edge',
        stage,
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__can_activate()).named_first().returning_last())
def test__SKILL_TELEPORT_OVER_OCCUPIED__can_activate(stage):
    """
    Tests whether ``SKILL_TELEPORT_OVER_OCCUPIED.can_activate`` works as intended.
    
    Parameters
    ----------
    stage : ``Stage``
        Stage to create game state with.
    
    Returns
    -------
    output : `bool`
    """
    game_state = GameState(stage, -1)
    output = SKILL_TELEPORT_OVER_OCCUPIED.can_activate(game_state)
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
    stage.map[17] = BIT_MASK_FLOOR | BIT_MASK_BOX
    directions = MoveDirections()
    directions.set(MOVE_DIRECTION_NORTH, True)
    
    yield (
        'north',
        stage,
        directions,
    )
    
    stage = _build_default_stage()
    stage.map[25] = BIT_MASK_FLOOR | BIT_MASK_BOX
    directions = MoveDirections()
    directions.set(MOVE_DIRECTION_EAST, True)
    
    yield (
        'east',
        stage,
        directions,
    )
    
    stage = _build_default_stage()
    stage.map[31] = BIT_MASK_FLOOR | BIT_MASK_BOX
    directions = MoveDirections()
    directions.set(MOVE_DIRECTION_SOUTH, True)
    
    yield (
        'south',
        stage,
        directions,
    )
    
    stage = _build_default_stage()
    stage.map[23] = BIT_MASK_FLOOR | BIT_MASK_BOX
    directions = MoveDirections()
    directions.set(MOVE_DIRECTION_WEST, True)
    
    yield (
        'west',
        stage,
        directions,
    )
    
    stage = _build_default_stage()
    stage.map[17] = BIT_MASK_HOLE
    directions = MoveDirections()
    
    yield (
        'cannot, test with hole',
        stage,
        directions,
    )
    
    stage = _build_default_stage()
    stage.map[17] = BIT_MASK_WALL | BIT_FLAG_NORTH
    directions = MoveDirections()
    directions.set(MOVE_DIRECTION_NORTH, True)
    
    yield (
        'north, wall',
        stage,
        directions,
    )
    
    stage = _build_default_stage()
    stage.map[31] = BIT_MASK_FLOOR | BIT_MASK_BOX
    stage.map[38] = BIT_MASK_FLOOR | BIT_MASK_BOX
    directions = MoveDirections()
    directions.set(MOVE_DIRECTION_SOUTH, True)
    
    yield (
        'south, double box',
        stage,
        directions,
    )
    
    stage = _build_default_stage()
    stage.map[31] = BIT_MASK_WALL | BIT_FLAG_NORTH
    stage.map[38] = BIT_MASK_WALL | BIT_FLAG_NORTH
    directions = MoveDirections()
    directions.set(MOVE_DIRECTION_SOUTH, True)
    
    yield (
        'sauth, double wall',
        stage,
        directions,
    )
    
    stage = _build_default_stage()
    stage.map[31] = BIT_MASK_WALL | BIT_FLAG_NORTH
    stage.map[38] = BIT_MASK_FLOOR | BIT_MASK_BOX
    directions = MoveDirections()
    directions.set(MOVE_DIRECTION_SOUTH, True)
    
    yield (
        'south, wall and box',
        stage,
        directions,
    )
    
    stage = _build_default_stage()
    stage.map[31] = BIT_MASK_WALL | BIT_FLAG_NORTH
    stage.map[38] = BIT_MASK_HOLE
    directions = MoveDirections()
    
    yield (
        'cannot, wall then hole',
        stage,
        directions,
    )
    
    stage = _build_default_stage()
    stage.map[17] = BIT_MASK_WALL | BIT_FLAG_NORTH
    stage.map[10] = BIT_MASK_WALL | BIT_FLAG_NORTH
    directions = MoveDirections()
    
    yield (
        'cannot, wall thill edge',
        stage,
        directions,
    )


@vampytest._(vampytest.call_from(_iter_options__get_directions()).named_first().returning_last())
def test__SKILL_TELEPORT_OVER_OCCUPIED__get_directions(stage):
    """
    Tests whether ``SKILL_TELEPORT_OVER_OCCUPIED.get_directions`` works as intended.
    
    Parameters
    ----------
    stage : ``Stage``
        Stage to create game state with.
    
    Returns
    -------
    output : ``MoveDirections``
    """
    game_state = GameState(stage, -1)
    output = SKILL_TELEPORT_OVER_OCCUPIED.get_directions(game_state)
    vampytest.assert_instance(output, MoveDirections)
    return output


def _iter_options__use():
    stage = _build_default_stage()
    
    yield (
        'cannot',
        stage,
        -7,
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
    stage.map[17] = BIT_MASK_FLOOR | BIT_MASK_BOX
    
    map_ = stage.map.copy()
    map_[24] = BIT_MASK_FLOOR
    map_[10] = BIT_MASK_FLOOR | BIT_MASK_CHARACTER | BIT_FLAG_NORTH
    history = [
        HistoryElement(
            24,
            True,
            (
                (24, stage.map[24]),
                (10, stage.map[10]),
            ),
        ),
    ]
    
    yield (
        'north',
        stage,
        -7,
        BIT_FLAG_NORTH,
        (
            True,
            map_,
            10,
            False,
            history,
        ),
    )
    
    stage = _build_default_stage()
    stage.map[25] = BIT_MASK_FLOOR | BIT_MASK_BOX
    
    map_ = stage.map.copy()
    map_[24] = BIT_MASK_FLOOR
    map_[26] = BIT_MASK_FLOOR | BIT_MASK_CHARACTER | BIT_FLAG_EAST
    history = [
        HistoryElement(
            24,
            True,
            (
                (24, stage.map[24]),
                (26, stage.map[26]),
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
            26,
            False,
            history,
        ),
    )
    
    stage = _build_default_stage()
    stage.map[31] = BIT_MASK_FLOOR | BIT_MASK_BOX
    
    map_ = stage.map.copy()
    map_[24] = BIT_MASK_FLOOR
    map_[38] = BIT_MASK_FLOOR | BIT_MASK_CHARACTER | BIT_FLAG_SOUTH
    history = [
        HistoryElement(
            24,
            True,
            (
                (24, stage.map[24]),
                (38, stage.map[38]),
            ),
        ),
    ]
    
    yield (
        'south',
        stage,
        +7,
        BIT_FLAG_SOUTH,
        (
            True,
            map_,
            38,
            False,
            history,
        ),
    )
    
    stage = _build_default_stage()
    stage.map[23] = BIT_MASK_FLOOR | BIT_MASK_BOX
    
    map_ = stage.map.copy()
    map_[24] = BIT_MASK_FLOOR
    map_[22] = BIT_MASK_FLOOR | BIT_MASK_CHARACTER | BIT_FLAG_WEST
    history = [
        HistoryElement(
            24,
            True,
            (
                (24, stage.map[24]),
                (22, stage.map[22]),
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
            22,
            False,
            history,
        ),
    )
    
    stage = _build_default_stage()
    stage.map[17] = BIT_MASK_HOLE
    
    yield (
        'cannot, test with hole',
        stage,
        -7,
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
    stage.map[17] = BIT_MASK_WALL | BIT_FLAG_NORTH
    
    map_ = stage.map.copy()
    map_[24] = BIT_MASK_FLOOR
    map_[10] = BIT_MASK_FLOOR | BIT_MASK_CHARACTER | BIT_FLAG_NORTH
    history = [
        HistoryElement(
            24,
            True,
            (
                (24, stage.map[24]),
                (10, stage.map[10]),
            ),
        ),
    ]
    
    yield (
        'north, wall',
        stage,
        -7,
        BIT_FLAG_NORTH,
        (
            True,
            map_,
            10,
            False,
            history,
        ),
    )
    
    stage = _build_default_stage()
    stage.map[31] = BIT_MASK_FLOOR | BIT_MASK_BOX
    stage.map[38] = BIT_MASK_FLOOR | BIT_MASK_BOX
    
    map_ = stage.map.copy()
    map_[24] = BIT_MASK_FLOOR
    map_[45] = BIT_MASK_FLOOR | BIT_MASK_CHARACTER | BIT_FLAG_SOUTH
    history = [
        HistoryElement(
            24,
            True,
            (
                (24, stage.map[24]),
                (45, stage.map[45]),
            ),
        ),
    ]
    
    yield (
        'south, double box',
        stage,
        +7,
        BIT_FLAG_SOUTH,
        (
            True,
            map_,
            45,
            False,
            history,
        ),
    )
    
    stage = _build_default_stage()
    stage.map[31] = BIT_MASK_WALL | BIT_FLAG_NORTH
    stage.map[38] = BIT_MASK_WALL | BIT_FLAG_NORTH
    
    map_ = stage.map.copy()
    map_[24] = BIT_MASK_FLOOR
    map_[45] = BIT_MASK_FLOOR | BIT_MASK_CHARACTER | BIT_FLAG_SOUTH
    history = [
        HistoryElement(
            24,
            True,
            (
                (24, stage.map[24]),
                (45, stage.map[45]),
            ),
        ),
    ]
    
    yield (
        'south, double wall',
        stage,
        +7,
        BIT_FLAG_SOUTH,
        (
            True,
            map_,
            45,
            False,
            history,
        ),
    )

    stage = _build_default_stage()
    stage.map[31] = BIT_MASK_WALL | BIT_FLAG_NORTH
    stage.map[38] = BIT_MASK_FLOOR | BIT_MASK_BOX
    
    map_ = stage.map.copy()
    map_[24] = BIT_MASK_FLOOR
    map_[45] = BIT_MASK_FLOOR | BIT_MASK_CHARACTER | BIT_FLAG_SOUTH
    history = [
        HistoryElement(
            24,
            True,
            (
                (24, stage.map[24]),
                (45, stage.map[45]),
            ),
        ),
    ]
    
    yield (
        'south, wall and box',
        stage,
        +7,
        BIT_FLAG_SOUTH,
        (
            True,
            map_,
            45,
            False,
            history,
        ),
    )
    
    stage = _build_default_stage()
    stage.map[31] = BIT_MASK_WALL | BIT_FLAG_NORTH
    stage.map[38] = BIT_MASK_HOLE
    
    yield (
        'cannot, wall then hole',
        stage,
        +7,
        BIT_FLAG_SOUTH,
        (
            False,
            stage.map.copy(),
            stage.start_position,
            True,
            [],
        ),
    )
    
    stage = _build_default_stage()
    stage.map[17] = BIT_MASK_WALL | BIT_FLAG_NORTH
    stage.map[10] = BIT_MASK_WALL | BIT_FLAG_NORTH
    
    yield (
        'cannot, wall thill edge',
        stage,
        -7,
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
def test__SKILL_TELEPORT_OVER_OCCUPIED__use(stage, step, align):
    """
    Tests whether ``SKILL_TELEPORT_OVER_OCCUPIED.use`` works as intended.
    
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
    output = SKILL_TELEPORT_OVER_OCCUPIED.use(game_state, step, align)
    vampytest.assert_instance(output, bool)
    
    return (
        output,
        game_state.map,
        game_state.position,
        game_state.has_skill,
        game_state.history,
    )
