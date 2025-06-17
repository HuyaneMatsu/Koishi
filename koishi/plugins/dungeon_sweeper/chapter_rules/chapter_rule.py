__all__ = ('ChapterRule',)

from scarletio import RichAttributeErrorBaseType


class ChapterRule(RichAttributeErrorBaseType):
    """
    Represents the rules of a chapter.
    
    Attributes
    ----------
    component_builder : ``FunctionType``
        Rule component builder function.
    
    id : `int`
        The rule's identifier.
    """
    __slots__ = ('component_builder', 'id')
    
    def __new__(cls, chapter_rule_id, component_builder):
        """
        Creates a new rule with the given identifier.
        
        Parameters
        ----------
        chapter_rule_id : `int`
            The rule's identifier.
        
        component_builder : ``FunctionType``
            Rule component builder function.
        """
        self = object.__new__(cls)
        self.component_builder = component_builder
        self.id = chapter_rule_id
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # id
        repr_parts.append(' id = ')
        repr_parts.append(repr(self.id))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
