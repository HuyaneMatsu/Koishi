__all__ = ()

from scarletio import RichAttributeErrorBaseType


class Choice(RichAttributeErrorBaseType):
    """
    Represents a choice.
    
    Attributes
    ----------
    entity : ``Emoji | SoundboardSound | Sticker``
        The entity's type.
    
    type : ``type<ChoiceTypeBase>``
        The choice's type.
    """
    __slots__ = ('entity', 'type')
    
    def __new__(cls, entity, choice_type):
        """
        Parameters
        ----------
        entity : ``Emoji | SoundboardSound | Sticker``
            The entity's type.
        
        choice_type : ``type<ChoiceTypeBase>``
            The choice's type.
        """
        self = object.__new__(cls)
        self.entity = entity
        self.type = choice_type
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # name
        repr_parts.append(' type = ')
        repr_parts.append(self.type.name)
        
        # entity
        repr_parts.append(', entity = ')
        repr_parts.append(repr(self.entity))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self.entity is not other.entity:
            return False
        
        if self.type is not other.type:
            return False
        
        return True
    
    
    def __len__(self):
        """Returns len(self)."""
        return 2
    
    
    def __iter__(self):
        """
        Unpacks the choice.
        
        This method is an iterable generator.
        
        Yields
        ------
        entity / choice_type : ``Emoji | SoundboardSound | Sticker`` / ``type<ChoiceTypeBase>``
        """
        yield self.entity
        yield self.type
