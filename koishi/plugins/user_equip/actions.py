__all__ = ('equip_item', 'get_equip_item_suggestions', 'unequip_item')

from ..inventory_core import create_item_suggestions, get_inventory, save_inventory, select_item
from ..item_core import ITEM_FLAG_HEAD, ITEM_FLAG_COSTUME, get_item_nullable
from ..user_stats_core import get_user_stats

from .constants import ITEM_FLAGS_ALLOWED


async def get_equip_item_suggestions(user_id, item_flag, value):
    """
    Gets item suggestions for the given value.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        The user's identifier.
    
    item_flag : `int`
        The item flag to filter for.
    
    value : `None | str`
        Value to filter for.
    
    Returns
    -------
    suggestions : `None | list<(str, int)>`
    """
    if item_flag not in ITEM_FLAGS_ALLOWED:
        return
    
    inventory = await get_inventory(user_id)
    return create_item_suggestions(inventory, item_flag, value)


async def equip_item(user_id, item_flag, value):
    """
    Equips an item.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        The user's identifier.
    
    item_flag : `int`
        The item flag to filter for.
    
    value : `str`
        The item's name to select.
    
    Returns
    -------
    old_and_new_item : `(None | Item, None | Item)`
    """
    if item_flag not in ITEM_FLAGS_ALLOWED:
        return None, None
    
    inventory = await get_inventory(user_id)
    item = select_item(inventory, item_flag, value)
    if item is None:
        return None, None
    
    stats = await get_user_stats(user_id)
    
    if item_flag == ITEM_FLAG_HEAD:
        old_item_id = stats.item_id_head
        field_name = 'item_id_head'
    
    elif item_flag == ITEM_FLAG_COSTUME:
        old_item_id = stats.item_id_costume
        field_name = 'item_id_costume'
    
    else:
        old_item_id = stats.item_id_weapon
        field_name = 'item_id_weapon'
    
    old_item = get_item_nullable(old_item_id)
    if (old_item is not item):
        if (old_item is not None):
            inventory.modify_item_amount(old_item, +1)
        
        inventory.modify_item_amount(item, -1)
        
        stats.set(field_name, item.id)
        
        await stats.save()
        await save_inventory(inventory)
    
    return old_item, item


async def unequip_item(user_id, item_flag):
    """
    Unequips an item.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        The user's identifier.
    
    item_flag : `int`
        The item type to unequip.
    
    Returns
    -------
    old_item : ``None | Item``
    """
    if item_flag not in ITEM_FLAGS_ALLOWED:
        return None
    
    stats = await get_user_stats(user_id)
    
    if item_flag == ITEM_FLAG_HEAD:
        old_item_id = stats.item_id_head
        field_name = 'item_id_head'
    
    elif item_flag == ITEM_FLAG_COSTUME:
        old_item_id = stats.item_id_costume
        field_name = 'item_id_costume'
    
    else:
        old_item_id = stats.item_id_weapon
        field_name = 'item_id_weapon'
    
    old_item = get_item_nullable(old_item_id)
    if (old_item is not None):
        inventory = await get_inventory(user_id)
        inventory.modify_item_amount(old_item, +1)
    
        stats.set(field_name, 0)
        
        await stats.save()
        await save_inventory(inventory)
    
    return old_item
