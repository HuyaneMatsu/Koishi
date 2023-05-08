__all__ = ()

from scarletio import RichAttributeErrorBaseType


CATEGORIES = {}


class TriviaCategory(RichAttributeErrorBaseType):
    """
    Represents a trivia category.
    
    Attributes
    ----------
    id : `int`
        The category's identifier.
    items : `tuple` of ``TriviaItem``
        Possibilities suggested to the user. The 0th is always the correct one.
    """
    __slots__ = ('id', 'items', 'name')
    
    def __init__(self, name, items):
        """
        Creates a new trivia item with the given options.
        
        Parameters
        ----------
        name : `str`
            The name of the category.
        items : `tuple` of ``TriviaItem``
            Items under the category.
        """
        category_id = len(CATEGORIES) + 1
        
        self.id = category_id
        self.items = items
        self.name = name
        
        CATEGORIES[category_id] = self
    
    
    def __repr__(self):
        """
        Returns the trivia item's representation.
        """
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(', name = ')
        repr_parts.append(repr(self.name))
        
        repr_parts.append(', item = ')
        repr_parts.append(repr(self.items))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
