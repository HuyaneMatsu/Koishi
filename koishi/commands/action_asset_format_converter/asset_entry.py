__all__ = ()

from scarletio import RichAttributeErrorBaseType


class AssetEntry(RichAttributeErrorBaseType):
    """
    Represents an unprocessed asset entry.
    
    Attributes
    ----------
    _cache_name : `None | str`
        Cache slot for `.name`.
    
    extension : `str`
        The asset's extension.
    
    index : `int`
        The asset's index under its prefix.
    
    postfix : `None | str`
        The assets postfix if it has.
    
    prefix : `str`
        The assets prefix.
    """
    __slots__ = ('_cache_name', 'extension', 'index', 'postfix', 'prefix')
    
    def __new__(cls, prefix, index, postfix, extension):
        """
        Creates a new asset entry.
        
        Parameters
        ----------
        prefix : `str`
            The assets prefix.
        
        index : `int`
            The asset's index under its prefix.
        
        postfix : `None | str`
            The assets postfix if it has.
        
        extension : `str`
            The asset's extension.
        """
        self = object.__new__(cls)
        self._cache_name = None
        self.extension = extension
        self.index = index
        self.postfix = postfix
        self.prefix = prefix
        return self
    
    
    def __repr__(self):
        """Returns the asset entry's representation."""
        repr_parts = ['<', type(self).__name__]
        
        # prefix
        repr_parts.append(' prefix = ')
        repr_parts.append(repr(self.prefix))
        
        # index
        repr_parts.append(', index = ')
        repr_parts.append(repr(self.index))
        
        # postfix
        postfix = self.postfix
        if (postfix is not None):
            repr_parts.append(', postfix = ')
            repr_parts.append(repr(postfix))
        
        # extension
        repr_parts.append(', extension = ')
        repr_parts.append(repr(self.extension))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two entries are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        # extension
        if self.extension != other.extension:
            return False
        
        # index
        if self.index != other.index:
            return False
        
        # postfix
        if self.postfix != other.postfix:
            return False
        
        # prefix
        if self.prefix != other.prefix:
            return False
        
        return True
    
    
    def reconstruct_file_name(self):
        """
        Reconstructs the represented file's name.
        
        Returns
        -------
        file_name : `str`
        """
        file_name_parts = [self.prefix, '-', str(self.index).rjust(4, '0')]
        
        postfix = self.postfix
        if (postfix is not None):
            file_name_parts.append('-')
            file_name_parts.append(postfix)
        
        file_name_parts.append('.')
        file_name_parts.append(self.extension)
        
        return ''.join(file_name_parts)
    
    
    @property
    def name(self):
        """
        Returns the asset name of the asset entry.
        
        Returns
        -------
        name : `str`
        """
        name = self._cache_name
        if name is None:
            name = f'{self.prefix}-{str(self.index).rjust(4, "0")}'
            self._cache_name = name
        
        return name
