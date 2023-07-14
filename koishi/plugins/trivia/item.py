__all__ = ()

from scarletio import RichAttributeErrorBaseType


ITEMS = {}


class TriviaItem(RichAttributeErrorBaseType):
    """
    Represents a trivia item.
    
    Attributes
    ----------
    correct : `str`
        The correct answer.
    id : `int`
        The item's identifier.
    question : `str`
        The question to ask.
    options : `tuple` of `str`
        Additional options suggested to the user.
    """
    __slots__ = ('correct', 'id', 'question', 'options',)
    
    def __init__(self, question, correct, options):
        """
        Creates a new trivia item with the given options.
        
        Parameters
        ----------
        question : `str`
            The question to ask.
        correct : `str`
            The correct answer.
        options : `tuple` of `str`
            Additional options suggested to the user.
        """
        item_id = len(ITEMS) + 1
        
        self.correct = correct
        self.id = item_id
        self.question = question
        self.options = options
        
        ITEMS[item_id] = self
    
    
    def __repr__(self):
        """Returns the trivia item's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' id = ')
        repr_parts.append(repr(self.id))
        
        repr_parts.append(', question = ')
        repr_parts.append(repr(self.question))
        
        repr_parts.append(', correct = ')
        repr_parts.append(repr(self.correct))
        
        repr_parts.append(', options = ')
        repr_parts.append(repr(self.options))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
