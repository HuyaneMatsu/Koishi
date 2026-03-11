__all__ = ('QuestRequirementInstantiableDuration',)

from scarletio import copy_docs

from ..quest_requirement_serialisables import QuestRequirementSerialisableDuration
from ..quest_requirement_types import QUEST_REQUIREMENT_TYPE_DURATION

from .base import QuestRequirementInstantiableBase


class QuestRequirementInstantiableDuration(QuestRequirementInstantiableBase):
    """
    Represents an expiration duration.
    
    Attributes
    ----------
    duration : `int`
        After how much seconds the quest expires.
    """
    TYPE = QUEST_REQUIREMENT_TYPE_DURATION
   
    __slots__ = ('duration',)
   
    def __new__(cls, duration):
        """
        Creates a new expiration requirement.
        
        Parameters
        ----------
        duration : `int`
            After how much seconds the quest expires.
        """
        self = object.__new__(cls)
        self.duration = duration
        return self
   
   
    @copy_docs(QuestRequirementInstantiableBase._produce_representation_middle)
    def _produce_representation_middle(self):
        # duration
        yield ' duration = '
        yield repr(self.duration)
    
    
    @copy_docs(QuestRequirementInstantiableBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        # duration
        if self.duration != other.duration:
            return False
        
        return True
    
    
    @copy_docs(QuestRequirementInstantiableBase.instantiate)
    def instantiate(self):
        return QuestRequirementSerialisableDuration(
            self.duration,
        )
