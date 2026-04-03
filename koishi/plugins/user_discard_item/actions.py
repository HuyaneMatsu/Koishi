__all__ = ()

from ..inventory_core import get_inventory, save_inventory, select_item


async def discard_item(user_id, value, amount):
    """
    Discard an item.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        The user's identifier.
    
    value : `str`
        The item's name to select.
    
    amount : `int`
        The amount of items to be discarded.
    
    Returns
    -------
    item_and_discard_amount_and_new_amount : `(None | Item, int, int)`
    """
    inventory = await get_inventory(user_id)
    item = select_item(inventory, 0, value)
    if item is None:
        return None, 0, 0
    
    old_amount = inventory.get_item_amount(item)
    if amount <= 0:
        return item, 0, old_amount
    
    new_amount = inventory.modify_item_amount(item, -amount)
    await save_inventory(inventory)
    
    return item, old_amount - new_amount, new_amount
