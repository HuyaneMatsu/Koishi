__all__ = ()

from re import I as re_ignore_case, compile as re_compile, escape as re_escape

from ..item_core import ITEMS

from .constants import DISABLED_ITEM_FLAGS


def item_category_to_required_flags(item_category):
    """
    Converts the item category to required flags to use for filtering.
    
    Parameters
    ----------
    item_category : `None | str`
        The given item category.
    
    Returns
    -------
    required_flags : `int`
    """
    while True:
        if item_category is None:
            required_flags = 0
            break
        
        try:
            required_flags = int(item_category, 16)
        except ValueError:
            required_flags = 0
            break
        
        break
    
    return required_flags


def get_best_matching_item(required_flags, value):
    """
    Gets the best matching item.
    
    Parameters
    ----------
    required_flags : `int`
        Flags the item should have.
    
    value : `None | str`
        Value the user typed.
    
    Returns
    -------
    item : ``None | Item``
    """
    if value is None:
        return None
    
    if not required_flags:
        required_flags = ~0
    
    try:
        item_id = int(value, 16)
    except ValueError:
        pass
    else:
        try:
            item = ITEMS[item_id]
        except KeyError:
            pass
        else:
            flags = item.flags
            if (not flags & DISABLED_ITEM_FLAGS) and (flags & required_flags):
                return item
    
    pattern = re_compile('.*?'.join(re_escape(character) for character in value), re_ignore_case)
    
    best_item = None
    best_match_rate = (1 << 63, 1 << 63, '', 0)
    
    for item in ITEMS.values():
        flags = item.flags
        if (flags & DISABLED_ITEM_FLAGS) or (not flags & required_flags):
            continue
        
        match = pattern.search(item.name)
        if (match is None):
            continue
        
        match_start = match.start()
        match_rate = (match_start, match.end() - match_start, item.name, item.id)
        
        if best_match_rate <= match_rate:
            continue
        
        best_item = item
        best_match_rate = match_rate
        continue
    
    return best_item


def get_item_name_suggestions(required_flags, value):
    """
    Creates suggestions for the best matching items.
    
    Parameters
    ----------
    required_flags : `int`
        Flags the item should have.
    
    value : `None | str`
        Value the user typed.
    
    Returns
    -------
    item : ``None | list<(str, str)>``
    """
    if not required_flags:
        required_flags = ~0
    
    if value is None:
        items_with_match_rates = []
        
        for item in ITEMS.values():
            flags = item.flags
            if (flags & DISABLED_ITEM_FLAGS) or (not flags & required_flags):
                continue
            
            items_with_match_rates.append((item.name, item.id))
            continue
        
        items_with_match_rates.sort()
        del items_with_match_rates[24:]
        return [
            ('all', format(0, 'x')),
            *((item_name, format(item_id, 'x')) for item_name, item_id in items_with_match_rates)
        ]
    
    try:
        item_id = int(value, 16)
    except ValueError:
        pass
    else:
        try:
            item = ITEMS[item_id]
        except KeyError:
            pass
        else:
            flags = item.flags
            if (not flags & DISABLED_ITEM_FLAGS) and (flags & required_flags):
                return [(item.name, format(item.id, 'x'))]
    
    pattern = re_compile('.*?'.join(re_escape(character) for character in value), re_ignore_case)
    items_with_match_rates = []
    
    for item in ITEMS.values():
        flags = item.flags
        if (flags & DISABLED_ITEM_FLAGS) or (not flags & required_flags):
            continue
        
        match = pattern.search(item.name)
        if (match is None):
            continue
        
        match_start = match.start()
        match_length = match.end() - match_start
        
        items_with_match_rates.append((match_start, match_length, item.name, item.id))
    
    if not items_with_match_rates:
        return None
    
    items_with_match_rates.sort()
    del items_with_match_rates[25:]
    return [(item[2], format(item[3], 'x')) for item in items_with_match_rates]
