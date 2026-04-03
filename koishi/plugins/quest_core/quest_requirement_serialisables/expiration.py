__all__ = ('QuestRequirementSerialisableExpiration',)

from datetime import datetime as DateTime, timezone as TimeZone

from scarletio import copy_docs
from hata import DATETIME_FORMAT_CODE

from ..quest_requirement_types import QUEST_REQUIREMENT_TYPE_EXPIRATION

from .base import QuestRequirementSerialisableBase


class QuestRequirementSerialisableExpiration(QuestRequirementSerialisableBase):
    """
    Represents an expiration.
    
    Attributes
    ----------
    expiration : `DateTime`
        When the quest expires.
    """
    TYPE = QUEST_REQUIREMENT_TYPE_EXPIRATION
    
    __slots__ = ('expiration',)
    
    def __new__(cls, expiration):
        """
        Creates a new quest requirement expiration.
        
        Parameters
        ----------
        expiration : `DateTime`
            When the quest expires.
        """
        self = object.__new__(cls)
        self.expiration = expiration
        return self
    
    
    @copy_docs(QuestRequirementSerialisableBase._produce_representation_middle)
    def _produce_representation_middle(self):
        # expiration
        yield ' expiration = '
        yield format(self.expiration, DATETIME_FORMAT_CODE)
   
   
    @copy_docs(QuestRequirementSerialisableBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        # expiration
        if self.expiration != other.expiration:
            return False
        
        return True
   
   
    @classmethod
    @copy_docs(QuestRequirementSerialisableBase.deserialise)
    def deserialise(cls, data, start_index):
        end_index = start_index + 8
        
        if len(data) < end_index:
            return None
        
        self = object.__new__(cls)
        self.expiration = DateTime.fromtimestamp(
            int.from_bytes(data[start_index : end_index], 'little'),
            tz = TimeZone.utc,
        )
        
        return self, end_index
   
   
    @copy_docs(QuestRequirementSerialisableBase.serialise)
    def serialise(self):
        yield int(self.expiration.timestamp()).to_bytes(8, 'little')
