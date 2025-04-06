__all__ = ('accumulate_modifier_values', 'apply_modifiers')

from .helpers import construct_modifier_type
from .modifier_kinds import MODIFIER_KIND__FLAT, MODIFIER_KIND__PERCENT


def accumulate_modifier_values(*items):
    """
    Accumulates the modifier values into a single dictionary.
    
    Parameters
    ----------
    *items : `None | Item`
        The items to accumulate the values from.
    
    Returns
    -------
    accumulated_modifiers : `dict<int, int>`
    """
    modifiers = {}
    
    for item in items:
        if item is None:
            continue
        
        for modifier in item.iter_modifiers():
            modifier_type = modifier.type
            modifiers[modifier_type] = modifiers.get(modifier_type, 0) + modifier.amount
    
    return modifiers


def apply_modifiers(value, accumulated_modifiers, modifier_id):
    """
    Applies the modifiers for the given value.
    
    Parameters
    ----------
    value : `int`
        The current value.
    
    accumulated_modifiers : `dict<int, int>`
        The accumulated modifiers into a single dictionary.
    
    modifier_id : `int`
        The modifier identifiers that are affected.
    
    Returns
    -------
    value : `int`
    """
    try:
        amount = accumulated_modifiers[construct_modifier_type(modifier_id, MODIFIER_KIND__FLAT)]
    except KeyError:
        pass
    else:
        value += amount
    
    try:
        amount = accumulated_modifiers[construct_modifier_type(modifier_id, MODIFIER_KIND__PERCENT)]
    except KeyError:
        pass
    else:
        value = value * (100 + amount) // 100
    
    return value
