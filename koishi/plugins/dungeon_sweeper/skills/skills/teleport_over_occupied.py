__all__ = ('SKILL_TELEPORT_OVER_OCCUPIED',)

from ...constants import SKILLS
from ...move_directions import DIRECTIONS_MAIN, MoveDirections
from ...tile_bit_masks import BIT_MASK_ALIGN_ALL, BIT_MASK_CHARACTER, BIT_MASK_OCCUPIED, BIT_MASK_PASSABLE
from ...user_state import HistoryElement

from ..constants import SKILL_ID_TELEPORT_OVER_OCCUPIED
from ..skill import Skill


def skill_can_activate(game_state):
    """
    Returns whether Yukari skill can be activated.
    
    Parameters
    ----------
    game_state : ``GameState``
        The respective game state.
    
    Returns
    -------
    can_active : `bool`
    """
    map_ = game_state.map
    
    size_x = game_state.stage.size_x
    y_size = len(map_) // size_x

    position = game_state.position
    y_position, x_position = divmod(position, size_x)
    
    for step, limit in (
        (-size_x , -size_x + x_position                ,),
        (1       , size_x * (y_position + 1) - 1       ,),
        (size_x  , x_position + (size_x * (y_size - 1)),),
        ( -1     , size_x * y_position                 ,),
    ):
        target_position = position + step
        if target_position == limit:
            continue
        
        target_tile = map_[target_position]
        if not (target_tile & BIT_MASK_OCCUPIED):
            continue
        
        while True:
            target_position = target_position + step
            if target_position == limit:
                break
            
            target_tile = map_[target_position]
            if target_tile & BIT_MASK_OCCUPIED:
                continue
            
            if (target_tile & BIT_MASK_PASSABLE) == target_tile:
                return True
            
            break
    
    return False


def skill_get_directions(game_state):
    """
    Returns to which directions Yukari's skill could be used.
    
    Parameters
    ----------
    game_state : ``GameState``
        The respective game state.
    
    Returns
    -------
    move_directions : ``MoveDirections``
    """
    map_ = game_state.map
    
    size_x = game_state.stage.size_x
    y_size = len(map_) // size_x
    
    move_directions = MoveDirections()
    
    position = game_state.position
    y_position, x_position = divmod(position, size_x)
    
    for (step, limit), direction in zip(
        (
            ( -size_x , -size_x + x_position                ,),
            (1        , size_x * (y_position + 1) - 1       ,),
            (size_x   , x_position + (size_x * (y_size - 1)),),
            ( -1      , size_x * y_position                 ,),
        ),
        DIRECTIONS_MAIN,
    ):
        
        target_position = position + step
        if target_position == limit:
            can_go_to_direction = False
        
        else:
            target_tile = map_[target_position]
            if not (target_tile & BIT_MASK_OCCUPIED):
                can_go_to_direction = False
            
            else:
                while True:
                    target_position = target_position + step
                    if target_position == limit:
                        can_go_to_direction = False
                        break
                    
                    target_tile = map_[target_position]
                    if (target_tile & BIT_MASK_OCCUPIED):
                        continue
                    
                    if (target_tile & BIT_MASK_PASSABLE) == target_tile:
                        can_go_to_direction = True
                        break
                    
                    can_go_to_direction = False
                    break
        
        move_directions.set(direction, can_go_to_direction)
    
    return move_directions


def skill_use(game_state, step, align):
    """
    Uses Yukari's skill to the represented directory.
    
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

    size_x = game_state.stage.size_x
    y_size = len(map_) // size_x
    
    position = game_state.position
    y_position, x_position = divmod(position, size_x)

    if step > 0:
        if step == 1:
            limit = size_x * (y_position + 1) - 1
        else:
            limit = x_position + (size_x * (y_size - 1))
    else:
        if step == -1:
            limit = size_x * y_position
        else:
            limit = -size_x + x_position

    target_position = position + step
    
    if target_position == limit:
        return False
    
    target_tile = map_[target_position]
    if not (target_tile & BIT_MASK_OCCUPIED):
        return False
    
    while True:
        target_position = target_position + step
        if target_position == limit:
            return False
        
        target_tile = map_[target_position]
        if target_tile & BIT_MASK_OCCUPIED:
            continue
        
        if (target_tile & BIT_MASK_PASSABLE) == target_tile:
            break
        
        return False
    
    actual_tile = map_[position]
    game_state.history.append(
        HistoryElement(
            position,
            True,
            (
                (position, actual_tile),
                (target_position, target_tile),
            ),
        ),
    )
    
    map_[position] = actual_tile &~ (BIT_MASK_CHARACTER | BIT_MASK_ALIGN_ALL)
    game_state.position = target_position
    
    map_[target_position] = target_tile | BIT_MASK_CHARACTER | align
    game_state.has_skill = False
    
    return True


SKILL_TELEPORT_OVER_OCCUPIED = SKILLS[SKILL_ID_TELEPORT_OVER_OCCUPIED] = Skill(
    SKILL_ID_TELEPORT_OVER_OCCUPIED,
    skill_can_activate,
    skill_get_directions,
    skill_use,
)
