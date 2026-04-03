__all__ = ('QuestRequirementSerialisableItemExact',)

from struct import Struct

from scarletio import copy_docs

from ...item_core import produce_item_id_with_name

from ..amount_types import produce_amount_type_with_name
from ..quest_requirement_types import QUEST_REQUIREMENT_TYPE_ITEM_EXACT

from .base import QuestRequirementSerialisableBase


QUEST_REQUIREMENT_COMPLETION_STATE_ITEM_EXACT_STRUCT = Struct('<LBQQ')


class QuestRequirementSerialisableItemExact(QuestRequirementSerialisableBase):
    """
    Represents an exact item requirement.
    
    Attributes
    ----------
    amount_required : `int`
        The required amount.
    
    amount_submitted : `int`
        The submitted amount.
    
    amount_type : `int`
        The amount's type.
    
    item_id : `int`
        The required item's identifier.
    """
    TYPE = QUEST_REQUIREMENT_TYPE_ITEM_EXACT
    
    __slots__ = ('amount_required', 'amount_submitted', 'amount_type', 'item_id')
    
    def __new__(cls, item_id, amount_type, amount_required, amount_submitted):
        """
        Creates a new quest requirement for item amount.
        
        Parameters
        ----------
        item_id : `int`
            The required item's identifier.
        
        amount_type : `int`
            The amount's type.
        
        amount_required : `int`
            The required amount.
        
        amount_submitted : `int`
            The submitted amount.
        """
        self = object.__new__(cls)
        self.item_id = item_id
        self.amount_type = amount_type
        self.amount_required = amount_required
        self.amount_submitted = amount_submitted
        return self
    
    
    @copy_docs(QuestRequirementSerialisableBase._produce_representation_middle)
    def _produce_representation_middle(self):
        # item_id
        yield ' item_id = '
        yield from produce_item_id_with_name(self.item_id)
        
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
        
        # item_id
        if self.item_id != other.item_id:
            return False
        
        return True
   
   
    @classmethod
    @copy_docs(QuestRequirementSerialisableBase.deserialise)
    def deserialise(cls, data, start_index):
        end_index = start_index + 21
        
        if len(data) < end_index:
            return None
        
        self = object.__new__(cls)
        (
            self.item_id,
            self.amount_type,
            self.amount_required,
            self.amount_submitted,
        ) = QUEST_REQUIREMENT_COMPLETION_STATE_ITEM_EXACT_STRUCT.unpack(
            data[start_index : end_index]
        )
        return self, end_index
   
   
    @copy_docs(QuestRequirementSerialisableBase.serialise)
    def serialise(self):
        yield QUEST_REQUIREMENT_COMPLETION_STATE_ITEM_EXACT_STRUCT.pack(
            self.item_id,
            self.amount_type,
            self.amount_required,
            self.amount_submitted,
        )
