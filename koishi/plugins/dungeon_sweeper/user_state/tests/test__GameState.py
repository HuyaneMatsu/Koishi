import vampytest

from ...chapters import CHAPTER_DEFAULT, Chapter, Stage
from ...move_directions import (
    MOVE_DIRECTION_EAST, MOVE_DIRECTION_EAST_TO_SOUTH, MOVE_DIRECTION_NORTH, MOVE_DIRECTION_NORTH_TO_EAST,
    MOVE_DIRECTION_SOUTH, MOVE_DIRECTION_SOUTH_TO_WEST, MOVE_DIRECTION_WEST, MOVE_DIRECTION_WEST_TO_NORTH,
    MoveDirections
)
from ...skills import SKILL_DESTROY_OBSTACLE, Skill
from ...tile_bit_masks import (
    BIT_FLAG_EAST, BIT_FLAG_NORTH, BIT_FLAG_SOUTH, BIT_FLAG_WEST, BIT_MASK_BOX, BIT_MASK_CHARACTER, BIT_MASK_FLOOR,
    BIT_MASK_HOLE, BIT_MASK_HOLE_FILLED, BIT_MASK_OBSTACLE, BIT_MASK_OBSTACLE_DESTROYED, BIT_MASK_TARGET_ON_FLOOR,
    BIT_MASK_WALL
)

from ..game_state import (
    GameState, JSON_KEY_GAME_STATE_HAS_SKILL, JSON_KEY_GAME_STATE_HISTORY, JSON_KEY_GAME_STATE_MAP,
    JSON_KEY_GAME_STATE_NEXT_SKILL, JSON_KEY_GAME_STATE_POSITION, JSON_KEY_GAME_STATE_STAGE_BEST,
    JSON_KEY_GAME_STATE_STAGE_ID
)
from ..history_element import HistoryElement


def _assert_fields_set(game_state):
    """
    Asserts whether every fields are set of the game state.
    
    Parameters
    ----------
    game_state : ``GameState``
        The game state to check.
    """
    vampytest.assert_instance(game_state, GameState)
    
    vampytest.assert_instance(game_state.best, int)
    vampytest.assert_instance(game_state.chapter, Chapter)
    vampytest.assert_instance(game_state.has_skill, bool)
    vampytest.assert_instance(game_state.history, list)
    vampytest.assert_instance(game_state.map, list)
    vampytest.assert_instance(game_state.next_skill, bool)
    vampytest.assert_instance(game_state.position, int)
    vampytest.assert_instance(game_state.skill, Skill)
    vampytest.assert_instance(game_state.stage, Stage)


def _create_test_stage():
    """
    Creates a stage for testing.
    
    Returns
    -------
    stage : ``Stage``
    """
    wall = BIT_MASK_WALL | BIT_FLAG_NORTH
    character = BIT_MASK_FLOOR | BIT_MASK_CHARACTER | BIT_FLAG_NORTH
    target = BIT_MASK_TARGET_ON_FLOOR
    floor = BIT_MASK_FLOOR
    box = BIT_MASK_FLOOR | BIT_MASK_BOX
    hole = BIT_MASK_HOLE
    
    return Stage(
        CHAPTER_DEFAULT.id,
        999,
        
        0,
        0,
        0,
        0,
        
        3,
        [
            wall, wall, wall, wall, wall,
            wall, floor, box, target, wall,
            wall, floor, character, floor, wall,
            wall, floor, floor, hole, wall,
            wall, wall, wall, wall, wall,
        ],
        5,
        12,
        1,
    )


def test__GameState__new():
    """
    Tests whether ``GameState.__new__`` works as intended.
    """
    stage = _create_test_stage()
    best = 5
    
    game_state = GameState(stage, best)
    _assert_fields_set(game_state)
    
    vampytest.assert_eq(game_state.best, best)
    vampytest.assert_is(game_state.chapter, stage.get_chapter())
    vampytest.assert_eq(game_state.has_skill, True)
    vampytest.assert_eq(game_state.history, [])
    vampytest.assert_eq(game_state.map, stage.map.copy())
    vampytest.assert_eq(game_state.next_skill, False)
    vampytest.assert_eq(game_state.position, stage.start_position)
    vampytest.assert_is(game_state.skill, stage.get_chapter().get_skill())
    vampytest.assert_is(game_state.stage, stage)


def test__GameState__repr():
    """
    Tests whether ``GameState.__repr__`` works as intended.
    """
    stage = _create_test_stage()
    best = 5
    
    game_state = GameState(stage, best)
    
    output = repr(game_state)
    vampytest.assert_instance(output, str)


