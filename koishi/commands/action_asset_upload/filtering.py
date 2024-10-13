__all__ = ()

from ..action_asset_format_converter.constants import EXTENSIONS_TO_CONVERT


def get_image_detail_names(action_image_handler):
    """
    Get the image details names of the given action image handler.
    
    Parameters
    ----------
    action_image_handler : ``ImageHandlerStatic``
        Action image handler.
    
    Returns
    -------
    image_detail_names : `set<str>`
    """
    return {image_detail.name for image_detail in action_image_handler._images}


def get_image_detail_tags(action_image_handler):
    """
    Get image detail tags used in the given action image handler.
    
    Parameters
    ----------
    action_image_handler : ``ImageHandlerStatic``
        Action image handler.
    
    Returns
    -------
    action_tags : `set<str>`
    """
    action_tags = set()
    
    for image_detail in action_image_handler._images:
        image_detail_actions = image_detail.actions
        if image_detail_actions is None:
            continue
        
        for image_detail_actions in image_detail_actions:
            action_tags.add(image_detail_actions.tag)
    
    return action_tags


def filter_new_asset_entries(asset_entries, registered_image_names):
    """
    Filters out the new asset entries from the given ones.
    
    Parameters
    ----------
    asset_entries : `list<AssetEntry>`
        Asset entries to filter from.
    
    Returns
    -------
    filtered_down_entries : `list<AssetEntry>`
    """
    filtered_down_entries = []
    
    for asset_entry in asset_entries:
        # Exclude entries that are variants.
        if asset_entry.postfix is not None:
            continue
        
        # Exclude entries to be converted first.
        if asset_entry.extension in EXTENSIONS_TO_CONVERT:
            continue
        
        # Exclude entries that are already uploaded.
        if asset_entry.name in registered_image_names:
            continue
        
        filtered_down_entries.append(asset_entry)
    
    return filtered_down_entries


def classify_asset_entry_parts(asset_entry, registered_action_tags, touhou_character_getter):
    """
    Classifies the parts of an action asset's prefix.
    
    Parameters
    ----------
    asset_entry : ``AssetEntry``
        The asset entry to classify.
    
    registered_action_tags : `set<str>`
        The registered action tags that can be picked up.
    
    touhou_character_getter : `FunctionType`
        Function to identify touhou character by their name.
    
    Returns
    -------
    characters : `None | set<TouhouCharacter>`
        Touhou characters.
    
    action_tags : `None | set<str>
        Action tags.
    
    unidentified : `None | set<str>`
        Unidentified name parts.
    """
    characters = None
    action_tags = None
    unidentified = None
    
    for part in asset_entry.prefix.split('-'):
        # try match tag
        if part in registered_action_tags:
            if action_tags is None:
                action_tags = set()
            
            action_tags.add(part)
            continue
        
        # try match character
        character = touhou_character_getter(part)
        if (character is not None):
            if characters is None:
                characters = set()
            characters.add(character)
            continue
        
        if unidentified is None:
            unidentified = set()
        
        unidentified.add(part)
        continue
    
    return characters, action_tags, unidentified
