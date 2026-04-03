__all__ = ('QuestRequirementInstantiableItemCategory',)

from scarletio import copy_docs

from ...item_core import produce_item_flags_with_names

from ..amount_types import produce_amount_type_with_name
from ..quest_requirement_serialisables import QuestRequirementSerialisableItemCategory
from ..quest_requirement_types import QUEST_REQUIREMENT_TYPE_ITEM_CATEGORY

from .base import QuestRequirementInstantiableBase


class QuestRequirementInstantiableItemCategory(QuestRequirementInstantiableBase):
    """
    Represents an category item requirement.
    
    Attributes
    ----------
    amount_required : `int`
        The required amount.
    
    amount_type : `int`
        The amount's type.
    
    item_flags : `int`
        The required item flags the item should have.
    """
    TYPE = QUEST_REQUIREMENT_TYPE_ITEM_CATEGORY
    
    __slots__ = ('amount_required', 'amount_type', 'item_flags')
    
    def __new__(cls, item_flags, amount_type, amount_required):
        """
        Creates a new quest category item requirement.
        
        Parameters
        ----------
        item_flags : `int`
            The required item flags the item should have.
        
        amount_type : `int`
            The amount's type.
        
        amount_required : `int`
            The required amount.
        """
        self = object.__new__(cls)
        self.item_flags = item_flags
        self.amount_type = amount_type
        self.amount_required = amount_required
        return self
    
    
    @copy_docs(QuestRequirementInstantiableBase._produce_representation_middle)
    def _produce_representation_middle(self):
        # item_flags
        yield ', item_flags = '
        yield from produce_item_flags_with_names(self.item_flags)
        
        # amount_type
        yield ', amount_type = '
        yield from produce_amount_type_with_name(self.amount_type)
        
        # amount_required
        yield ', amount_required = '
        yield repr(self.amount_required)
    
    
    @copy_docs(QuestRequirementInstantiableBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        # amount_type
        if self.amount_type != other.amount_type:
            return False
        
        # amount_required
        if self.amount_required != other.amount_required:
            return False
        
        # item_flags
        if self.item_flags != other.item_flags:
            return False
        
        return True
    
    
    @copy_docs(QuestRequirementInstantiableBase.instantiate)
    def instantiate(self):
        return QuestRequirementSerialisableItemCategory(
            self.item_flags,
            self.amount_type,
            self.amount_required,
            0,
        )
