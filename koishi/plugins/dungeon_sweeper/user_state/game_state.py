__all__ = ('GameState',)

from scarletio import RichAttributeErrorBaseType, include

from ..constants import STAGES
from ..move_directions import DIRECTIONS_MAIN, DIRECTION_DIAGONAL, MoveDirections
from ..tile_bit_masks import (
    BIT_FLAG_EAST, BIT_FLAG_NORTH, BIT_FLAG_SOUTH, BIT_FLAG_WEST, BIT_MASK_ALIGN_ALL, BIT_MASK_BOX_ON_TARGET,
    BIT_MASK_CHARACTER, BIT_MASK_HOLE_FILLED, BIT_MASK_OCCUPIED, BIT_MASK_PASSABLE, BIT_MASK_PUSHABLE,
    BIT_MASK_UNPUSHABLE
)

from .history_element import HistoryElement


STAGE_DEFAULT = include('STAGE_DEFAULT')


DIRECTION_MOVE_STATE_NONE = 0
DIRECTION_MOVE_STATE_CAN  = 1
DIRECTION_MOVE_STATE_PUSH = 2
DIRECTION_MOVE_STATE_DIAGONAL_0 = 3
DIRECTION_MOVE_STATE_DIAGONAL_1 = 4


JSON_KEY_GAME_STATE_STAGE_ID = '0'
JSON_KEY_GAME_STATE_MAP = '1'
JSON_KEY_GAME_STATE_POSITION = '2'
JSON_KEY_GAME_STATE_HAS_SKILL = '3'
JSON_KEY_GAME_STATE_NEXT_SKILL = '4'
JSON_KEY_GAME_STATE_HISTORY = '5'
JSON_KEY_GAME_STATE_STAGE_BEST = '6'


def can_move_to(map_, position, step):
    """
    Returns whether the player can move to the given direction.
    
    Parameters
    ----------
    map_ : `list<int>`
        The map where the player is.
    
    position : `int`
        The player's position on the map.
    
    step : `int`
        The step to do.
    
    Returns
    -------
    move_state : `int`
        Whether the player can move.
        
        Can be any of the following values:
        
        +---------------------------+-------+
        | Respective name           | Value |
        +===========================+=======+
        | DIRECTION_MOVE_STATE_NONE | 0     |
        +---------------------------+-------+
        | DIRECTION_MOVE_STATE_CAN  | 1     |
        +---------------------------+-------+
        | DIRECTION_MOVE_STATE_PUSH | 2     |
        +---------------------------+-------+
    """
    target_tile = map_[position + step]
    
    if target_tile & BIT_MASK_UNPUSHABLE:
        move_state = DIRECTION_MOVE_STATE_NONE
    
    elif (target_tile & BIT_MASK_PASSABLE) == target_tile:
        move_state = DIRECTION_MOVE_STATE_CAN
    
    elif not (target_tile & BIT_MASK_PUSHABLE):
        move_state = DIRECTION_MOVE_STATE_NONE
    
    else:
        after_tile = map_[position + (step << 1)]
        if after_tile & BIT_MASK_OCCUPIED:
            move_state = DIRECTION_MOVE_STATE_NONE
        
        else:
            move_state = DIRECTION_MOVE_STATE_PUSH
    
    return move_state


