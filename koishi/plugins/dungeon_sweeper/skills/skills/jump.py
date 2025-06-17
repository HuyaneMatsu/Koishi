__all__ = ('SKILL_JUMP',)

from ...constants import SKILLS
from ...move_directions import DIRECTIONS_MAIN, MoveDirections
from ...tile_bit_masks import BIT_MASK_ALIGN_ALL, BIT_MASK_CHARACTER, BIT_MASK_JUMPABLE, BIT_MASK_PASSABLE
from ...user_state import HistoryElement

from ..constants import SKILL_ID_JUMP
from ..skill import Skill


def skill_can_activate(game_state):
    """
    Returns whether Reimu skill can be activated.
    
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
        
        if not (target_tile & BIT_MASK_JUMPABLE):
            continue
        
        after_tile = map_[position + (step << 1)]
        
        if (after_tile & BIT_MASK_PASSABLE) != after_tile:
            continue
        
        return True
    
    return False


def skill_get_directions(game_state):
    """
    Returns to which directions Reimu's skill could be used.
    
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
        
        if not (target_tile & BIT_MASK_JUMPABLE):
            can_go_to_direction = False
        
        else:
            after_tile = map_[position + (step << 1)]
    
            if (after_tile & BIT_MASK_PASSABLE) == after_tile:
                can_go_to_direction = True
            else:
                can_go_to_direction = False
        
        move_directions.set(direction, can_go_to_direction)
    
    return move_directions


def skill_use(game_state, step, align):
    """
    Uses Reimu's skill to the represented directory.
    
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
    
    if not (target_tile & BIT_MASK_JUMPABLE):
        return False
    
    after_tile = map_[position + (step << 1)]
    
    if (after_tile & BIT_MASK_PASSABLE) != after_tile:
        return False
    
    actual_tile = map_[position]
    game_state.history.append(
        HistoryElement(
            position,
            True,
            (
                (position, actual_tile),
                (position + (step << 1), after_tile),
            ),
        ),
    )
    
    map_[position] = actual_tile &~ (BIT_MASK_CHARACTER | BIT_MASK_ALIGN_ALL)
    game_state.position = position = position + (step << 1)
    
    map_[position] = after_tile | BIT_MASK_CHARACTER | align
    game_state.has_skill = False
    
    return True


SKILL_JUMP = SKILLS[SKILL_ID_JUMP] = Skill(
    SKILL_ID_JUMP,
    skill_can_activate,
    skill_get_directions,
    skill_use,
)
