__all__ = ('SKILL_DEFAULT',)

from ...constants import SKILLS
from ...move_directions import MoveDirections

from ..constants import SKILL_ID_DEFAULT
from ..skill import Skill


def skill_can_activate(game_state):
    """
    Returns that the skill cannot be activated.
    
    Parameters
    ----------
    game_state : ``GameState``
        The respective game state.
    
    Returns
    -------
    can_active : `bool`
    """
    return False


def skill_get_directions(game_state):
    """
    Returns no directions.
    
    Parameters
    ----------
    game_state : ``GameState``
        The respective game state.
    
    Returns
    -------
    move_directions : ``MoveDirections``
    """
    return MoveDirections()


def skill_use(game_state, step, align):
    """
    Does nothing.
    
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
    return False


SKILL_DEFAULT = SKILLS[SKILL_ID_DEFAULT] = Skill(
    SKILL_ID_DEFAULT,
    skill_can_activate,
    skill_get_directions,
    skill_use,
)
