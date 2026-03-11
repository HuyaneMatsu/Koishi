__all__ = ('QuestRewardGeneratorCredibility',)

from scarletio import copy_docs

from ..quest_reward_instantiables import QuestRewardInstantiableCredibility
from ..quest_reward_types import QUEST_REWARD_TYPE_CREDIBILITY

from .base import QuestRewardGeneratorBase


class QuestRewardGeneratorCredibility(QuestRewardGeneratorBase):
    """
    Represents a quest reward generator with credibility.
    
    Attributes
    ----------
    credibility_base : `int`
        The credibility given by the quest.
    """
    TYPE = QUEST_REWARD_TYPE_CREDIBILITY
    
    __slots__ = ('credibility_base', )
    
    def __new__(
        cls,
        credibility_base,
    ):
        """
        Creates a new credibility reward generator.
        
        Parameters
        ----------
        credibility_base : `int`
            The credibility given by the quest.
        """
        self = object.__new__(cls)
        self.credibility_base = credibility_base
        return self
    
    
    @copy_docs(QuestRewardGeneratorBase._produce_representation_middle)
    def _produce_representation_middle(self):
        # credibility_base
        yield ' credibility_base = '
        yield repr(self.credibility_base)
    
    
    @copy_docs(QuestRewardGeneratorBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        # credibility_base
        if self.credibility_base != other.credibility_base:
            return False
        
        return True
    
    
    @copy_docs(QuestRewardGeneratorBase.generate_with_diversion)
    def generate_with_diversion(self, random_number_generator, accumulated_diversion):
        credibility = round(self.credibility_base * accumulated_diversion)
        
        return (
            QuestRewardInstantiableCredibility(credibility),
            1.0,
        )
