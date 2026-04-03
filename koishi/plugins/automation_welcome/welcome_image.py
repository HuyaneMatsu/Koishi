__all__ = ('WelcomeImage',)

from scarletio import RichAttributeErrorBaseType


class WelcomeImage(RichAttributeErrorBaseType):
    """
    Represents a welcome image.
    
    Attributes
    ----------
    creator : `str`
        The image's creator.
        
    url : `str`
        Url to the image.
    """
    __slots__ = ('creator', 'url')
    
    
    def __new__(cls, creator, url):
        """
        Creates a new welcome image instance.
        
        Parameters
        ----------
        creator : `str`
            The image's creator.
        
        url : `str`
            Url to the image.
        """
        self = object.__new__(cls)
        self.creator = creator
        self.url = url
        return self
    
    
    def __repr__(self):
        """Returns the welcome image's representation."""
        repr_parts = ['<', type(self).__name__]
        
        # creator
        repr_parts.append(' creator = ')
        repr_parts.append(repr(self.creator))
        
        # url
        repr_parts.append(', url = ')
        repr_parts.append(repr(self.url))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
