__all__ = ()

from re import I as re_ignore_case, compile as re_compile, escape as re_escape

from ..adventure_core import ACTIONS
from ..item_core import get_item_nullable


def _item_by_name_sort_key(item):
    """
    Sort key.
    
    Parameters
    ----------
    item : ``Item``
        Item to sort.
    
    Returns
    -------
    sort_key : `str`
    """
    return item.name


def _item_match_sort_key(item):
    """
    Sort key.
    
    Parameters
    ----------
    item : ``tuple<Item, (int, int, str)>``
        The item and it's match rate.
    
    Returns
    -------
    match_rate : `(int, int, str)`
    """
    return item[1]


def get_matching_items(action_ids, value):
    """
    Gets matching items.
    
    Parameters
    ----------
    action_ids : `tuple<int>`
        Actions identifier that can happen at a target.
    
    value : `None | str`
        Value that the user already typed in.
    
    Returns
    -------
    items : ``None | list<Item>``
    """
    items = None
    
    for action_id in action_ids:
        try:
            action = ACTIONS[action_id]
        except KeyError:
            continue
        
        loot = action.loot
        if (loot is None):
            continue
        
        for option in loot:
            item = get_item_nullable(option.item_id)
            
            if items is None:
                items = []
            elif item in items:
                continue
            
            items.append(item)
            continue
    
    if (items is None):
        return
    
    if (value is not None):
        try:
            item_id = int(value, 16)
        except ValueError:
            pass
        else:
            for item in items:
                if item.id == item_id:
                    return [item]
    
    if (value is None):
        return sorted(items, key = _item_by_name_sort_key)
    
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
    return [item[0] for item in matches]


def get_goal_item_suggestions(action_ids, value):
    """
    Gets goal item suggestions.
    
    Parameters
    ----------
    action_ids : `tuple<int>`
        Actions identifier that can happen at a target.
    
    value : `None | str`
        Value that the user already typed in.
    
    Returns
    -------
    suggestions : `None | list<(str, str)>`
    """
    items = get_matching_items(action_ids, value)
    if (items is not None):
        return [(item.name, format(item.id, 'x')) for item in items]


def get_best_matching_goal_item(action_ids, value):
    """
    Gets the best matching goal item.
    
    Parameters
    ----------
    action_ids : `tuple<int>`
        Actions identifier that can happen at a target.
    
    value : `None | str`
        Value that the user already typed in.
    
    Returns
    -------
    item : ``None | Item``
    """
    items = get_matching_items(action_ids, value)
    if (items is not None):
        return items[0]
