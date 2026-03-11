__all__ = ('QuestRewardSerialisableBalance',)

from scarletio import copy_docs

from ..quest_reward_types import QUEST_REWARD_TYPE_BALANCE

from .base import QuestRewardSerialisableBase


class QuestRewardSerialisableBalance(QuestRewardSerialisableBase):
    """
    Represents reward balance.
    
    Attributes
    ----------
    balance : `int`
        The amount of balance given by the quest.
    """
    TYPE = QUEST_REWARD_TYPE_BALANCE
    
    __slots__ = ('balance',)
    
    def __new__(cls, balance):
        """
        Creates a new reward balance.
        
        Parameters
        ----------
        balance : `int`
            The amount of balance given by the quest.
        """
        self = object.__new__(cls)
        self.balance = balance
        return self
    
    
    @copy_docs(QuestRewardSerialisableBase._produce_representation_middle)
    def _produce_representation_middle(self):
        # balance
        yield ' balance = '
        yield repr(self.balance)
   
   
    @copy_docs(QuestRewardSerialisableBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        # balance
        if self.balance != other.balance:
            return False
        
        return True
   
   
    @classmethod
    @copy_docs(QuestRewardSerialisableBase.deserialise)
    def deserialise(cls, data, start_index):
        end_index = start_index + 8
        
        if len(data) < end_index:
            return None
        
        self = object.__new__(cls)
        self.balance = int.from_bytes(data[start_index : end_index], 'little')
        
        return self, end_index
   
   
    @copy_docs(QuestRewardSerialisableBase.serialise)
    def serialise(self):
        yield self.balance.to_bytes(8, 'little')