def can_move_to_diagonal(map_, position, step_0, step_1):
    """
    Returns whether the player can move diagonally.
    
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
    move_state : `int`
        Whether the player can move diagonally.
        
        Can be any of the following values:
        
        +-----------------------------------+-------+
        | Respective name                   | Value |
        +===================================+=======+
        | DIRECTION_MOVE_STATE_NONE         | 0     |
        +-----------------------------------+-------+
        | DIRECTION_MOVE_STATE_DIAGONAL_0   | 3     |
        +-----------------------------------+-------+
        | DIRECTION_MOVE_STATE_DIAGONAL_1   | 4     |
        +-----------------------------------+-------+
    """
    step_0_1_state = can_move_to(map_, position, step_0)
    if step_0_1_state == DIRECTION_MOVE_STATE_NONE:
        step_0_2_state = DIRECTION_MOVE_STATE_NONE
    else:
        step_0_2_state = can_move_to(map_, position + step_0, step_1)
    
    step_1_1_state = can_move_to(map_, position, step_1)
    if step_1_1_state == DIRECTION_MOVE_STATE_NONE:
        step_1_2_state = DIRECTION_MOVE_STATE_NONE
    else:
        step_1_2_state = can_move_to(map_, position + step_1, step_0)
    
    
    if (
        (step_0_1_state == DIRECTION_MOVE_STATE_CAN) and
        (step_0_2_state == DIRECTION_MOVE_STATE_CAN)
    ):
        move_state = DIRECTION_MOVE_STATE_DIAGONAL_0
    
    elif (
        (step_1_1_state == DIRECTION_MOVE_STATE_CAN) and
        (step_1_2_state == DIRECTION_MOVE_STATE_CAN)
    ):
        move_state = DIRECTION_MOVE_STATE_DIAGONAL_1
    
    elif (
        (
            (step_1_1_state == DIRECTION_MOVE_STATE_NONE) or
            (step_1_2_state == DIRECTION_MOVE_STATE_NONE)
        ) and
        (step_0_1_state != DIRECTION_MOVE_STATE_NONE) and
        (step_0_2_state != DIRECTION_MOVE_STATE_NONE)
    ):
        move_state = DIRECTION_MOVE_STATE_DIAGONAL_0
    
    elif (
        (
            (step_0_1_state == DIRECTION_MOVE_STATE_NONE) or
            (step_0_2_state == DIRECTION_MOVE_STATE_NONE)
        ) and
        (step_1_1_state != DIRECTION_MOVE_STATE_NONE) and
        (step_1_2_state != DIRECTION_MOVE_STATE_NONE)
    ):
        move_state = DIRECTION_MOVE_STATE_DIAGONAL_1
    
    else:
        move_state = DIRECTION_MOVE_STATE_NONE
    
    return move_state


def get_move_directions(game_state):
    """
    Returns to which directions can the character move, excluding the skill of the character.
    
    Parameters
    ----------
    game_state : ``GameState``
        Game state to get directions for.
    
    Returns
    -------
    move_directions : ``MoveDirections``
    """
    size_x = game_state.stage.size_x
    position = game_state.position
    map_ = game_state.map
    
    move_directions = MoveDirections()
    
    for step, direction in zip((-size_x, 1, size_x, -1), DIRECTIONS_MAIN):
        if can_move_to(map_, position, step) != DIRECTION_MOVE_STATE_NONE:
            move_directions.set(direction, True)
    
    for steps, directions in zip(
        ((-size_x, 1), (1, size_x), (size_x, -1), (-1, -size_x),), DIRECTION_DIAGONAL
    ):
        move_state = can_move_to_diagonal(map_, position, *steps)
        if move_state != DIRECTION_MOVE_STATE_NONE:
            move_directions.set(directions[move_state == DIRECTION_MOVE_STATE_DIAGONAL_1], True)
    
    return move_directions


