__all__ = ('ImageDetailStatic',)

from scarletio import copy_docs

from .base import ImageDetailBase


class ImageDetailStatic(ImageDetailBase):
    """
    Represents a static image.
    
    Attributes
    ----------
    _cache_name : `None | str`
        Cache slot for `.name`.
    actions : `None | tuple<ImageDetailAction>`
        Actions done on the image.
    characters : `None`, `tuple<TouhouCharacter>`
        Touhou characters presented on the image.
    creators : `None | tuple<str>`
        Who created the image.
    editors : `None | tuple<str>`
        Who edited the image.
    url : `str`
        Url to the image.
    """
    __slots__ = ('_cache_name', 'actions', 'characters', 'creators', 'editors')
    
    
    @copy_docs(ImageDetailBase.__new__)
    def __new__(cls, url):
        self = ImageDetailBase.__new__(cls, url)
        self._cache_name = None
        self.actions = None
        self.characters = None
        self.creators = None
        self.editors = None
        return self
    
    
    @copy_docs(ImageDetailBase._put_repr_parts_into)
    def _put_repr_parts_into(self, repr_parts):
        # actions
        actions = self.actions
        if (actions is not None):
            repr_parts.append(', actions = ')
            repr_parts.append(repr(actions))
        
        # characters
        characters = self.characters
        if (characters is not None):
            repr_parts.append(', characters = ')
            repr_parts.append(repr(characters))
        
        # creators
        creators = self.creators
        if (creators is not None):
            repr_parts.append(', creators = ')
            repr_parts.append(repr(creators))
        
        # editors
        editors = self.editors
        if (editors is not None):
            repr_parts.append(', editors = ')
            repr_parts.append(repr(editors))
    
    
    @copy_docs(ImageDetailBase.copy)
    def copy(self):
        new = ImageDetailBase.copy(self)
        new._cache_name = self._cache_name
        new.actions = self.actions
        new.characters = self.characters
        new.creators = self.creators
        new.editors = self.editors
        return new
    
    
    @property
    @copy_docs(ImageDetailBase.name)
    def name(self):
        name = self._cache_name
        if name is None:
            name = ImageDetailBase.name.fget(self)
            self._cache_name = name
        
        return name
