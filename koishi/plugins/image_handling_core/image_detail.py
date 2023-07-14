__all__ = ('ImageDetail',)

class ImageDetail:
    """
    Represents an image.
    
    Attributes
    ----------
    url : `str`
        Url to the image.
    tags : `frozenset` of `str`
        Additional tags for the image.
    provider : `None`, `str`
        The provider of the image.
    """
    __slots__ = ('url', 'tags', 'provider')
    
    def __new__(cls, url, tags, provider=None):
        """
        Creates a new image detail.
        
        Parameters
        ----------
        url : `str`
            Url to the image.
        tags : `frozenset` of `str`
            Additional tags for the image.
        provider : `None, `str` = `None`, Optional
            Provider of the image.
        """
        self = object.__new__(cls)
        self.url = url
        self.tags = tags
        self.provider = provider
        return self
    
    
    def __repr__(self):
        """Returns the image handler's representation."""
        repr_parts = [self.__class__.__name__, '(', repr(self.url), ', ', repr(self.tags)]
        
        provider = self.provider
        if (provider is not None):
            repr_parts.append(', ')
            repr_parts.append(repr(provider))
        
        repr_parts.append(')')
        
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns the image detail's hash value."""
        hash_value = hash(self.url)
        
        tags = self.tags
        if (tags is not None):
            hash_value ^= hash(tags)
        
        provider = self.provider
        if (provider is not None):
            hash_value ^= hash(provider)
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns whether the two image details are equal."""
        if type(self) is not type(other):
            return False
        
        if self.url != other.url:
            return False
        
        if self.tags != other.tags:
            return False
        
        if self.provider != other.provider:
            return False
        
        return True
