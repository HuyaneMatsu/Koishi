__all__ = ('Stage',)

from scarletio import RichAttributeErrorBaseType, include

from ..constants import CHAPTERS, STAGES

from .constants import (
    JSON_KEY_STAGE_BEST, JSON_KEY_STAGE_DIFFICULTY_ID, JSON_KEY_STAGE_ID, JSON_KEY_STAGE_IN_DIFFICULTY_INDEX,
    JSON_KEY_STAGE_MAP, JSON_KEY_STAGE_NEXT_STAGE_ID, JSON_KEY_STAGE_PREVIOUS_STAGE_ID, JSON_KEY_STAGE_SIZE_X,
    JSON_KEY_STAGE_START_POSITION, JSON_KEY_STAGE_TARGET_COUNT, TILE_NAME_TO_VALUE, TILE_VALUE_DEFAULT
)


CHAPTER_DEFAULT = include('CHAPTER_DEFAULT')
STAGE_DEFAULT = include('STAGE_DEFAULT')


class Stage(RichAttributeErrorBaseType):
    """
    A stage's source.
    
    Attributes
    ----------
    best : `int`
        The lowest amount of steps needed to solve the stage.
    
    chapter_id . `int`
        The chapter's identifier.
    
    difficulty_id : `int`
        The index of the stage's difficulty inside of it's chapter.
    
    id : `int`
        The identifier of the stage.
    
    in_difficulty_index : `int`
        The stage's index inside of it's difficulty.
    
    map : `list<int>`
        The stage's map.
    
    next_stage_id : `int`
        The next stage's identifier.
    
    previous_stage_id : `int`
        The previous stage's identifier
    
    size_x : `int`
        The map's size on the x axis.
    
    start_position : `int`
        The position, where the character starts on the stage.
    
    target_count : `int`
        The amount of targets on the map to fulfill.
    """
    __slots__ = (
        'best', 'chapter_id', 'difficulty_id', 'id', 'in_difficulty_index', 'map', 'next_stage_id',
        'previous_stage_id', 'size_x', 'start_position', 'target_count'
    )
    
    def __new__(
        cls,
        
        chapter_id,
        stage_id,
        
        difficulty_id,
        in_difficulty_index,
        next_stage_id,
        previous_stage_id,
        
        best,
        map_,
        size_x,
        start_position,
        target_count,
    ):
        """
        Creates a stage with the given fields.
        
        Parameters
        ----------
        chapter_id . `int`
            The chapter's identifier.
        
        stage_id : `int`
            The identifier of the stage.
        
    
        difficulty_id : `int`
            The index of the stage's difficulty inside of it's chapter.
        
        in_difficulty_index : `int`
            The stage's index inside of it's difficulty.
        
        next_stage_id : `int`
            The next stage's identifier.
        
        previous_stage_id : `int`
            The previous stage's identifier
        
        
        best : `int`
            The lowest amount of steps needed to solve the stage.
        
        map_ : `list<int>`
            The stage's map.
        
        size_x : `int`
            The map's size on the x axis.
        
        start_position : `int`
            The position, where the character starts on the stage.
        
        target_count : `int`
            The amount of targets on the map to fulfill.
        """
        self = object.__new__(cls)
        
        self.chapter_id = chapter_id
        self.id = stage_id
        
        self.difficulty_id = difficulty_id
        self.in_difficulty_index = in_difficulty_index
        self.next_stage_id = next_stage_id
        self.previous_stage_id = previous_stage_id
        
        self.best = best
        self.map = map_
        self.size_x = size_x
        self.start_position = start_position
        self.target_count = target_count
        
        return self
    
    
    @classmethod
    def from_data(cls, chapter_id, data):
        """
        Creates a stage from the given data.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Decoded json data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.best = data[JSON_KEY_STAGE_BEST]
        self.chapter_id = chapter_id
        self.difficulty_id = data[JSON_KEY_STAGE_DIFFICULTY_ID]
        self.id = data[JSON_KEY_STAGE_ID]
        self.in_difficulty_index = data[JSON_KEY_STAGE_IN_DIFFICULTY_INDEX]
        self.map = [
            TILE_NAME_TO_VALUE.get(tile_name, TILE_VALUE_DEFAULT) for tile_name in data[JSON_KEY_STAGE_MAP]
        ]
        self.next_stage_id = data[JSON_KEY_STAGE_NEXT_STAGE_ID]
        self.previous_stage_id = data[JSON_KEY_STAGE_PREVIOUS_STAGE_ID]
        self.size_x = data[JSON_KEY_STAGE_SIZE_X]
        self.start_position = data[JSON_KEY_STAGE_START_POSITION]
        self.target_count = data[JSON_KEY_STAGE_TARGET_COUNT]
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # id
        repr_parts.append(' id = ')
        repr_parts.append(str(self.id))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def get_chapter(self):
        """
        Returns the stage source's chapter.
        
        Returns
        -------
        chapter : ``Chapter``
        """
        return CHAPTERS.get(self.chapter_id, CHAPTER_DEFAULT)
    
    
    def get_previous_stage(self):
        """
        Returns the previous stage.
        
        Returns
        -------
        stage : ``None | Stage``
        """
        previous_stage_id = self.previous_stage_id
        if previous_stage_id:
            return STAGES.get(previous_stage_id, STAGE_DEFAULT)
    
    
    def get_next_stage(self):
        """
        Returns the next stage.
        
        Returns
        -------
        stage : ``None | Stage``
        """
        next_stage_id = self.next_stage_id
        if next_stage_id:
            return STAGES.get(next_stage_id, STAGE_DEFAULT)