def test__GameState__from_data():
    """
    Tests whether ``GameState.from_data`` works as intended.
    """
    stage = _create_test_stage()
    best = 5
    
    patched = vampytest.mock_globals(
        GameState.from_data.__func__,
        STAGES = {
            stage.id : stage,
        },
    )
    
    map_ = stage.map.copy()
    map_[11] = BIT_MASK_FLOOR | BIT_MASK_CHARACTER | BIT_FLAG_WEST
    map_[12] = BIT_MASK_FLOOR
    position = 11
    has_skill = False
    next_skill = False
    history = [
        HistoryElement(
            12,
            False,
            (
                (12, stage.map[12]),
                (11, stage.map[11]),
            ),
        ),
    ]
    
    data = {
        JSON_KEY_GAME_STATE_STAGE_ID : stage.id,
        JSON_KEY_GAME_STATE_STAGE_BEST : best,
        JSON_KEY_GAME_STATE_MAP : map_,
        JSON_KEY_GAME_STATE_POSITION : position,
        JSON_KEY_GAME_STATE_HAS_SKILL : has_skill,
        JSON_KEY_GAME_STATE_NEXT_SKILL : next_skill,
        JSON_KEY_GAME_STATE_HISTORY : [history_element.to_data() for history_element in history],
    }
    
    game_state = patched(GameState, data)
    _assert_fields_set(game_state)
    
    vampytest.assert_eq(game_state.best, best)
    vampytest.assert_is(game_state.chapter, stage.get_chapter())
    vampytest.assert_eq(game_state.has_skill, has_skill)
    vampytest.assert_eq(game_state.history, history)
    vampytest.assert_eq(game_state.map, map_)
    vampytest.assert_eq(game_state.next_skill, next_skill)
    vampytest.assert_eq(game_state.position, position)
    vampytest.assert_is(game_state.skill, stage.get_chapter().get_skill())
    vampytest.assert_is(game_state.stage, stage)


def test__GameState__to_data():
    """
    Tests whether ``GameState.to_data`` works as intended.
    """
    stage = _create_test_stage()
    best = 5
    
    map_ = stage.map.copy()
    map_[11] = BIT_MASK_FLOOR | BIT_MASK_CHARACTER | BIT_FLAG_WEST
    map_[12] = BIT_MASK_FLOOR
    position = 11
    has_skill = False
    next_skill = False
    history = [
        HistoryElement(
            12,
            False,
            (
                (12, stage.map[12]),
                (11, stage.map[11]),
            ),
        ),
    ]
    
    game_state = GameState(stage, best)
    game_state.map[:] = map_
    game_state.position = position
    game_state.has_skill = has_skill
    game_state.next_skill = next_skill
    game_state.history[:] = history
    
    output = game_state.to_data()
    
    vampytest.assert_eq(
        output,
        {
            JSON_KEY_GAME_STATE_STAGE_ID : stage.id,
            JSON_KEY_GAME_STATE_STAGE_BEST : best,
            JSON_KEY_GAME_STATE_MAP : map_,
            JSON_KEY_GAME_STATE_POSITION : position,
            JSON_KEY_GAME_STATE_HAS_SKILL : has_skill,
            JSON_KEY_GAME_STATE_NEXT_SKILL : next_skill,
            JSON_KEY_GAME_STATE_HISTORY : [history_element.to_data() for history_element in history],
        },
    )


def test__GameState__restart__success():
    """
    Tests whether ``GameState.restart`` works as intended.
    
    Case: success.
    """
    stage = _create_test_stage()
    best = 5
    
    map_ = stage.map.copy()
    map_[11] = BIT_MASK_FLOOR | BIT_MASK_CHARACTER | BIT_FLAG_WEST
    map_[12] = BIT_MASK_FLOOR
    position = 11
    has_skill = False
    next_skill = False
    history = [
        HistoryElement(
            12,
            False,
            (
                (12, stage.map[12]),
                (11, stage.map[11]),
            ),
        ),
    ]
    
    game_state = GameState(stage, best)
    
    game_state.map[:] = map_
    game_state.position = position
    game_state.has_skill = has_skill
    game_state.next_skill = next_skill
    game_state.history[:] = history
    
    output = game_state.restart()
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)
    
    vampytest.assert_eq(game_state.best, best)
    vampytest.assert_is(game_state.chapter, stage.get_chapter())
    vampytest.assert_eq(game_state.has_skill, True)
    vampytest.assert_eq(game_state.history, [])
    vampytest.assert_eq(game_state.map, stage.map.copy())
    vampytest.assert_eq(game_state.next_skill, False)
    vampytest.assert_eq(game_state.position, stage.start_position)
    vampytest.assert_is(game_state.skill, stage.get_chapter().get_skill())
    vampytest.assert_is(game_state.stage, stage)


