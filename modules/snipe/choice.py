__all__ = ()

from scarletio import RichAttributeErrorBaseType


class Choice(RichAttributeErrorBaseType):
    """
    Represents a choice.
    
    Attributes
    ----------
    entity : ``Emoji``, ``Sticker``
        The entity's type.
    type : `type<ChoiceTypeBase>`
        The choice's type.
    """
    __slots__ = ('entity', 'type')
    
    def __init__(self, entity, choice_type):
        """
        Parameters
        ----------
        entity : ``Emoji``, ``Sticker``
            The entity's type.
        choice_type : `type<ChoiceTypeBase>`
            The choice's type.
        """
        self.entity = entity
        self.type = choice_type
    
    
    def __repr__(self):
        """Returns the choice's representation"""
        return f'<{self.__class__.__name__} ({self.type.name}) entity = {self.entity!r}>'
    
    
    def __len__(self):
        """Returns the choice's length. Helper for unpacking."""
        return 2
    
    
    def __iter__(self):
        """
        Unpacks the choice.
        
        This method is an iterable generator.
        
        Yields
        ------
        entity / choice_type : ``Emoji`` |  ``Sticker`` / `type<ChoiceTypeBase>`
        """
        yield self.entity
        yield self.type