class GameState(RichAttributeErrorBaseType):
    """
    A user's actual game's state.
    
    Attributes
    ----------
    best : `int`
        The user's best solution for the stage. Set as `-1` by default.
    
    chapter : ``Chapter``
        The stage's chapter.
    
    has_skill : `bool`
        Whether the character' skill in the game was not yet used.
    
    history : ``list<HistoryElement>``
        The done steps in the game.
    
    map : `list<int>`
        The game's actual map.
    
    next_skill : `bool`
        Whether the next step is a skill usage.
    
    position : `int`
        The position of the selected stage.
    
    skill : ``Skill``
        The skill to be used on the selected stage,
    
    stage : ``Stage``
        The represented stage.
    """
    __slots__ = ('best', 'chapter', 'has_skill', 'history', 'map', 'next_skill', 'position', 'skill', 'stage',)
    
    def __new__(cls, stage, best):
        """
        Creates a new game state instance from the given parameters.
        
        Parameters
        ----------
        stage : ``Stage``
            The stage to execute by the game.
        
        best : `int`
            The user's best solution for the stage.
        """
        chapter = stage.get_chapter()
        
        self = object.__new__(cls)
        self.best = best
        self.chapter = chapter
        self.has_skill = True
        self.history = []
        self.map = stage.map.copy()
        self.next_skill = False
        self.position = stage.start_position
        self.skill = chapter.get_skill()
        self.stage = stage
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # stage
        repr_parts.append(' stage = ')
        repr_parts.append(repr(self.stage))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates stage state from the given json data.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Json data.
        
        Returns
        -------
        self : ``GameState``
        """
        self = object.__new__(cls)
        
        stage_id = data[JSON_KEY_GAME_STATE_STAGE_ID]
        
        stage = STAGES.get(stage_id, STAGE_DEFAULT)
        chapter = stage.get_chapter()
        self.chapter = chapter
        self.skill = chapter.get_skill()
        self.stage = stage
        
        self.best = data.get(JSON_KEY_GAME_STATE_STAGE_BEST, -1)
        
        try:
            map_ = data[JSON_KEY_GAME_STATE_MAP]
        except KeyError:
            map_ = stage.map.copy()
        
        self.map = map_
        
        try:
            position = data[JSON_KEY_GAME_STATE_POSITION]
        except KeyError:
            position = stage.start_position
        
        self.position = position
        
        self.has_skill = data.get(JSON_KEY_GAME_STATE_HAS_SKILL, True)
        self.next_skill = data.get(JSON_KEY_GAME_STATE_NEXT_SKILL, True)
        
        try:
            history_datas = data[JSON_KEY_GAME_STATE_HISTORY]
        except KeyError:
            history = []
        else:
            history = [HistoryElement.from_data(history_data) for history_data in history_datas]
        
        self.history = history
        return self
    
    
    def to_data(self):
        """
        Converts the stage state to json serializable data.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        data = {}
        stage = self.stage
        
        data[JSON_KEY_GAME_STATE_STAGE_ID] = stage.id
        
        best = self.best
        if best != -1:
            data[JSON_KEY_GAME_STATE_STAGE_BEST] = best
        
        if not self.has_skill:
            data[JSON_KEY_GAME_STATE_HAS_SKILL] = False
        
        if not self.next_skill:
            data[JSON_KEY_GAME_STATE_NEXT_SKILL] = False
        
        history = self.history
        if history:
            data[JSON_KEY_GAME_STATE_HISTORY] = [history_element.to_data() for history_element in history]
            data[JSON_KEY_GAME_STATE_POSITION] = self.position
            data[JSON_KEY_GAME_STATE_MAP] = self.map.copy()
        
        return data
    
    
    def restart(self):
        """
        Restarts the game.
        
        Returns
        -------
        success : `bool`
            Whether the map was reset.
        """
        history = self.history
        if (not history) and (not self.next_skill):
            return False
        
        history.clear()
        
        self.map = self.stage.map.copy()
        self.position = self.stage.start_position
        self.has_skill = True
        self.next_skill = False
        return True
    
    
    def is_done(self):
        """
        Returns whether all the targets on the stage are satisfied.
        
        Returns
        -------
        done : `bool`
        """
        target_count = self.stage.target_count
        for tile in self.map:
            if (tile & BIT_MASK_BOX_ON_TARGET) == BIT_MASK_BOX_ON_TARGET:
                target_count -= 1
                
                if not target_count:
                    if (self.best == -1) or (self.best > len(self.history)):
                        self.best = len(self.history)
                    
                    return True
        
        return False
    
    
    def move_north(self):
        """
        Moves the character north.
        
        Returns
        -------
        moved : `bool`
            Whether the character move successfully.
        """
        return self.move(-self.stage.size_x, BIT_FLAG_NORTH)
    
    
    def move_east(self):
        """
        Moves the character east.
        
        Returns
        -------
        moved : `bool`
            Whether the character move successfully.
        """
        return self.move(1, BIT_FLAG_EAST)
    
    
    def move_south(self):
        """
        Moves the character south.
        
        Returns
        -------
        moved : `bool`
            Whether the character move successfully.
        """
        return self.move(self.stage.size_x, BIT_FLAG_SOUTH)
    
    
    def move_west(self):
        """
        Moves the character west.
        
        Returns
        -------
        moved : `bool`
            Whether the character move successfully.
        """
        return self.move(-1, BIT_FLAG_WEST)
    
    
    def get_directions(self):
        """
        Returns to which directions the character can move.
        
        Returns
        -------
        move_directions : ``MoveDirections``
        """
        if self.next_skill:
            return self.skill.get_directions(self)
        
        return get_move_directions(self)
    
    
    def move(self, step, align):
        """
        Moves the character to the given directory.
        
        Parameters
        ----------
        step : `int`
            Difference between 2 adjacent tile-s translated to 1 dimension based on the map's size.
        
        align : `int`
            The character's new align if the move is successful.
        
        Returns
        -------
        success : `bool`
            Whether the move was completed successfully.
        """
        if self.next_skill:
            result = self.skill.use(self, step, align)
            if result:
                self.next_skill = False
            
            return result
        
        map_ = self.map
        position = self.position
        
        actual_tile = map_[position]
        target_tile = map_[position + step]
        
        if target_tile & BIT_MASK_UNPUSHABLE:
            return False
        
        if (target_tile & BIT_MASK_PASSABLE) == target_tile:
            self.history.append(
                HistoryElement(
                    position,
                    False,
                    (
                        (position, actual_tile),
                        (position + step, target_tile),
                    ),
                )
            )
            
            map_[position] = actual_tile &~ (BIT_MASK_CHARACTER | BIT_MASK_ALIGN_ALL)
            self.position = position = position + step
            map_[position] = target_tile | BIT_MASK_CHARACTER | align
            
            return True
        
        if not (target_tile & BIT_MASK_PUSHABLE):
            return False
        
        after_tile = map_[position + (step << 1)]
        if after_tile & BIT_MASK_OCCUPIED:
            return False
        
        self.history.append(
            HistoryElement(
                position,
                False,
                (
                    (position, actual_tile),
                    (position + step, target_tile),
                    (position + (step << 1), after_tile),
                ),
            )
        )
        
        map_[position] = actual_tile &~ (BIT_MASK_CHARACTER | BIT_MASK_ALIGN_ALL)
        self.position = position = position + step
        pushed = target_tile & BIT_MASK_PUSHABLE
        map_[position] = (target_tile &~ BIT_MASK_PUSHABLE) | BIT_MASK_CHARACTER | align
        if after_tile & BIT_MASK_PASSABLE:
            map_[position + step] = after_tile | pushed
        else:
            # hole
            map_[position + step] = BIT_MASK_HOLE_FILLED
        
        return True
    
    
    def skill_can_activate(self):
        """
        Activates the character's skill if applicable.
        
        Returns
        -------
        success : `bool`
            Whether the skill was activated.
        """
        if not self.has_skill:
            return False
        
        if not self.skill.can_activate(self):
            return False
        
        return True
    
    
    def skill_activate(self):
        """
        Activates (or deactivates) the character's skill.
        
        Returns
        -------
        success : `bool`
            Whether the skill could be (de)activated.
        """
        if not self.has_skill:
            return False
        
        if self.next_skill:
            self.next_skill = False
            return True
        
        if self.skill.can_activate(self):
            self.next_skill = True
            return True
        
        return False
    
    
    def can_back_or_restart(self):
        """
        Returns whether the character can go back, or resetting the game is available.
        
        Returns
        -------
        can_back_or_restart : `bool`
        """
        if self.history:
            return True
        
        if self.next_skill:
            return True
        
        return False
    
    
    def back(self):
        """
        Goes back one step.
        
        Returns
        -------
        success : `bool`
            Whether the character could go back one step.
        """
        if self.next_skill:
            self.next_skill = False
            return True
        
        history = self.history
        if not history:
            return False
        
        element = history.pop(-1)
        map_ = self.map
        self.position = element.position
        
        for position, value in element.changes:
            map_[position] = value
        
        if element.was_skill:
            self.has_skill = True
        
        return True