def test__GameState__restart__nothing_to_restart():
    """
    Tests whether ``GameState.restart`` works as intended.
    
    Case: nothing to restart..
    """
    stage = _create_test_stage()
    best = 5
    
    game_state = GameState(stage, best)
    
    output = game_state.restart()
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)
    
    vampytest.assert_eq(game_state.best, best)
    vampytest.assert_is(game_state.chapter, stage.get_chapter())
    vampytest.assert_eq(game_state.has_skill, True)
    vampytest.assert_eq(game_state.history, [])
    vampytest.assert_eq(game_state.map, stage.map.copy())
    vampytest.assert_eq(game_state.next_skill, False)
    vampytest.assert_eq(game_state.position, stage.start_position)
    vampytest.assert_is(game_state.skill, stage.get_chapter().get_skill())
    vampytest.assert_is(game_state.stage, stage)


def test__GameState__is_done__false():
    """
    Tests whether ``GameState.is_done`` works as intended.
    
    Case: false.
    """
    stage = _create_test_stage()
    best = 5
    
    game_state = GameState(stage, best)
    
    output = game_state.is_done()
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)
    vampytest.assert_eq(game_state.best, best)


def test__GameState__is_done__true():
    """
    Tests whether ``GameState.is_done`` works as intended.
    
    Case: true.
    """
    stage = _create_test_stage()
    best = 5
    
    game_state = GameState(stage, best)
    
    map_ = stage.map.copy()
    map_[7] = BIT_MASK_FLOOR | BIT_MASK_CHARACTER | BIT_FLAG_EAST
    map_[8] = BIT_MASK_TARGET_ON_FLOOR | BIT_MASK_BOX
    map_[11] = BIT_MASK_FLOOR
    map_[12] = BIT_MASK_FLOOR
    
    position = 8
    
    history = [
        HistoryElement(
            12,
            False,
            (
                (12, BIT_MASK_FLOOR | BIT_MASK_CHARACTER | BIT_FLAG_NORTH),
                (11, BIT_MASK_FLOOR),
            ),
        ),
        HistoryElement(
            11,
            False,
            (
                (11, BIT_MASK_FLOOR | BIT_MASK_CHARACTER | BIT_FLAG_WEST),
                (6, BIT_MASK_FLOOR),
            ),
        ),
        HistoryElement(
            6,
            False,
            (
                (6, BIT_MASK_FLOOR | BIT_MASK_CHARACTER | BIT_FLAG_NORTH),
                (7, BIT_MASK_FLOOR | BIT_MASK_BOX),
                (8, BIT_MASK_TARGET_ON_FLOOR),
            ),
        ),
    ]
    
    game_state.map[:] = map_
    game_state.position = position
    game_state.history[:] = history
    
    output = game_state.is_done()
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)
    vampytest.assert_eq(game_state.best, len(history))


def test__GameState__move_north__can():
    """
    Tests whether ``GameState.move_north`` works as intended.
    
    Case: can.
    """
    stage = _create_test_stage()
    stage.map[7] = BIT_MASK_FLOOR
    best = 5
    
    game_state = GameState(stage, best)
    
    output = game_state.move_north()
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)
    
    map_ = stage.map.copy()
    map_[7] = BIT_MASK_FLOOR | BIT_MASK_CHARACTER | BIT_FLAG_NORTH
    map_[12] = BIT_MASK_FLOOR
    
    vampytest.assert_eq(game_state.map, map_)
    
    vampytest.assert_eq(
        game_state.history,
        [
            HistoryElement(
                12,
                False,
                (
                    (12, BIT_MASK_FLOOR | BIT_MASK_CHARACTER | BIT_FLAG_NORTH),
                    (7, BIT_MASK_FLOOR),
                ),
            ),
        ],
    )
    
    vampytest.assert_eq(game_state.position, 7)


def test__GameState__move_north__cannot():
    """
    Tests whether ``GameState.move_north`` works as intended.
    
    Case: cannot.
    """
    stage = _create_test_stage()
    stage.map[7] = BIT_MASK_WALL | BIT_FLAG_NORTH
    best = 5
    
    game_state = GameState(stage, best)
    
    output = game_state.move_north()
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)
    
    map_ = stage.map.copy()
    
    vampytest.assert_eq(game_state.map, map_)
    
    vampytest.assert_eq(
        game_state.history,
        [],
    )
    
    vampytest.assert_eq(game_state.position, stage.start_position)


