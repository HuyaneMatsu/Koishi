__all__ = ('QuestRequirementGeneratorChoice',)

from scarletio import copy_docs

from .base import QuestRequirementGeneratorBase


class QuestRequirementGeneratorChoice(QuestRequirementGeneratorBase):
    """
    Represents an choice requirement generator.
    
    Attributes
    ----------
    options : ``tuple<QuestRequirementGeneratorChoiceOption>``
        Options to choose from.
    """
    __slots__ = ('options',)
    
    def __new__(
        cls,
        options,
    ):
        """
        Creates a new quest choice requirement generator.
        
        Parameters
        ----------
        options : ``tuple<QuestRequirementGeneratorChoiceOption>``
            Options to choose from.
        """
        self = object.__new__(cls)
        self.options = options
        return self
    
    
    @copy_docs(QuestRequirementGeneratorBase._produce_representation_middle)
    def _produce_representation_middle(self):
        # options
        yield ' options = '
        yield repr(self.options)
    
    
    @copy_docs(QuestRequirementGeneratorBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        # options
        if self.options != other.options:
            return False
        
        return True
    
    
    @copy_docs(QuestRequirementGeneratorBase.generate)
    def generate(self, random_number_generator):
        options = self.options
        total_weight = sum(option.weight for option in options)
        value = total_weight * random_number_generator.random()
        
        cumulative = 0.0
        for option in options:
            cumulative += option.weight
            if cumulative >= value:
                break
        
        return option.generator.generate(random_number_generator)
