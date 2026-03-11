__all__ = ('QuestRewardInstantiableItemExact',)

from scarletio import copy_docs

from ...item_core import produce_item_id_with_name

from ..quest_reward_serialisables import QuestRewardSerialisableItemExact
from ..quest_reward_types import QUEST_REWARD_TYPE_ITEM_EXACT

from .base import QuestRewardInstantiableBase


class QuestRewardInstantiableItemExact(QuestRewardInstantiableBase):
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
    
    __slots__ = ('amount_given','item_id')
    
    def __new__(cls, item_id, amount_given):
        """
        Creates a new quest exact item reward.
        
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
    
    
    @copy_docs(QuestRewardInstantiableBase._produce_representation_middle)
    def _produce_representation_middle(self):
        # item_id
        yield ' item_id = '
        yield from produce_item_id_with_name(self.item_id)
        
        # amount_given
        yield ', amount_given = '
        yield repr(self.amount_given)
    
    
    @copy_docs(QuestRewardInstantiableBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        # amount_given
        if self.amount_given != other.amount_given:
            return False
        
        # item_id
        if self.item_id != other.item_id:
            return False
        
        return True
    
    
    @copy_docs(QuestRewardInstantiableBase.instantiate)
    def instantiate(self):
        return QuestRewardSerialisableItemExact(
            self.item_id,
            self.amount_given,
        )
