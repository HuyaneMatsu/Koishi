__all__ = ('ImageDetailAction',)

from scarletio import RichAttributeErrorBaseType


class ImageDetailAction(RichAttributeErrorBaseType):
    """
    Represents an tag on an image.
    
    Attributes
    ----------
    tag : `str`
        The done action's tag..
    source : `None | TouhouCharacter`
        Source character.
    target : `None | TouhouCharacter`
        Target character.
    """
    __slots__ = ('source', 'tag', 'target')
    
    def __new__(cls, tag, source, target):
        """
        Creates a new image detail tag.
        
        Parameters
        ----------
        tag : `str`
            The done tag.
        source : `None | TouhouCharacter`
            Source character.
        target : `None | TouhouCharacter`
            Target character.
        """
        self = object.__new__(cls)
        self.tag = tag
        self.source = source
        self.target = target
        return self
    
    
    def __repr__(self):
        """Returns the image detail tag's representation."""
        repr_parts = ['<', type(self).__name__]
        
        # tag
        repr_parts.append(' tag = ')
        repr_parts.append(repr(self.tag))
        
        # source
        source = self.source
        if (source is not None):
            repr_parts.append(', source = ')
            repr_parts.append(repr(source))
        
        # target
        target = self.target
        if (target is not None):
            repr_parts.append(', target = ')
            repr_parts.append(repr(target))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns the image detail tag's hash value"""
        hash_value = 0
        
        # tag
        hash_value ^= hash(self.tag)
        
        # source
        source = self.source
        if (source is not None):
            hash_value ^= 156
            hash_value ^= hash(source)
        
        # target
        target = self.target
        if (target is not None):
            hash_value ^= 156 << 8
            if (source is not target):
                hash_value ^= hash(target)
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns whether the two touhou image detail tags are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.tag != other.tag:
            return False
        
        if self.source != other.source:
            return False
        
        if self.target != other.target:
            return False
        
        return True
    
    
    def __len__(self):
        """Helper for unpacking."""
        return 3
    
    
    def __iter__(self):
        """Unpacks."""
        yield self.tag
        yield self.source
        yield self.target
    
    
    def __gt__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        # tag
        if self.tag > other.tag:
            return True
        
        # source
        self_source = self.source
        other_source = other.source
        if (self_source is None):
            if (other_source is not None):
                return False
        
        else:
            if (other_source is None) or (self_source > other_source):
                return True
        
        # target
        self_target = self.target
        other_target = other.target
        if (self_target is None):
            if (other_target is not None):
                return False
        
        else:
            if (other_target is None) or (self_target > other_target):
                return True
        
        return False
    
    
    def iter_characters(self):
        """
        Iterates overt he characters registered into the tag.
        
        This method is an iterable generator.
        
        Yields
        ------
        character : ``TouhouCharacter``
        """
        source = self.source
        if (source is not None):
            yield source
        
        target = self.target
        if (target is not None):
            yield target
