__all__ = ()

from .constants import (
    AUTOMATION_REACTION_ROLE_ENTRY_DATA_VERSION_1_HEAD_STRUCT,
    AUTOMATION_REACTION_ROLE_ENTRY_DATA_VERSION_1_ROLE_IDS_STRUCT
)
from .automation_reaction_role_item import AutomationReactionRoleItem


def _unpack_items_version_1(data):
    """
    Unpacks version 1 auto react role items.
    
    Parameters
    ----------
    data : `None | bytes`
        Data to unpack from.
    
    Returns
    -------
    items : ``None | list<AutomationReactionRoleItem>``
    """
    if (data is None):
        return None
    
    items = []
    
    chunk_start = 0
    data_length = len(data)
    data = memoryview(data)
    while chunk_start < data_length:
        chunk_end = chunk_start + AUTOMATION_REACTION_ROLE_ENTRY_DATA_VERSION_1_HEAD_STRUCT.size
        emoji_id, add_role_count, remove_role_count = AUTOMATION_REACTION_ROLE_ENTRY_DATA_VERSION_1_HEAD_STRUCT.unpack(
            data[chunk_start : chunk_end],
        )
        if not add_role_count:
            add_role_ids = None
        else:
            chunk_start = chunk_end
            chunk_end = (
                chunk_start + add_role_count * AUTOMATION_REACTION_ROLE_ENTRY_DATA_VERSION_1_ROLE_IDS_STRUCT.size
            )
            add_role_ids = (*(
                element[0] for element in AUTOMATION_REACTION_ROLE_ENTRY_DATA_VERSION_1_ROLE_IDS_STRUCT.iter_unpack(
                    data[chunk_start : chunk_end]
                )
            ),)
            
        if not remove_role_count:
            remove_role_ids = None
        else:
            chunk_start = chunk_end
            chunk_end = (
                chunk_start + remove_role_count * AUTOMATION_REACTION_ROLE_ENTRY_DATA_VERSION_1_ROLE_IDS_STRUCT.size
            )
            remove_role_ids = (*(
                element[0] for element in AUTOMATION_REACTION_ROLE_ENTRY_DATA_VERSION_1_ROLE_IDS_STRUCT.iter_unpack(
                    data[chunk_start : chunk_end]
                )
            ),)
        
        chunk_start = chunk_end
        items.append(AutomationReactionRoleItem(emoji_id, add_role_ids, remove_role_ids))
        continue
    
    return items


def unpack_items(data, data_version):
    """
    Unpacks an auto react role item.
    
    Parameters
    ----------
    data : `None | bytes`
        Data to unpack from.
    
    data_version : `int`
        Serialization version.
    
    Returns
    -------
    items : ``None | list<AutomationReactionRoleItem>``
    """
    if data_version == 1:
        return _unpack_items_version_1(data)


def _pack_items_version_1(items):
    """
    Packs version 1 auto react role item.
    
    Parameters
    ----------
    items : ``None | list<AutomationReactionRoleItem>``
        Items to pack.
    
    Returns
    -------
    data : `None | bytes`
    """
    if items is None:
        return None
    
    data_parts = []
    
    for item in items:
        add_role_ids = item.add_role_ids
        remove_role_ids = item.remove_role_ids
        
        data_parts.append(AUTOMATION_REACTION_ROLE_ENTRY_DATA_VERSION_1_HEAD_STRUCT.pack(
            item.emoji_id,
            (0 if add_role_ids is None else len(add_role_ids)),
            (0 if remove_role_ids is None else len(remove_role_ids)),
        ))
        
        if (add_role_ids is not None):
            for role_id in add_role_ids:
                data_parts.append(AUTOMATION_REACTION_ROLE_ENTRY_DATA_VERSION_1_ROLE_IDS_STRUCT.pack(role_id))
        
        if (remove_role_ids is not None):
            for role_id in remove_role_ids:
                data_parts.append(AUTOMATION_REACTION_ROLE_ENTRY_DATA_VERSION_1_ROLE_IDS_STRUCT.pack(role_id))
    
    return b''.join(data_parts)


def pack_items(items, data_version):
    """
    Packs auto react role item.
    
    Parameters
    ----------
    items : ``None | list<AutomationReactionRoleItem>``
        Items to pack.
    
    data_version : `int`
        Serialization version.
    
    Returns
    -------
    data : `None | bytes`
    """
    if data_version == 1:
        return _pack_items_version_1(items)
