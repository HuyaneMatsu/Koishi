__all__ = ('QuestRewardSerialisableItemExact',)

from struct import Struct

from scarletio import copy_docs

from ...item_core import produce_item_id_with_name

from ..quest_reward_types import QUEST_REWARD_TYPE_ITEM_EXACT

from .base import QuestRewardSerialisableBase


QUEST_REWARD_COMPLETION_STATE_ITEM_EXACT_STRUCT = Struct('<LQ')


class QuestRewardSerialisableItemExact(QuestRewardSerialisableBase):
    """
    Represents an exact item reward.
    
    Attributes
    ----------
    amount_given : `int`
        The given amount.
    
    item_id : `int`
        The given item's identifier.
    """
    TYPE = QUEST_REWARD_TYPE_ITEM_EXACT
    
    __slots__ = ('amount_given', 'item_id')
    
    def __new__(cls, item_id, amount_given):
        """
        Creates a new quest reward for item amount.
        
        Parameters
        ----------
        item_id : `int`
            The given item's identifier.
        
        amount_given : `int`
            The given amount.
        """
        self = object.__new__(cls)
        self.item_id = item_id
        self.amount_given = amount_given
        return self
    
    
    @copy_docs(QuestRewardSerialisableBase._produce_representation_middle)
    def _produce_representation_middle(self):
        # item_id
        yield ' item_id = '
        yield from produce_item_id_with_name(self.item_id)
        
        # amount_given
        yield ', amount_given = '
        yield str(self.amount_given)
   
   
    @copy_docs(QuestRewardSerialisableBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        # amount_given
        if self.amount_given != other.amount_given:
            return False
        
        # item_id
        if self.item_id != other.item_id:
            return False
        
        return True
   
   
    @classmethod
    @copy_docs(QuestRewardSerialisableBase.deserialise)
    def deserialise(cls, data, start_index):
        end_index = start_index + 12
        
        if len(data) < end_index:
            return None
        
        self = object.__new__(cls)
        (
            self.item_id,
            self.amount_given,
        ) = QUEST_REWARD_COMPLETION_STATE_ITEM_EXACT_STRUCT.unpack(
            data[start_index : end_index]
        )
        return self, end_index
   
   
    @copy_docs(QuestRewardSerialisableBase.serialise)
    def serialise(self):
        yield QUEST_REWARD_COMPLETION_STATE_ITEM_EXACT_STRUCT.pack(
            self.item_id,
            self.amount_given,
        )