def test__GameState__move_east__can():
    """
    Tests whether ``GameState.move_east`` works as intended.
    
    Case: can.
    """
    stage = _create_test_stage()
    stage.map[13] = BIT_MASK_FLOOR
    best = 5
    
    game_state = GameState(stage, best)
    
    output = game_state.move_east()
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)
    
    map_ = stage.map.copy()
    map_[13] = BIT_MASK_FLOOR | BIT_MASK_CHARACTER | BIT_FLAG_EAST
    map_[12] = BIT_MASK_FLOOR
    
    vampytest.assert_eq(game_state.map, map_)
    
    vampytest.assert_eq(
        game_state.history,
        [
            HistoryElement(
                12,
                False,
                (
                    (12, BIT_MASK_FLOOR | BIT_MASK_CHARACTER | BIT_FLAG_NORTH),
                    (13, BIT_MASK_FLOOR),
                ),
            ),
        ],
    )
    
    vampytest.assert_eq(game_state.position, 13)


def test__GameState__move_east__cannot():
    """
    Tests whether ``GameState.move_east`` works as intended.
    
    Case: cannot.
    """
    stage = _create_test_stage()
    stage.map[13] = BIT_MASK_WALL | BIT_FLAG_NORTH
    best = 5
    
    game_state = GameState(stage, best)
    
    output = game_state.move_east()
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)
    
    map_ = stage.map.copy()
    
    vampytest.assert_eq(game_state.map, map_)
    
    vampytest.assert_eq(
        game_state.history,
        [],
    )
    
    vampytest.assert_eq(game_state.position, stage.start_position)


def test__GameState__move_south__can():
    """
    Tests whether ``GameState.move_south`` works as intended.
    
    Case: can.
    """
    stage = _create_test_stage()
    stage.map[17] = BIT_MASK_FLOOR
    best = 5
    
    game_state = GameState(stage, best)
    
    output = game_state.move_south()
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)
    
    map_ = stage.map.copy()
    map_[17] = BIT_MASK_FLOOR | BIT_MASK_CHARACTER | BIT_FLAG_SOUTH
    map_[12] = BIT_MASK_FLOOR
    
    vampytest.assert_eq(game_state.map, map_)
    vampytest.assert_eq(
        game_state.history,
        [
            HistoryElement(
                12,
                False,
                (
                    (12, BIT_MASK_FLOOR | BIT_MASK_CHARACTER | BIT_FLAG_NORTH),
                    (17, BIT_MASK_FLOOR),
                ),
            ),
        ],
    )
    
    vampytest.assert_eq(game_state.position, 17)


def test__GameState__move_south__cannot():
    """
    Tests whether ``GameState.move_south`` works as intended.
    
    Case: cannot.
    """
    stage = _create_test_stage()
    stage.map[17] = BIT_MASK_WALL | BIT_FLAG_NORTH
    best = 5
    
    game_state = GameState(stage, best)
    
    output = game_state.move_south()
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)
    
    map_ = stage.map.copy()
    
    vampytest.assert_eq(game_state.map, map_)
    
    vampytest.assert_eq(
        game_state.history,
        [],
    )
    
    vampytest.assert_eq(game_state.position, stage.start_position)


def test__GameState__move_west__can():
    """
    Tests whether ``GameState.move_west`` works as intended.
    
    Case: can.
    """
    stage = _create_test_stage()
    stage.map[11] = BIT_MASK_FLOOR
    best = 5
    
    game_state = GameState(stage, best)
    
    output = game_state.move_west()
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)
    
    map_ = stage.map.copy()
    map_[11] = BIT_MASK_FLOOR | BIT_MASK_CHARACTER | BIT_FLAG_WEST
    map_[12] = BIT_MASK_FLOOR
    
    vampytest.assert_eq(game_state.map, map_)
    
    vampytest.assert_eq(
        game_state.history,
        [
            HistoryElement(
                12,
                False,
                (
                    (12, BIT_MASK_FLOOR | BIT_MASK_CHARACTER | BIT_FLAG_NORTH),
                    (11, BIT_MASK_FLOOR),
                ),
            ),
        ],
    )
    
    vampytest.assert_eq(game_state.position, 11)


def test__GameState__move_west__cannot():
    """
    Tests whether ``GameState.move_west`` works as intended.
    
    Case: cannot.
    """
    stage = _create_test_stage()
    stage.map[11] = BIT_MASK_WALL | BIT_FLAG_NORTH
    best = 5
    
    game_state = GameState(stage, best)
    
    output = game_state.move_west()
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)
    
    map_ = stage.map.copy()
    
    vampytest.assert_eq(game_state.map, map_)
    
    vampytest.assert_eq(
        game_state.history,
        [],
    )
    
    vampytest.assert_eq(game_state.position, stage.start_position)


