__all__ = ('QuestRequirementGeneratorChoiceOption',)

from scarletio import copy_docs

from ..sub_type_bases import QuestSubTypeBase


class QuestRequirementGeneratorChoiceOption(QuestSubTypeBase):
    """
    Option of a requirement choice generator.
    
    Attributes
    ----------
    generator : ``QuestRequirementGeneratorBase``
        The wrapped generator.
    
    weight : `int`
        The weight of the option to be chosen.
    """
    __slots__ = ('generator', 'weight')
    
    def __new__(cls, generator, weight):
        """
        Creates a new choice option.
    
        Parameters
        ----------
        generator : ``QuestRequirementGeneratorBase``
            The wrapped generator.
        
        weight : `int`
            The weight of the option to be chosen.
        """
        self = object.__new__(cls)
        self.generator = generator
        self.weight = weight
        return self
    
    
    @copy_docs(QuestSubTypeBase._produce_representation_middle)
    def _produce_representation_middle(self):
        # generator
        yield ' generator = '
        yield repr(self.generator)
        
        # weight
        yield ' weight = '
        yield repr(self.weight)
    
    
    @copy_docs(QuestSubTypeBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        # generator
        if self.generator != other.generator:
            return False
        
        # weight
        if self.weight != other.weight:
            return False
        
        return True
