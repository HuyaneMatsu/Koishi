__all__ = ('QuestRewardInstantiableBalance',)

from scarletio import copy_docs

from ..quest_reward_serialisables import QuestRewardSerialisableBalance
from ..quest_reward_types import QUEST_REWARD_TYPE_BALANCE

from .base import QuestRewardInstantiableBase


class QuestRewardInstantiableBalance(QuestRewardInstantiableBase):
    """
    Represents an quest reward balance.
    
    Attributes
    ----------
    balance : `int`
        The amount of balance rewarded.
    """
    TYPE = QUEST_REWARD_TYPE_BALANCE
   
    __slots__ = ('balance',)
   
    def __new__(cls, balance):
        """
        Creates a new quest reward balance.
        
        Parameters
        ----------
        balance : `int`
            The amount of balance rewarded.
        """
        self = object.__new__(cls)
        self.balance = balance
        return self
   
   
    @copy_docs(QuestRewardInstantiableBase._produce_representation_middle)
    def _produce_representation_middle(self):
        # balance
        yield ' balance = '
        yield repr(self.balance)
    
    
    @copy_docs(QuestRewardInstantiableBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        # balance
        if self.balance != other.balance:
            return False
        
        return True
    
    
    @copy_docs(QuestRewardInstantiableBase.instantiate)
    def instantiate(self):
        return QuestRewardSerialisableBalance(
            self.balance,
        )