def test__GameState__get_directions__blocked():
    """
    Tests whether ``GameState.get_directions`` works as intended.
    
    Case: blocked.
    """
    stage = _create_test_stage()
    stage.map[11] = BIT_MASK_WALL | BIT_FLAG_NORTH
    stage.map[13] = BIT_MASK_WALL | BIT_FLAG_NORTH
    stage.map[7] = BIT_MASK_WALL | BIT_FLAG_NORTH
    stage.map[17] = BIT_MASK_WALL | BIT_FLAG_NORTH
    best = 5
    
    game_state = GameState(stage, best)
    
    expected_output = MoveDirections()
    
    output = game_state.get_directions()
    vampytest.assert_instance(output, MoveDirections)
    vampytest.assert_eq(output, expected_output)


def test__GameState__get_directions__non_blocked():
    """
    Tests whether ``GameState.get_directions`` works as intended.
    
    Case: non blocked.
    """
    stage = _create_test_stage()
    stage.map[11] = BIT_MASK_FLOOR
    stage.map[13] = BIT_MASK_FLOOR
    stage.map[6] = BIT_MASK_FLOOR
    stage.map[7] = BIT_MASK_FLOOR
    stage.map[8] = BIT_MASK_FLOOR
    stage.map[16] = BIT_MASK_FLOOR
    stage.map[17] = BIT_MASK_FLOOR
    stage.map[18] = BIT_MASK_FLOOR
    best = 5
    
    game_state = GameState(stage, best)
    
    expected_output = MoveDirections()
    expected_output.set(MOVE_DIRECTION_NORTH, True)
    expected_output.set(MOVE_DIRECTION_EAST, True)
    expected_output.set(MOVE_DIRECTION_SOUTH, True)
    expected_output.set(MOVE_DIRECTION_WEST, True)
    expected_output.set(MOVE_DIRECTION_NORTH_TO_EAST, True)
    expected_output.set(MOVE_DIRECTION_EAST_TO_SOUTH, True)
    expected_output.set(MOVE_DIRECTION_SOUTH_TO_WEST, True)
    expected_output.set(MOVE_DIRECTION_WEST_TO_NORTH, True)
    
    output = game_state.get_directions()
    vampytest.assert_instance(output, MoveDirections)
    vampytest.assert_eq(output, expected_output)


def test__GameState__get_directions__skill__blocked():
    """
    Tests whether ``GameState.get_directions`` works as intended.
    
    Case: skill blocked.
    """
    stage = _create_test_stage()
    stage.map[11] = BIT_MASK_WALL | BIT_FLAG_NORTH
    stage.map[13] = BIT_MASK_WALL | BIT_FLAG_NORTH
    stage.map[7] = BIT_MASK_WALL | BIT_FLAG_NORTH
    stage.map[17] = BIT_MASK_WALL | BIT_FLAG_NORTH
    best = 5
    
    game_state = GameState(stage, best)
    game_state.skill = SKILL_DESTROY_OBSTACLE
    game_state.next_skill = True
    
    expected_output = MoveDirections()
    
    output = game_state.get_directions()
    vampytest.assert_instance(output, MoveDirections)
    vampytest.assert_eq(output, expected_output)


def test__GameState__get_directions__skill__non_blocked():
    """
    Tests whether ``GameState.get_directions`` works as intended.
    
    Case: skill non blocked.
    """
    stage = _create_test_stage()
    stage.map[11] = BIT_MASK_OBSTACLE
    stage.map[13] = BIT_MASK_OBSTACLE
    stage.map[7] = BIT_MASK_OBSTACLE
    stage.map[17] = BIT_MASK_OBSTACLE
    best = 5
    
    game_state = GameState(stage, best)
    game_state.skill = SKILL_DESTROY_OBSTACLE
    game_state.next_skill = True
    
    expected_output = MoveDirections()
    expected_output.set(MOVE_DIRECTION_NORTH, True)
    expected_output.set(MOVE_DIRECTION_EAST, True)
    expected_output.set(MOVE_DIRECTION_SOUTH, True)
    expected_output.set(MOVE_DIRECTION_WEST, True)
    
    output = game_state.get_directions()
    vampytest.assert_instance(output, MoveDirections)
    vampytest.assert_eq(output, expected_output)


