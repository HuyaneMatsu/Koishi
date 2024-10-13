__all__ = ()

from os import listdir as list_directory, remove as delete_file
from os.path import isfile as is_file, join as join_paths

from PIL import Image

from .asset_entry import AssetEntry
from .asset_group import AssetGroup
from .constants import ASSET_NAME_PATTERN


def notify(message):
    """
    Shows the given message.
    
    Parameters
    ----------
    message : `str`
        The message to show.
    """
    print(message)


def read_asset_entries(directory):
    """
    Reads asset entries from the given directory.
    
    Parameters
    ----------
    directory : `str`
        Target directory.
    
    Returns
    -------
    asset_entries : `list<AssetEntry>`
        The read asset entries.
    """
    asset_entries = []
    
    for name in list_directory(directory):
        file_path = join_paths(directory, name)
        if not is_file(file_path):
            notify(f'Skipping: {name} (not a file)')
            continue
        
        match = ASSET_NAME_PATTERN.fullmatch(name)
        if (match is None):
            notify(f'Skipping: {name} (invalid name structure)')
            continue
        
        prefix, index, postfix, extension = match.groups()
        entry = AssetEntry(prefix, int(index), postfix, extension)
        asset_entries.append(entry)
    
    return asset_entries


def group_assets(asset_entries):
    """
    Parameters
    ----------
    asset_entries : `list<AssetEntry>`
        Asset entries to group.
    
    Returns
    -------
    asset_groups : `dict<str, AssetGroup>`
        The grouped asset groups.
    """
    asset_groups = {}
    
    for asset_entry in asset_entries:
        prefix = asset_entry.prefix
        try:
            group = asset_groups[prefix]
        except KeyError:
            group = AssetGroup(prefix)
            asset_groups[prefix] = group
        
        group.add_entry(asset_entry)
    
    return asset_groups


def convert_assets(directory, asset_groups):
    """
    Converts the assets that have bad format.
    
    Parameters
    ----------
    directory : `str`
        The directory where the files are located.
    
    asset_groups : `dict<str, AssetGroup>`
        The grouped assets.
    """
    for asset_group in asset_groups.values():
        while True:
            asset = asset_group.pop_first_incorrect_asset()
            if asset is None:
                break
            
            best_fit_index = asset_group.find_best_fit_index()
            
            for postfix in asset.iter_postfix_variants():
                old_asset_entry = AssetEntry(asset_group.prefix, asset.index, postfix, asset.extension)
                new_asset_entry = AssetEntry(asset_group.prefix, best_fit_index, postfix, 'png')
                
                old_file_name = old_asset_entry.reconstruct_file_name()
                new_file_name = new_asset_entry.reconstruct_file_name()
                
                old_path = join_paths(directory, old_file_name)
                new_path = join_paths(directory, new_file_name)
                
                notify(f'Converting: {old_file_name} -> {new_file_name}')
                Image.open(old_path).save(new_path, format = 'png')
                notify(f'Converting: {old_file_name} -> {new_file_name} (success)')
                delete_file(old_path)
                
                asset_group.add_entry(new_asset_entry)
