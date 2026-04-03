__all__ = ('QuestRewardSerialisableCredibility',)

from scarletio import copy_docs

from ..quest_reward_types import QUEST_REWARD_TYPE_CREDIBILITY

from .base import QuestRewardSerialisableBase


class QuestRewardSerialisableCredibility(QuestRewardSerialisableBase):
    """
    Represents reward credibility.
    
    Attributes
    ----------
    credibility : `int`
        The amount of credibility given by the quest.
    """
    TYPE = QUEST_REWARD_TYPE_CREDIBILITY
    
    __slots__ = ('credibility',)
    
    def __new__(cls, credibility):
        """
        Creates a new reward credibility.
        
        Parameters
        ----------
        credibility : `int`
            The amount of credibility given by the quest.
        """
        self = object.__new__(cls)
        self.credibility = credibility
        return self
    
    
    @copy_docs(QuestRewardSerialisableBase._produce_representation_middle)
    def _produce_representation_middle(self):
        # credibility
        yield ' credibility = '
        yield repr(self.credibility)
   
   
    @copy_docs(QuestRewardSerialisableBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        # credibility
        if self.credibility != other.credibility:
            return False
        
        return True
   
   
    @classmethod
    @copy_docs(QuestRewardSerialisableBase.deserialise)
    def deserialise(cls, data, start_index):
        end_index = start_index + 8
        
        if len(data) < end_index:
            return None
        
        self = object.__new__(cls)
        self.credibility = int.from_bytes(data[start_index : end_index], 'little')
        
        return self, end_index
   
   
    @copy_docs(QuestRewardSerialisableBase.serialise)
    def serialise(self):
        yield self.credibility.to_bytes(8, 'little')
