__all__ = ('SKILL_DESTROY_OBSTACLE',)

from ...constants import SKILLS
from ...move_directions import DIRECTIONS_MAIN, MoveDirections
from ...tile_bit_masks import BIT_MASK_ALIGN_ALL, BIT_MASK_OBSTACLE, BIT_MASK_OBSTACLE_DESTROYED
from ...user_state import HistoryElement

from ..constants import SKILL_ID_DESTROY_OBSTACLE
from ..skill import Skill


def skill_can_activate(game_state):
    """
    Returns whether Flandre skill can be activated.
    
    Parameters
    ----------
    game_state : ``GameState``
        The respective game state.
    
    Returns
    -------
    can_active : `bool`
    """
    size_x = game_state.stage.size_x
    position = game_state.position
    map_ = game_state.map
    
    for step in (-size_x, 1, size_x, -1):
        target_tile = map_[position + step]
        
        if target_tile & BIT_MASK_OBSTACLE:
            return True
    
    return False


def skill_get_directions(game_state):
    """
    Returns to which directions Flandre's skill could be used.
    
    Parameters
    ----------
    game_state : ``GameState``
        The respective game state.
    
    Returns
    -------
    move_directions : ``MoveDirections``
    """
    size_x = game_state.stage.size_x
    position = game_state.position
    map_ = game_state.map
    
    move_directions = MoveDirections()
    
    for step, direction in zip((-size_x, 1, size_x, -1), DIRECTIONS_MAIN):
        target_tile = map_[position + step]
        if target_tile & BIT_MASK_OBSTACLE:
            can_go_to_direction = True
        else:
            can_go_to_direction = False
        
        move_directions.set(direction, can_go_to_direction)
    
    return move_directions


def skill_use(game_state, step, align):
    """
    Uses Flandre's skill to the represented directory.
    
    Parameters
    ----------
    game_state : ``GameState``
        The respective game state.
    
    step : `int`
        Difference between 2 adjacent tile-s translated to 1 dimension based on the map's size.
    
    align : `int`
        The character's new align if the move is successful.
    
    Returns
    -------
    success : `bool`
        Whether the move was completed successfully.
    """
    map_ = game_state.map
    position = game_state.position
    
    target_tile = map_[position + step]
    
    if not target_tile & BIT_MASK_OBSTACLE:
        return False
    
    actual_tile = map_[position]
    game_state.history.append(
        HistoryElement(
            position,
            True,
            (
                (position, actual_tile),
                (position + step, target_tile),
            ),
        ),
    )
    
    map_[position] = (actual_tile &~ BIT_MASK_ALIGN_ALL) | align
    map_[position + step] = (target_tile &~ BIT_MASK_OBSTACLE) | BIT_MASK_OBSTACLE_DESTROYED
    game_state.has_skill = False
    
    return True


SKILL_DESTROY_OBSTACLE = SKILLS[SKILL_ID_DESTROY_OBSTACLE] = Skill(
    SKILL_ID_DESTROY_OBSTACLE,
    skill_can_activate,
    skill_get_directions,
    skill_use,
)