def test__GameState__move__skill_can():
    """
    Tests whether ``GameState.move`` works as intended.
    
    Case: skill can.
    """
    stage = _create_test_stage()
    stage.map[7] = BIT_MASK_OBSTACLE
    best = 5
    
    game_state = GameState(stage, best)
    game_state.skill = SKILL_DESTROY_OBSTACLE
    game_state.next_skill = True
    
    output = game_state.move(-stage.size_x, BIT_FLAG_NORTH)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)
    
    map_ = stage.map.copy()
    map_[7] = BIT_MASK_OBSTACLE_DESTROYED
    map_[12] = BIT_MASK_FLOOR | BIT_MASK_CHARACTER | BIT_FLAG_NORTH
    
    vampytest.assert_eq(game_state.map, map_)
    vampytest.assert_eq(game_state.position, 12)
    vampytest.assert_eq(game_state.next_skill, False)
    vampytest.assert_eq(game_state.has_skill, False)
    vampytest.assert_eq(
        game_state.history,
        [
            HistoryElement(
                12,
                True,
                (
                    (12, stage.map[12]),
                    (7, stage.map[7]),
                ),
            ),
        ],
    )


def test__GameState__move__skill_cannot():
    """
    Tests whether ``GameState.move`` works as intended.
    
    Case: skill cannot.
    """
    stage = _create_test_stage()
    stage.map[7] = BIT_MASK_WALL
    best = 5
    
    game_state = GameState(stage, best)
    game_state.skill = SKILL_DESTROY_OBSTACLE
    game_state.next_skill = True
    
    output = game_state.move(-stage.size_x, BIT_FLAG_NORTH)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)
    
    vampytest.assert_eq(game_state.map, stage.map.copy())
    vampytest.assert_eq(game_state.position, 12)
    vampytest.assert_eq(game_state.next_skill, True)
    vampytest.assert_eq(game_state.has_skill, True)
    vampytest.assert_eq(
        game_state.history,
        [],
    )


def test__GameState__move__cannot_unpushable():
    """
    Tests whether ``GameState.move`` works as intended.
    
    Case: cannot, unpushable.
    """
    stage = _create_test_stage()
    stage.map[7] = BIT_MASK_OBSTACLE
    best = 5
    
    game_state = GameState(stage, best)
    
    output = game_state.move(-stage.size_x, BIT_FLAG_NORTH)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)
    
    vampytest.assert_eq(game_state.map, stage.map.copy())
    vampytest.assert_eq(game_state.position, 12)
    vampytest.assert_eq(game_state.next_skill, False)
    vampytest.assert_eq(game_state.has_skill, True)
    vampytest.assert_eq(
        game_state.history,
        [],
    )


def test__GameState__move__can_passable():
    """
    Tests whether ``GameState.move`` works as intended.
    
    Case: can, passable.
    """
    stage = _create_test_stage()
    stage.map[7] = BIT_MASK_FLOOR
    best = 5
    
    game_state = GameState(stage, best)
    
    output = game_state.move(-stage.size_x, BIT_FLAG_NORTH)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)
    
    map_ = stage.map.copy()
    map_[7] = BIT_MASK_FLOOR | BIT_MASK_CHARACTER | BIT_FLAG_NORTH
    map_[12] = BIT_MASK_FLOOR
    
    vampytest.assert_eq(game_state.map, map_)
    vampytest.assert_eq(game_state.position, 7)
    vampytest.assert_eq(game_state.next_skill, False)
    vampytest.assert_eq(game_state.has_skill, True)
    vampytest.assert_eq(
        game_state.history,
        [
            HistoryElement(
                12,
                False,
                (
                    (12, stage.map[12]),
                    (7, stage.map[7]),
                ),
            ),
        ],
    )


def test__GameState__move__cannot_pushable_blocked_behind():
    """
    Tests whether ``GameState.move`` works as intended.
    
    Case: cannot, pushable blocked behind.
    """
    stage = _create_test_stage()
    stage.map[7] = BIT_MASK_BOX | BIT_MASK_TARGET_ON_FLOOR
    stage.map[12] = BIT_MASK_BOX | BIT_MASK_TARGET_ON_FLOOR
    stage.map[17] = BIT_MASK_FLOOR | BIT_MASK_CHARACTER | BIT_FLAG_NORTH
    stage.start_position = 17
    best = 5
    
    game_state = GameState(stage, best)
    
    output = game_state.move(-stage.size_x, BIT_FLAG_NORTH)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)
    
    vampytest.assert_eq(game_state.map, stage.map.copy())
    vampytest.assert_eq(game_state.position, 17)
    vampytest.assert_eq(game_state.next_skill, False)
    vampytest.assert_eq(game_state.has_skill, True)
    vampytest.assert_eq(
        game_state.history,
        [],
    )


