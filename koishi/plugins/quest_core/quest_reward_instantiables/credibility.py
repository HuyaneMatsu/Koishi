__all__ = ('QuestRewardInstantiableCredibility',)

from scarletio import copy_docs

from ..quest_reward_serialisables import QuestRewardSerialisableCredibility
from ..quest_reward_types import QUEST_REWARD_TYPE_CREDIBILITY

from .base import QuestRewardInstantiableBase


class QuestRewardInstantiableCredibility(QuestRewardInstantiableBase):
    """
    Represents an quest reward credibility.
    
    Attributes
    ----------
    credibility : `int`
        The amount of credibility rewarded.
    """
    TYPE = QUEST_REWARD_TYPE_CREDIBILITY
   
    __slots__ = ('credibility',)
   
    def __new__(cls, credibility):
        """
        Creates a new quest reward credibility.
        
        Parameters
        ----------
        credibility : `int`
            The amount of credibility rewarded.
        """
        self = object.__new__(cls)
        self.credibility = credibility
        return self
   
   
    @copy_docs(QuestRewardInstantiableBase._produce_representation_middle)
    def _produce_representation_middle(self):
        # credibility
        yield ' credibility = '
        yield repr(self.credibility)
    
    
    @copy_docs(QuestRewardInstantiableBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        # credibility
        if self.credibility != other.credibility:
            return False
        
        return True
    
    
    @copy_docs(QuestRewardInstantiableBase.instantiate)
    def instantiate(self):
        return QuestRewardSerialisableCredibility(
            self.credibility,
        )
