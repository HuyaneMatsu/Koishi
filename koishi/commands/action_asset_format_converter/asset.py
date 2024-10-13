__all__ = ()

from scarletio import RichAttributeErrorBaseType


class Asset(RichAttributeErrorBaseType):
    """
    Represents and asset of a ``AssetGroup``.
    
    Attributes
    ----------
    default_variant : `bool`
        Whether the asset has default variant.
    
    extension : `str`
        File extension.
    
    index : `int`
        The index of the asset.
    
    variants : `None | list<str>`
        Additional variants of the asset.
    """
    __slots__ = ('default_variant', 'extension', 'index', 'variants')
    
    def __new__(cls, index, extension):
        """
        Creates a new asset.
        
        Parameters
        ----------
        index : `int`
            The index of the asset.
        
        extension : `str`
            File extension.
        """
        self = object.__new__(cls)
        self.default_variant = False
        self.index = index
        self.extension = extension
        self.variants = None
        return self
    
    
    def __repr__(self):
        """Returns the assets representation."""
        repr_parts = ['<', type(self).__name__]
        
        # index
        repr_parts.append(' index = ')
        repr_parts.append(repr(self.index))
        
        # extension
        repr_parts.append(', extension = ')
        repr_parts.append(repr(self.extension))
        
        # default_variant
        default_variant = self.default_variant
        if default_variant:
            repr_parts.append(', default_variant = ')
            repr_parts.append(repr(default_variant))
        
        # variants
        variants = self.variants
        if (variants is not None):
            repr_parts.append(', variants = ')
            repr_parts.append(repr(variants))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two assets are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        # default_variant
        if self.default_variant != other.default_variant:
            return False
        
        # index
        if self.index != other.index:
            return False
        
        # extension
        if self.extension != other.extension:
            return False
        
        # variants
        if self.variants != other.variants:
            return False
        
        return True
    
    
    def add_variant(self, asset_entry):
        """
        Adds a new variant to the asset based on the asset entry.
        
        Parameters
        ----------
        asset_entry : ``AssetEntry``
            Unprocessed asset entry to add.
        """
        postfix = asset_entry.postfix
        if postfix is None:
            self.default_variant = True
            return
        
        variants = self.variants
        if (variants is None):
            variants = []
            self.variants = variants
        
        # safe guard
        if postfix in variants:
            return
        
        variants.append(postfix)
        variants.sort()
    
    
    def iter_postfix_variants(self):
        """
        Iterates over the postfix variants.
        
        This method is an iterable generator.
        
        Yields
        ------
        variant : `None | str`
        """
        if self.default_variant:
            yield None
        
        variants = self.variants
        if (variants is not None):
            yield from variants
