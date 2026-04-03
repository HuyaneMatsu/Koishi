__all__ = ('QuestRequirementGeneratorExpiration',)

from scarletio import copy_docs
from hata import DATETIME_FORMAT_CODE

from ..quest_requirement_instantiables import QuestRequirementInstantiableExpiration
from ..quest_requirement_types import QUEST_REQUIREMENT_TYPE_EXPIRATION

from .base import QuestRequirementGeneratorBase


class QuestRequirementGeneratorExpiration(QuestRequirementGeneratorBase):
    """
    Represents a quest requirement generator with fix expiration.
    
    Attributes
    ----------
    expiration : `DateTime`
        When the quest expires.
    """
    TYPE = QUEST_REQUIREMENT_TYPE_EXPIRATION
   
    __slots__ = ('expiration',)
   
    def __new__(cls, expiration):
        """
        Creates a new expiration requirement generator.
        
        Parameters
        ----------
        expiration : `DateTime`
            When the quest expires.
        """
        self = object.__new__(cls)
        self.expiration = expiration
        return self
    
    
    @copy_docs(QuestRequirementGeneratorBase._produce_representation_middle)
    def _produce_representation_middle(self):
        # expiration
        yield ' expiration = '
        yield format(self.expiration, DATETIME_FORMAT_CODE)
    
    
    @copy_docs(QuestRequirementGeneratorBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        # expiration
        if self.expiration != other.expiration:
            return False
        
        return True
    
    
    @copy_docs(QuestRequirementGeneratorBase.generate)
    def generate(self, random_number_generator):
        return (
            QuestRequirementInstantiableExpiration(self.expiration),
            1.0,
        )
