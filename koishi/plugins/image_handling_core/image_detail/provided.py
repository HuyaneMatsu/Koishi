__all__ = ('ImageDetailProvided',)

from scarletio import copy_docs

from .base import ImageDetailBase


class ImageDetailProvided(ImageDetailBase):
    """
    Represents a provided image.
    
    Attributes
    ----------
    provider : `None | str`
        The provider of the image.
    tags : `None | frozenset<str>`
        Additional tags for the image.
    url : `str`
        Url to the image.
    """
    __slots__ = ('provider', 'tags')
    
    
    @copy_docs(ImageDetailBase.__new__)
    def __new__(cls, url):
        self = ImageDetailBase.__new__(cls, url)
        self.provider = None
        self.tags = None
        return self
    
    
    @copy_docs(ImageDetailBase._put_repr_parts_into)
    def _put_repr_parts_into(self, repr_parts):
        # provider
        provider = self.provider
        if (provider is not None):
            repr_parts.append(', provider = ')
            repr_parts.append(repr(provider))
        
        # tags
        tags = self.tags
        if (tags is not None):
            repr_parts.append(', tags = ')
            repr_parts.append(repr(tags))

    
    @copy_docs(ImageDetailBase.copy)
    def copy(self):
        new = ImageDetailBase.copy(self)
        new.provider = self.provider
        new.tags = self.tags
        return new