def test__GameState__move__can_pushable_passable_behind():
    """
    Tests whether ``GameState.move`` works as intended.
    
    Case: can, pushable, passable behind.
    """
    stage = _create_test_stage()
    stage.map[7] = BIT_MASK_TARGET_ON_FLOOR
    stage.map[12] = BIT_MASK_BOX | BIT_MASK_TARGET_ON_FLOOR
    stage.map[17] = BIT_MASK_FLOOR | BIT_MASK_CHARACTER | BIT_FLAG_NORTH
    stage.start_position = 17
    best = 5
    
    game_state = GameState(stage, best)
    
    output = game_state.move(-stage.size_x, BIT_FLAG_NORTH)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)
    
    map_ = stage.map.copy()
    map_[17] = BIT_MASK_FLOOR
    map_[12] = BIT_MASK_TARGET_ON_FLOOR | BIT_MASK_CHARACTER | BIT_FLAG_NORTH
    map_[7] = BIT_MASK_BOX | BIT_MASK_TARGET_ON_FLOOR
    
    vampytest.assert_eq(game_state.map, map_)
    vampytest.assert_eq(game_state.position, 12)
    vampytest.assert_eq(game_state.next_skill, False)
    vampytest.assert_eq(game_state.has_skill, True)
    vampytest.assert_eq(
        game_state.history,
        [
            HistoryElement(
                17,
                False,
                (
                    (17, stage.map[17]),
                    (12, stage.map[12]),
                    (7, stage.map[7]),
                ),
            ),
        ],
    )


def test__GameState__move__can_pushable_hole_behind():
    """
    Tests whether ``GameState.move`` works as intended.
    
    Case: can, pushable, hole behind.
    """
    stage = _create_test_stage()
    stage.map[7] = BIT_MASK_HOLE
    stage.map[12] = BIT_MASK_BOX | BIT_MASK_TARGET_ON_FLOOR
    stage.map[17] = BIT_MASK_FLOOR | BIT_MASK_CHARACTER | BIT_FLAG_NORTH
    stage.start_position = 17
    best = 5
    
    game_state = GameState(stage, best)
    
    output = game_state.move(-stage.size_x, BIT_FLAG_NORTH)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)
    
    map_ = stage.map.copy()
    map_[17] = BIT_MASK_FLOOR
    map_[12] = BIT_MASK_TARGET_ON_FLOOR | BIT_MASK_CHARACTER | BIT_FLAG_NORTH
    map_[7] = BIT_MASK_HOLE_FILLED
    
    vampytest.assert_eq(game_state.map, map_)
    vampytest.assert_eq(game_state.position, 12)
    vampytest.assert_eq(game_state.next_skill, False)
    vampytest.assert_eq(game_state.has_skill, True)
    vampytest.assert_eq(
        game_state.history,
        [
            HistoryElement(
                17,
                False,
                (
                    (17, stage.map[17]),
                    (12, stage.map[12]),
                    (7, stage.map[7]),
                ),
            ),
        ],
    )


def test__GameState__skill_can_activate__no_skill():
    """
    Tests whether ``GameState.skill_can_activate`` works as intended.
    
    Case: no skill.
    """
    stage = _create_test_stage()
    stage.map[7] = BIT_MASK_OBSTACLE
    best = 5
    
    game_state = GameState(stage, best)
    game_state.skill = SKILL_DESTROY_OBSTACLE
    game_state.has_skill = False
    
    output = game_state.skill_can_activate()
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)


def test__GameState__skill_can_activate__cannot():
    """
    Tests whether ``GameState.skill_can_activate`` works as intended.
    
    Case: cannot.
    """
    stage = _create_test_stage()
    stage.map[7] = BIT_MASK_FLOOR
    best = 5
    
    game_state = GameState(stage, best)
    game_state.skill = SKILL_DESTROY_OBSTACLE
    game_state.has_skill = True
    
    output = game_state.skill_can_activate()
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)


def test__GameState__skill_can_activate__can():
    """
    Tests whether ``GameState.skill_can_activate`` works as intended.
    
    Case: can.
    """
    stage = _create_test_stage()
    stage.map[7] = BIT_MASK_OBSTACLE
    best = 5
    
    game_state = GameState(stage, best)
    game_state.skill = SKILL_DESTROY_OBSTACLE
    game_state.has_skill = True
    
    output = game_state.skill_can_activate()
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)


def test__GameState__skill_activate__no_skill():
    """
    Tests whether ``GameState.skill_activate`` works as intended.
    
    Case: no skill.
    """
    stage = _create_test_stage()
    stage.map[7] = BIT_MASK_OBSTACLE
    best = 5
    
    game_state = GameState(stage, best)
    game_state.skill = SKILL_DESTROY_OBSTACLE
    game_state.has_skill = False
    game_state.next_skill = False
    
    output = game_state.skill_activate()
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)
    
    vampytest.assert_eq(game_state.next_skill, False)


