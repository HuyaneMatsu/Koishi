__all__ = ('create_item_suggestions', 'select_item')

from re import I as re_ignore_case, compile as re_compile, escape as re_escape


def _item_match_sort_key(item):
    """
    Sort key used inside of ``Guild.get_items_like`` to sort items based on their match rate.
    
    Parameters
    ----------
    item : `tuple<Emoji, (int, int, str)>`
        The item and it's match rate.
    
    Returns
    -------
    match_rate : `(int, int, str)`
    """
    return item[1]


def _filter_inventory_items_of_type(inventory, item_flag):
    """
    Filters out the inventory items having the given flag.
    
    Parameters
    ----------
    inventory : ``Inventory``
        Inventory to filter from.
    
    item_flag : `int`
        The item flag to filter for.
    
    Returns
    -------
    items : `list<Item>`
    """
    items = []
    for item_entry in inventory.iter_item_entries():
        item = item_entry.item
        if item.flags & item_flag:
            items.append(item)
    
    return items


def _get_inventory_items(inventory):
    """
    Gets the items of the inventory.
    
    Parameters
    ----------
    inventory : ``Inventory``
        Inventory to filter from.
    
    Returns
    -------
    items : `list<Item>`
    """
    return [item_entry.item for item_entry in inventory.iter_item_entries()]


def create_item_suggestions(inventory, item_flag, value):
    """
    Gets item suggestions.
    
    Parameters
    ----------
    inventory : ``Inventory``
        Inventory to filter from.
    
    item_flag : `int`
        The item flag to filter for.
    
    value : `None | str`
        Value to filter for.
    
    Returns
    -------
    suggestions : `None | list<(str, int)>`
    """
    if (value is not None) and value.isdigit():
        item_entry = inventory.get_item_entry_by_id(int(value))
        if item_entry is None:
            return
        
        item = item_entry.item
        return [(item.name, item.id)]
    
    if item_flag:
        items = _filter_inventory_items_of_type(inventory, item_flag)
    else:
        items = _get_inventory_items(inventory)
    
    if not items:
        return
    
    if (value is None):
        items.sort()
        return [(item.name, item.id) for item in items]
    
    item_name_pattern = re_compile('.*?'.join(re_escape(char) for char in value), re_ignore_case)
    
    matches = None
    for item in items:
        item_name = item.name
        parsed = item_name_pattern.search(item_name)
        if parsed is None:
            continue
        
        match_start = parsed.start()
        match_length = parsed.end() - match_start
        
        if matches is None:
            matches = []
        
        matches.append((item, (match_length, match_start, item.name)))
    
    if matches is None:
        return
    
    matches.sort(key = _item_match_sort_key)
    return [(item.name, item.id) for item, match in matches]


def select_item(inventory, item_flag, value):
    """
    Selects the best matching item from the inventory.
    
    Parameters
    ----------
    inventory : ``Inventory``
        Inventory to filter from.
    
    item_flag : `int`
        The item flag to filter for.
    
    value : `str`
        Value to filter for.
    
    Returns
    -------
    item : ``None | Item``
    """
    if value.isdigit():
        item_entry = inventory.get_item_entry_by_id(int(value))
        if item_entry is None:
            return
        
        return item_entry.item
    
    if item_flag:
        items = _filter_inventory_items_of_type(inventory, item_flag)
    else:
        items = _get_inventory_items(inventory)
    
    if not items:
        return
    
    item_name_pattern = re_compile('.*?'.join(re_escape(char) for char in value), re_ignore_case)
    
    accurate_item = None
    accurate_match_key = None
    
    for item in items:
        item_name = item.name
        parsed = item_name_pattern.search(item_name)
        if parsed is None:
            continue
        
        match_start = parsed.start()
        match_length = parsed.end() - match_start
        
        match_rate = (match_length, match_start)
        if (accurate_match_key is not None) and (accurate_match_key < match_rate):
            continue
        
        accurate_item = item
        accurate_match_key = match_rate
    
    return accurate_item
