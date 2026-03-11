__all__ = ('QuestRequirementSerialisableItemCategory',)

from struct import Struct

from scarletio import copy_docs

from ...item_core import produce_item_flags_with_names

from ..amount_types import produce_amount_type_with_name
from ..quest_requirement_types import QUEST_REQUIREMENT_TYPE_ITEM_CATEGORY

from .base import QuestRequirementSerialisableBase


QUEST_REQUIREMENT_COMPLETION_STATE_ITEM_CATEGORY_STRUCT = Struct('<QBQQ')


class QuestRequirementSerialisableItemCategory(QuestRequirementSerialisableBase):
    """
    Represents an category item requirement.
    
    Attributes
    ----------
    amount_required : `int`
        The required amount.
    
    amount_submitted : `int`
        The submitted amount.
    
    amount_type : `int`
        The amount's type.
    
    item_flags : `int`
        The required item flags the item should have.
    """
    TYPE = QUEST_REQUIREMENT_TYPE_ITEM_CATEGORY
    
    __slots__ = ('amount_required', 'amount_submitted', 'amount_type', 'item_flags')
    
    def __new__(cls, item_flags, amount_type, amount_required, amount_submitted):
        """
        Creates a new quest requirement for item amount.
        
        Parameters
        ----------
        item_flags : `int`
            The required item flags the item should have.
        
        amount_type : `int`
            The amount's type.
        
        amount_required : `int`
            The required amount.
        
        amount_submitted : `int`
            The submitted amount.
        """
        self = object.__new__(cls)
        self.item_flags = item_flags
        self.amount_type = amount_type
        self.amount_required = amount_required
        self.amount_submitted = amount_submitted
        return self
    
    
    @copy_docs(QuestRequirementSerialisableBase._produce_representation_middle)
    def _produce_representation_middle(self):
        # item_flags
        yield ' item_flags = '
        yield from produce_item_flags_with_names(self.item_flags)
        
        # amount_type
        yield ', amount_type = '
        yield from produce_amount_type_with_name(self.amount_type)
        
        # amount_required
        yield ', amount_required = '
        yield str(self.amount_required)
        
        # amount_submitted
        yield ', amount_submitted = '
        yield str(self.amount_submitted)
   
   
    @copy_docs(QuestRequirementSerialisableBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        # amount_required
        if self.amount_required != other.amount_required:
            return False
        
        # amount_submitted
        if self.amount_submitted != other.amount_submitted:
            return False
        
        # amount_type
        if self.amount_type != other.amount_type:
            return False
        
        # item_flags
        if self.item_flags != other.item_flags:
            return False
        
        return True
   
   
    @classmethod
    @copy_docs(QuestRequirementSerialisableBase.deserialise)
    def deserialise(cls, data, start_index):
        end_index = start_index + 25
        
        if len(data) < end_index:
            return None
        
        self = object.__new__(cls)
        (
            self.item_flags,
            self.amount_type,
            self.amount_required,
            self.amount_submitted,
        ) = QUEST_REQUIREMENT_COMPLETION_STATE_ITEM_CATEGORY_STRUCT.unpack(
            data[start_index : end_index]
        )
        return self, end_index
   
   
    @copy_docs(QuestRequirementSerialisableBase.serialise)
    def serialise(self):
        yield QUEST_REQUIREMENT_COMPLETION_STATE_ITEM_CATEGORY_STRUCT.pack(
            self.item_flags,
            self.amount_type,
            self.amount_required,
            self.amount_submitted,
        )
