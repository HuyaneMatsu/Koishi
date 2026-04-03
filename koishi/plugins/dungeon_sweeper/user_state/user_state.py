__all__ = ('UserState', 'get_first_stage_id')

from zlib import compress, decompress

from scarletio import RichAttributeErrorBaseType, from_json, include, to_json

from ..constants import CHAPTERS, STAGES

from .game_state import GameState
from .stage_result import StageResult


CHAPTER_DEFAULT = include('CHAPTER_DEFAULT')
STAGE_DEFAULT = include('STAGE_DEFAULT')


def get_first_stage_id():
    """
    Returns the first stage's identifier.
    
    Returns
    -------
    stage_id : `int`
    """
    for chapter in CHAPTERS.values():
        if (chapter is not CHAPTER_DEFAULT) and (not chapter.unlock_prerequisite_stage_id):
            return chapter.first_stage_id
    
    return CHAPTER_DEFAULT.first_stage_id


class UserState(RichAttributeErrorBaseType):
    """
    A user's state in dungeon sweeper.
    
    Attributes
    ----------
    entry_id : `int`
        The field identifier in the database.
    
    game_state : ``None | GameState``
        The state of the actual game.
    
    selected_stage_id : `int`
        The selected stage's identifier.
    
    stage_results: ``dict<int, StageResult>``
        Result of each completed stage by the user.
    
    user_id : `int`
        The respective user's identifier.
    """
    __slots__ = ('entry_id', 'game_state', 'selected_stage_id', 'stage_results', 'user_id')
    
    def __new__(cls, user_id):
        """
        Creates a new user state based on he given `user_id`.
        
        Parameters
        ----------
        user_id : `int`
            The user' respective identifier.
        """
        self = object.__new__(cls)
        self.game_state = None
        self.selected_stage_id = 0
        self.entry_id = 0
        self.stage_results = {}
        self.user_id = user_id
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # user_id
        repr_parts.append(' user_id = ')
        repr_parts.append(repr(self.user_id))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @classmethod
    def from_entry(cls, ds_entry, ds_result_entries):
        """
        Creates a new user state from the given entry.
        
        Parameters
        ----------
        ds_entry : `sqlalchemy.engine.result.RowProxy`
            The user's entry.
        
        ds_result_entries : `list<sqlalchemy.engine.result.RowProxy>`
            The user's results.
        
        Returns
        -------
        self : `instance<cls>`
        """
        game_state_data = ds_entry['game_state']
        if (game_state_data is None):
            game_state = None
        else:
            game_state = GameState.from_data(from_json(decompress(game_state_data)))
        
        stage_results = {}
        for ds_result_entry in ds_result_entries:
            stage_result = StageResult.from_entry(ds_result_entry)
            stage_results[stage_result.stage_id] = stage_result
        
        self = object.__new__(cls)
        self.game_state = game_state
        self.selected_stage_id = ds_entry['selected_stage_id']
        self.entry_id = ds_entry['id']
        self.stage_results = stage_results
        self.user_id = ds_entry['user_id']
        return self
    
    
    def get_game_state_data(self):
        """
        Gets the user state's game state's data in json serializable from.
        
        Returns
        -------
        game_state_data : `None | bytes`
        """
        game_state = self.game_state
        if (game_state is None) or (not game_state.can_back_or_restart()):
            game_state_data = None
        else:
            game_state_data = compress(to_json(game_state.to_data()).encode())
        
        return game_state_data
    
    
    def get_selected_stage(self):
        """
        Gets the selected stage of the user. If the user's selected stage is invalid returns them to stage 0.
        
        Returns
        -------
        stage : ``Stage``
        
        Raises
        ------
        RuntimeError
            - If no first stage could be detected.
        """
        selected_stage_id = self.selected_stage_id
        if selected_stage_id:
            try:
                stage = STAGES[selected_stage_id]
            except KeyError:
                pass
            else:
                return stage
        
        selected_stage_id = get_first_stage_id()
        if selected_stage_id:
            try:
                stage = STAGES[selected_stage_id]
            except KeyError:
                pass
            else:
                self.selected_stage_id = selected_stage_id
                return stage
        
        return STAGE_DEFAULT
