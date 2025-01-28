__all__ = ()

from itertools import count

from scarletio import RichAttributeErrorBaseType

from .asset import Asset
from .constants import EXTENSIONS_TO_CONVERT


class AssetGroup(RichAttributeErrorBaseType):
    """
    Represents grouped assets by their prefix.
    
    Attributes
    ----------
    assets : `None | dict<(index, str), Asset>`
        The grouped up assets.
    
    prefix : `str`
        The prefix based on what the assets are grouped.
    """
    __slots__ = ('assets', 'prefix',)
    
    def __new__(cls, prefix):
        """
        Creates a new asset group.
        
        Parameters
        ----------
        prefix : `str`
            The prefix to represent with the group.
        """
        self = object.__new__(cls)
        self.assets = None
        self.prefix = prefix
        return self
    
    
    def __repr__(self):
        """Returns the asset group's representation."""
        repr_parts = ['<', type(self).__name__]
        
        # prefix
        repr_parts.append(' prefix = ')
        repr_parts.append(repr(self.prefix))
        
        # assets:
        assets = self.assets
        if (assets is not None):
            repr_parts.append(', assets')
            repr_parts.append(repr(assets))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two entries are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        # assets
        if self.assets != other.assets:
            return False
        
        # prefix
        if self.prefix != other.prefix:
            return False
        
        return True
    
    
    def add_entry(self, asset_entry):
        """
        Adds a new asset to the asset group based on the given asset entry.
        
        Parameters
        ----------
        asset_entry : ``AssetEntry``
            Unprocessed asset entry to add.
        """
        assets = self.assets
        if assets is None:
            assets = {}
            self.assets = assets
        
        index = asset_entry.index
        extension = asset_entry.extension
        
        try:
            asset = assets[index, extension]
        except KeyError:
            asset = Asset(index, extension)
            assets[index, extension] = asset
        
        asset.add_variant(asset_entry)
    
    
    def pop_first_incorrect_asset(self):
        """
        Pops the first assets of the group that has incorrect extension.
        
        Returns
        -------
        asset : `None | Asset`
            The popped asset.
        """
        assets = self.assets
        if (assets is None):
            return None
        
        for asset in assets.values():
            if asset.extension in EXTENSIONS_TO_CONVERT:
                break
        else:
            return None
        
        del assets[asset.index, asset.extension]
        if not assets:
            self.assets = None
        return asset
    
    
    def find_best_fit_index(self):
        """
        Finds best fix index with good file extension.
        
        Returns
        -------
        best_fit_index : `int`
        """
        assets = self.assets
        if assets is None:
            return 0
        
        used_indexes = set()
        for asset in assets.values():
            if asset.extension in EXTENSIONS_TO_CONVERT:
                continue
            
            used_indexes.add(asset.index)
        
        for index in count():
            if index not in used_indexes:
                return index
