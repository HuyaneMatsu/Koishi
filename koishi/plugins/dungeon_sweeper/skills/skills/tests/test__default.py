import vampytest


from ....chapters import CHAPTER_DEFAULT, Stage
from ....move_directions import MoveDirections
from ....tile_bit_masks import BIT_FLAG_NORTH, BIT_MASK_CHARACTER, BIT_MASK_FLOOR, BIT_MASK_WALL
from ....user_state import GameState

from ..default import SKILL_DEFAULT


def _build_default_stage():
    """
    Builds a default stage to use for testing.
    
    Returns
    -------
    stage : ``Stage``
    """
    wall = BIT_MASK_WALL | BIT_FLAG_NORTH
    character = BIT_MASK_FLOOR | BIT_MASK_CHARACTER | BIT_FLAG_NORTH
    
    return Stage(
        CHAPTER_DEFAULT.id,
        999,
        
        0,
        0,
        0,
        0,
        
        5,
        [
            wall    , wall      , wall  ,
            wall    , character , wall ,
            wall    , wall      , wall ,
        ],
        3,
        4,
        1,
    )


def _iter_options__can_activate():
    stage = _build_default_stage()
    
    yield (
        'cannot',
        stage,
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__can_activate()).named_first().returning_last())
def test__SKILL_DEFAULT__can_activate(stage):
    """
    Tests whether ``SKILL_DEFAULT.can_activate`` works as intended.
    
    Parameters
    ----------
    stage : ``Stage``
        Stage to create game state with.
    
    Returns
    -------
    output : `bool`
    """
    game_state = GameState(stage, -1)
    output = SKILL_DEFAULT.can_activate(game_state)
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


@vampytest._(vampytest.call_from(_iter_options__get_directions()).named_first().returning_last())
def test__SKILL_DEFAULT__get_directions(stage):
    """
    Tests whether ``SKILL_DEFAULT.get_directions`` works as intended.
    
    Parameters
    ----------
    stage : ``Stage``
        Stage to create game state with.
    
    Returns
    -------
    output : ``MoveDirections``
    """
    game_state = GameState(stage, -1)
    output = SKILL_DEFAULT.get_directions(game_state)
    vampytest.assert_instance(output, MoveDirections)
    return output


def _iter_options__use():
    stage = _build_default_stage()
    
    yield (
        'cannot',
        stage,
        -3,
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
def test__SKILL_DEFAULT__use(stage, step, align):
    """
    Tests whether ``SKILL_DEFAULT.use`` works as intended.
    
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
    output = SKILL_DEFAULT.use(game_state, step, align)
    vampytest.assert_instance(output, bool)
    
    return (
        output,
        game_state.map,
        game_state.position,
        game_state.has_skill,
        game_state.history,
    )
