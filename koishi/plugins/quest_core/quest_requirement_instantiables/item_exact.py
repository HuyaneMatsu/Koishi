__all__ = ('QuestRequirementInstantiableItemExact',)

from scarletio import copy_docs

from ...item_core import produce_item_id_with_name

from ..amount_types import produce_amount_type_with_name
from ..quest_requirement_serialisables import QuestRequirementSerialisableItemExact
from ..quest_requirement_types import QUEST_REQUIREMENT_TYPE_ITEM_EXACT

from .base import QuestRequirementInstantiableBase


class QuestRequirementInstantiableItemExact(QuestRequirementInstantiableBase):
    """
    Represents an exact item requirement.
    
    Attributes
    ----------
    amount_required : `int`
        The required amount.
    
    amount_type : `int`
        The amount's type.
    
    item_id : `int`
        The required item's identifier.
    """
    TYPE = QUEST_REQUIREMENT_TYPE_ITEM_EXACT
    
    __slots__ = ('amount_required', 'amount_type', 'item_id')
    
    def __new__(cls, item_id, amount_type, amount_required):
        """
        Creates a new quest exact item requirement.
        
        Parameters
        ----------
        item_id : `int`
            The required item's identifier.
        
        amount_type : `int`
            The amount's type.
        
        amount_required : `int`
            The required amount.
        """
        self = object.__new__(cls)
        self.item_id = item_id
        self.amount_type = amount_type
        self.amount_required = amount_required
        return self
    
    
    @copy_docs(QuestRequirementInstantiableBase._produce_representation_middle)
    def _produce_representation_middle(self):
        # item_id
        yield ' item_id = '
        yield from produce_item_id_with_name(self.item_id)
        
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
        
        # item_id
        if self.item_id != other.item_id:
            return False
        
        return True
    
    
    @copy_docs(QuestRequirementInstantiableBase.instantiate)
    def instantiate(self):
        return QuestRequirementSerialisableItemExact(
            self.item_id,
            self.amount_type,
            self.amount_required,
            0,
        )
