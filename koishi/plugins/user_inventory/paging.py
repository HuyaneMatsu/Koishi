__all__ = ()

from math import ceil

from .constants import PAGE_SIZE, SORT_ORDER_INCREASING
from .item_entry_sorting import SORT_FUNCTION_DEFAULT, SORT_FUNCTIONS 


def get_inventory_page(inventory, sort_by, sort_order, page_index):
    """
    Gets a page of the inventory.
    
    Parameters
    ----------
    inventory : ``Inventory``
        The user's inventory.
    
    sort_by : `int`
        Identifier to determine how item entries should be sorted.
    
    sort_order : `int`
        Identifier to determine sorting order.
    
    page_index : `int`
        The current page's index.
    
    Returns
    -------
    item_entries_and_page_count : `(list<ItemEntry>, int)`
    """
    item_entries = sorted(
        inventory.iter_item_entries(),
        key = SORT_FUNCTIONS.get(sort_by, SORT_FUNCTION_DEFAULT),
        reverse = (sort_order != SORT_ORDER_INCREASING),
    )
    page_count = ceil(len(item_entries) / PAGE_SIZE)
    item_entries = item_entries[page_index * PAGE_SIZE : (page_index + 1) * PAGE_SIZE]
    
    return item_entries, page_count
