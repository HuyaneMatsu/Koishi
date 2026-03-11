__all__ = ('QuestRewardGeneratorItemExactFix',)

from scarletio import copy_docs

from ...item_core import produce_item_id_with_name

from ..quest_reward_instantiables import QuestRewardInstantiableItemExact
from ..quest_reward_types import QUEST_REWARD_TYPE_ITEM_EXACT

from .base import QuestRewardGeneratorBase


class QuestRewardGeneratorItemExactFix(QuestRewardGeneratorBase):
    """
    Represents an exact item reward generator.
    
    Attributes
    ----------
    amount_base : `int`
        The amount of items given by the quest.
    
    item_id : `int`
        The required item's identifier.
    """
    TYPE = QUEST_REWARD_TYPE_ITEM_EXACT
    
    __slots__ = (
        'amount_base', 'item_id'
    )
    
    def __new__(
        cls,
        item_id,
        amount_base,
    ):
        """
        Creates a new quest exact item reward generator.
        
        Parameters
        ----------
        item_id : `int`
            The required item's identifier.
        
        amount_base : `int`
            The amount of items given by the quest.
        """
        self = object.__new__(cls)
        self.amount_base = amount_base
        self.item_id = item_id
        return self
    
    
    @copy_docs(QuestRewardGeneratorBase._produce_representation_middle)
    def _produce_representation_middle(self):
        # item_id
        yield ' item_id = '
        yield from produce_item_id_with_name(self.item_id)
        
        # amount_base
        yield ', amount_base = '
        yield repr(self.amount_base)
    
    
    @copy_docs(QuestRewardGeneratorBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        # amount_base
        if self.amount_base != other.amount_base:
            return False
        
        # item_id
        if self.item_id != other.item_id:
            return False
        
        return True
    
    
    @copy_docs(QuestRewardGeneratorBase.generate_with_diversion)
    def generate_with_diversion(self, random_number_generator, accumulated_diversion):
        return (
            QuestRewardInstantiableItemExact(self.item_id, self.amount_base),
            1.0,
        )
