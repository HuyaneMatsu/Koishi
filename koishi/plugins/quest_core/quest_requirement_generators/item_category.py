__all__ = ('QuestRequirementGeneratorItemCategory',)

from scarletio import copy_docs

from ...item_core import produce_item_flags_with_names

from ..amount_types import produce_amount_type_with_name
from ..generation_helpers import get_random_value_and_diversity_with_variance
from ..quest_requirement_instantiables import QuestRequirementInstantiableItemCategory
from ..quest_requirement_types import QUEST_REQUIREMENT_TYPE_ITEM_CATEGORY

from .base import QuestRequirementGeneratorBase


class QuestRequirementGeneratorItemCategory(QuestRequirementGeneratorBase):
    """
    Represents an category item requirement generator.
    
    Attributes
    ----------
    amount_base : `int`
        The amount of items required by the quest.
    
    amount_require_multiple_of : `int`
        Value to require the amount to be multiple of.
    
    amount_type : `int`
        The amount's type.
    
    amount_variance_percentage_lower_threshold : `int`
        Lower threshold of for amount variance in percentage.
    
    amount_variance_percentage_upper_threshold : `int`
        Upper threshold of for amount variance in percentage.
    
    item_flags : `int`
        The required item flags the items should have.
    """
    TYPE = QUEST_REQUIREMENT_TYPE_ITEM_CATEGORY
    
    __slots__ = (
        'amount_base', 'amount_require_multiple_of', 'amount_type', 'amount_variance_percentage_lower_threshold',
        'amount_variance_percentage_upper_threshold', 'item_flags'
    )
    
    def __new__(
        cls,
        item_flags,
        amount_type,
        amount_base,
        amount_require_multiple_of,
        amount_variance_percentage_lower_threshold,
        amount_variance_percentage_upper_threshold,
    ):
        """
        Creates a new quest category item requirement generator.
        
        Parameters
        ----------
        item_flags : `int`
            The required item flags the items should have.
        
        amount_type : `int`
            The amount's type.
        
        amount_base : `int`
            The amount of items required by the quest.
        
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
        self.amount_type = amount_type
        self.amount_variance_percentage_lower_threshold = amount_variance_percentage_lower_threshold
        self.amount_variance_percentage_upper_threshold = amount_variance_percentage_upper_threshold
        self.item_flags = item_flags
        return self
    
    
    @copy_docs(QuestRequirementGeneratorBase._produce_representation_middle)
    def _produce_representation_middle(self):
        # item_flags
        yield ' item_flags = '
        yield from produce_item_flags_with_names(self.item_flags)
        
        # amount_type
        yield ', amount_type = '
        yield from produce_amount_type_with_name(self.amount_type)
        
        # amount_require_multiple_of
        yield ', amount_require_multiple_of = '
        yield repr(self.amount_require_multiple_of)
        
        # amount_variance_percentage_lower_threshold
        yield ', amount_variance_percentage_lower_threshold = '
        yield repr(self.amount_variance_percentage_lower_threshold)
        
        # amount_variance_percentage_upper_threshold
        yield ', amount_variance_percentage_upper_threshold = '
        yield repr(self.amount_variance_percentage_upper_threshold)
    
    
    @copy_docs(QuestRequirementGeneratorBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        # amount_base
        if self.amount_base != other.amount_base:
            return False
        
        # amount_require_multiple_of
        if self.amount_require_multiple_of != other.amount_require_multiple_of:
            return False
        
        # amount_type
        if self.amount_type != other.amount_type:
            return False
        
        # amount_variance_percentage_lower_threshold
        if self.amount_variance_percentage_lower_threshold != other.amount_variance_percentage_lower_threshold:
            return False
        
        # amount_variance_percentage_upper_threshold
        if self.amount_variance_percentage_upper_threshold != other.amount_variance_percentage_upper_threshold:
            return False
        
        # item_flags
        if self.item_flags != other.item_flags:
            return False
        
        return True
    
    
    @copy_docs(QuestRequirementGeneratorBase.generate)
    def generate(self, random_number_generator):
        amount, diversion = get_random_value_and_diversity_with_variance(
            random_number_generator,
            self.amount_base,
            self.amount_require_multiple_of,
            self.amount_variance_percentage_lower_threshold,
            self.amount_variance_percentage_upper_threshold,
        )
        
        return (
            QuestRequirementInstantiableItemCategory(self.item_flags, self.amount_type, amount),
            diversion,
        )