def test__GameState__skill_activate__cannot():
    """
    Tests whether ``GameState.skill_activate`` works as intended.
    
    Case: cannot.
    """
    stage = _create_test_stage()
    stage.map[7] = BIT_MASK_FLOOR
    best = 5
    
    game_state = GameState(stage, best)
    game_state.skill = SKILL_DESTROY_OBSTACLE
    game_state.has_skill = True
    game_state.next_skill = False
    
    output = game_state.skill_activate()
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)
    
    vampytest.assert_eq(game_state.next_skill, False)


def test__GameState__skill_activate__can():
    """
    Tests whether ``GameState.skill_activate`` works as intended.
    
    Case: can.
    """
    stage = _create_test_stage()
    stage.map[7] = BIT_MASK_OBSTACLE
    best = 5
    
    game_state = GameState(stage, best)
    game_state.skill = SKILL_DESTROY_OBSTACLE
    game_state.has_skill = True
    game_state.next_skill = False
    
    output = game_state.skill_activate()
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)
    
    vampytest.assert_eq(game_state.next_skill, True)


def test__GameState__skill_activate__already_active():
    """
    Tests whether ``GameState.skill_activate`` works as intended.
    
    Case: already active.
    """
    stage = _create_test_stage()
    stage.map[7] = BIT_MASK_FLOOR
    best = 5
    
    game_state = GameState(stage, best)
    game_state.skill = SKILL_DESTROY_OBSTACLE
    game_state.has_skill = True
    game_state.next_skill = True
    
    output = game_state.skill_activate()
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)
    
    vampytest.assert_eq(game_state.next_skill, False)


def test__GameState__can_back_or_restart__cannot():
    """
    Tests whether ``GameState.skill_activate`` works as intended.
    
    Case: cannot.
    """
    stage = _create_test_stage()
    best = 5
    
    game_state = GameState(stage, best)
    
    output = game_state.can_back_or_restart()
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)


def test__GameState__can_back_or_restart__can_next_skill():
    """
    Tests whether ``GameState.skill_activate`` works as intended.
    
    Case: can, next skill.
    """
    stage = _create_test_stage()
    best = 5
    
    game_state = GameState(stage, best)
    game_state.next_skill = True
    
    output = game_state.can_back_or_restart()
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)


def test__GameState__can_back_or_restart__can_has_history():
    """
    Tests whether ``GameState.skill_activate`` works as intended.
    
    Case: can, has history.
    """
    stage = _create_test_stage()
    best = 5
    
    game_state = GameState(stage, best)
    
    # Move 1 west
    game_state.history[:] = [
        HistoryElement(
            12,
            False,
            (
                (12, stage.map[12]),
                (11, stage.map[11]),
            ),
        ),
    ]
    game_state.position = 11
    game_state.map[12] = BIT_MASK_FLOOR
    game_state.map[11] = BIT_MASK_FLOOR | BIT_MASK_CHARACTER | BIT_FLAG_WEST
    
    output = game_state.can_back_or_restart()
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)


def test__GameState__back__cannot():
    """
    Tests whether ``GameState.skill_activate`` works as intended.
    
    Case: cannot.
    """
    stage = _create_test_stage()
    best = 5
    
    game_state = GameState(stage, best)
    
    output = game_state.back()
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)


def test__GameState__back__can_next_skill():
    """
    Tests whether ``GameState.skill_activate`` works as intended.
    
    Case: can, next skill.
    """
    stage = _create_test_stage()
    best = 5
    
    game_state = GameState(stage, best)
    game_state.next_skill = True
    
    output = game_state.back()
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)
    
    vampytest.assert_eq(game_state.next_skill, False)


def test__GameState__back__can_has_history():
    """
    Tests whether ``GameState.skill_activate`` works as intended.
    
    Case: can, has history.
    """
    stage = _create_test_stage()
    best = 5
    
    game_state = GameState(stage, best)
    
    # Move 1 west with skill (non existing move)
    game_state.has_skill = False
    game_state.history[:] = [
        HistoryElement(
            12,
            True,
            (
                (12, stage.map[12]),
                (11, stage.map[11]),
            ),
        ),
    ]
    game_state.position = 11
    game_state.map[12] = BIT_MASK_FLOOR
    game_state.map[11] = BIT_MASK_FLOOR | BIT_MASK_CHARACTER | BIT_FLAG_WEST
    
    output = game_state.back()
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)
    
    vampytest.assert_eq(game_state.has_skill, True)
    vampytest.assert_eq(game_state.history, [])
    vampytest.assert_eq(game_state.position, stage.start_position)
    vampytest.assert_eq(game_state.map, stage.map)
