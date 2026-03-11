__all__ = ('QuestRewardGeneratorItemExact',)

from scarletio import copy_docs

from ...item_core import produce_item_id_with_name

from ..generation_helpers import get_random_value_and_diversity_with_variance
from ..quest_reward_instantiables import QuestRewardInstantiableItemExact
from ..quest_reward_types import QUEST_REWARD_TYPE_ITEM_EXACT

from .base import QuestRewardGeneratorBase


class QuestRewardGeneratorItemExact(QuestRewardGeneratorBase):
    """
    Represents an exact item reward generator.
    
    Attributes
    ----------
    amount_base : `int`
        The amount of items given by the quest.
    
    amount_require_multiple_of : `int`
        Value to require the amount to be multiple of.
    
    amount_variance_percentage_lower_threshold : `int`
        Lower threshold of for amount variance in percentage.
    
    amount_variance_percentage_upper_threshold : `int`
        Upper threshold of for amount variance in percentage.
    
    item_id : `int`
        The required item's identifier.
    """
    TYPE = QUEST_REWARD_TYPE_ITEM_EXACT
    
    __slots__ = (
        'amount_base', 'amount_require_multiple_of', 'amount_variance_percentage_lower_threshold',
        'amount_variance_percentage_upper_threshold', 'item_id'
    )
    
    def __new__(
        cls,
        item_id,
        amount_base,
        amount_require_multiple_of,
        amount_variance_percentage_lower_threshold,
        amount_variance_percentage_upper_threshold,
    ):
        """
        Creates a new quest exact item reward generator.
        
        Parameters
        ----------
        item_id : `int`
            The required item's identifier.
        
        amount_base : `int`
            The amount of items given by the quest.
        
        amount_require_multiple_of : `int`
            Value to require the amount to be multiple of.
        
        amount_variance_percentage_lower_threshold : `int`
            Lower threshold of for amount variance in percentage.
        
        amount_variance_percentage_upper_threshold : `int`
            Upper threshold of for amount variance in percentage.
        """
        self = object.__new__(cls)
        self.amount_base = amount_base
        self.amount_require_multiple_of = amount_require_multiple_of
        self.amount_variance_percentage_lower_threshold = amount_variance_percentage_lower_threshold
        self.amount_variance_percentage_upper_threshold = amount_variance_percentage_upper_threshold
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
        
        # amount_require_multiple_of
        yield ', amount_require_multiple_of = '
        yield repr(self.amount_require_multiple_of)
        
        # amount_variance_percentage_lower_threshold
        yield ', amount_variance_percentage_lower_threshold = '
        yield repr(self.amount_variance_percentage_lower_threshold)
        
        # amount_variance_percentage_upper_threshold
        yield ', amount_variance_percentage_upper_threshold = '
        yield repr(self.amount_variance_percentage_upper_threshold)
    
    
    @copy_docs(QuestRewardGeneratorBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        # amount_base
        if self.amount_base != other.amount_base:
            return False
        
        # amount_require_multiple_of
        if self.amount_require_multiple_of != other.amount_require_multiple_of:
            return False
        
        # amount_variance_percentage_lower_threshold
        if self.amount_variance_percentage_lower_threshold != other.amount_variance_percentage_lower_threshold:
            return False
        
        # amount_variance_percentage_upper_threshold
        if self.amount_variance_percentage_upper_threshold != other.amount_variance_percentage_upper_threshold:
            return False
        
        # item_id
        if self.item_id != other.item_id:
            return False
        
        return True
    
    
    @copy_docs(QuestRewardGeneratorBase.generate_with_diversion)
    def generate_with_diversion(self, random_number_generator, accumulated_diversion):
        
        amount, diversion = get_random_value_and_diversity_with_variance(
            random_number_generator,
            round(self.amount_base * accumulated_diversion),
            self.amount_require_multiple_of,
            self.amount_variance_percentage_lower_threshold,
            self.amount_variance_percentage_upper_threshold,
        )
        
        return (
            QuestRewardInstantiableItemExact(self.item_id, amount),
            (1.0 / diversion),
        )
