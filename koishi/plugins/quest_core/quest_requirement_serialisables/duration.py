__all__ = ('QuestRequirementSerialisableDuration',)

from scarletio import copy_docs

from ..quest_requirement_types import QUEST_REQUIREMENT_TYPE_DURATION

from .base import QuestRequirementSerialisableBase


class QuestRequirementSerialisableDuration(QuestRequirementSerialisableBase):
    """
    Represents the duration until the quest expires.
    
    Attributes
    ----------
    duration : `int`
        The duration in seconds until the quest expires.
    """
    TYPE = QUEST_REQUIREMENT_TYPE_DURATION
    
    __slots__ = ('duration',)
    
    def __new__(cls, duration):
        """
        Creates a new quest duration requirement.
        
        Parameters
        ----------
        duration : `int`
            The duration in seconds until the quest expires.
        """
        self = object.__new__(cls)
        self.duration = duration
        return self
    
    
    @copy_docs(QuestRequirementSerialisableBase._produce_representation_middle)
    def _produce_representation_middle(self):
        # duration
        yield ' duration = '
        yield repr(self.duration)
   
   
    @copy_docs(QuestRequirementSerialisableBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        # duration
        if self.duration != other.duration:
            return False
        
        return True
   
   
    @classmethod
    @copy_docs(QuestRequirementSerialisableBase.deserialise)
    def deserialise(cls, data, start_index):
        end_index = start_index + 8
        
        if len(data) < end_index:
            return None
        
        self = object.__new__(cls)
        self.duration = int.from_bytes(data[start_index : end_index], 'little')
        
        return self, end_index
   
   
    @copy_docs(QuestRequirementSerialisableBase.serialise)
    def serialise(self):
        yield self.duration.to_bytes(8, 'little')
