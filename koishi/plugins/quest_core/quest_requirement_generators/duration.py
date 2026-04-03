__all__ = ('QuestRequirementGeneratorDuration',)

from scarletio import copy_docs

from ..generation_helpers import get_random_value_and_diversity_with_variance
from ..quest_requirement_instantiables import QuestRequirementInstantiableDuration
from ..quest_requirement_types import QUEST_REQUIREMENT_TYPE_DURATION

from .base import QuestRequirementGeneratorBase


class QuestRequirementGeneratorDuration(QuestRequirementGeneratorBase):
    """
    Represents a quest requirement generator with fix duration.
    
    Attributes
    ----------
    duration_base : `int`
        The quest's duration in seconds.
    
    duration_require_multiple_of : `int`
        Value to require the duration to be multiple of.
    
    duration_variance_percentage_lower_threshold : `int`
        Lower threshold of for duration variance in percentage.
    
    duration_variance_percentage_upper_threshold : `int`
        Upper threshold of for duration variance in percentage.
    """
    TYPE = QUEST_REQUIREMENT_TYPE_DURATION
   
    __slots__ = (
        'duration_base', 'duration_require_multiple_of', 'duration_variance_percentage_lower_threshold',
        'duration_variance_percentage_upper_threshold',
    )
   
    def __new__(
        cls,
        duration_base,
        duration_require_multiple_of,
        duration_variance_percentage_lower_threshold,
        duration_variance_percentage_upper_threshold,
    ):
        """
        Creates a new duration requirement generator.
        
        Parameters
        ----------
        duration_base : `int`
            The quest's duration in seconds.
        
        duration_require_multiple_of : `int`
            Value to require the duration to be multiple of.
        
        duration_variance_percentage_lower_threshold : `int`
            Lower threshold of for duration variance in percentage.
        
        duration_variance_percentage_upper_threshold : `int`
            Upper threshold of for duration variance in percentage.
        """
        self = object.__new__(cls)
        self.duration_base = duration_base
        self.duration_require_multiple_of = duration_require_multiple_of
        self.duration_variance_percentage_lower_threshold = duration_variance_percentage_lower_threshold
        self.duration_variance_percentage_upper_threshold = duration_variance_percentage_upper_threshold
        return self
    
    
    @copy_docs(QuestRequirementGeneratorBase._produce_representation_middle)
    def _produce_representation_middle(self):
        # duration_base
        yield ' duration_base = '
        yield repr(self.duration_base)
        
        # duration_require_multiple_of
        yield ', duration_require_multiple_of = '
        yield repr(self.duration_require_multiple_of)
        
        # duration_variance_percentage_lower_threshold
        yield ', duration_variance_percentage_lower_threshold = '
        yield repr(self.duration_variance_percentage_lower_threshold)
        
        # duration_variance_percentage_upper_threshold
        yield ', duration_variance_percentage_upper_threshold = '
        yield repr(self.duration_variance_percentage_upper_threshold)
    
    
    @copy_docs(QuestRequirementGeneratorBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        # duration_base
        if self.duration_base != other.duration_base:
            return False
        
        # duration_require_multiple_of
        if self.duration_require_multiple_of != other.duration_require_multiple_of:
            return False
        
        # duration_variance_percentage_lower_threshold
        if self.duration_variance_percentage_lower_threshold != other.duration_variance_percentage_lower_threshold:
            return False
        
        # duration_variance_percentage_upper_threshold
        if self.duration_variance_percentage_upper_threshold != other.duration_variance_percentage_upper_threshold:
            return False
        
        return True
    
    
    @copy_docs(QuestRequirementGeneratorBase.generate)
    def generate(self, random_number_generator):
        duration, diversion = get_random_value_and_diversity_with_variance(
            random_number_generator,
            self.duration_base,
            self.duration_require_multiple_of,
            self.duration_variance_percentage_lower_threshold,
            self.duration_variance_percentage_upper_threshold,
        )
        
        return (
            QuestRequirementInstantiableDuration(duration),
            (1.0 / diversion),
        )
