__all__ = ()

from .constants import (
    SORT_BY_AMOUNT, SORT_BY_CUMULATIVE_VALUE, SORT_BY_CUMULATIVE_WEIGHT, SORT_BY_NAME, SORT_BY_TYPE, SORT_BY_VALUE,
    SORT_BY_WEIGHT
)


def sort_function_by_name(item_entry):
    """
    By name sort key getter.
    
    Parameters
    ----------
    item_entry : ``ItemEntry``
        Item entry to get sort key of.
    
    Returns
    -------
    sort_key : `str`
    """
    return item_entry.item.name


def sort_function_by_amount(item_entry):
    """
    By amount sort key getter.
    
    Parameters
    ----------
    item_entry : ``ItemEntry``
        Item entry to get sort key of.
    
    Returns
    -------
    sort_key : `int`
    """
    return item_entry.amount


def sort_function_by_value(item_entry):
    """
    By value sort key getter.
    
    Parameters
    ----------
    item_entry : ``ItemEntry``
        Item entry to get sort key of.
    
    Returns
    -------
    sort_key : `int`
    """
    return item_entry.item.value


def sort_function_by_weight(item_entry):
    """
    By weight sort key getter.
    
    Parameters
    ----------
    item_entry : ``ItemEntry``
        Item entry to get sort key of.
    
    Returns
    -------
    sort_key : `int`
    """
    return item_entry.item.weight


def sort_function_by_type(item_entry):
    """
    By type (flags) sort key getter.
    
    Parameters
    ----------
    item_entry : ``ItemEntry``
        Item entry to get sort key of.
    
    Returns
    -------
    sort_key : `int`
    """
    return item_entry.item.flags


def sort_function_by_cumulative_value(item_entry):
    """
    By cumulative value (amount * value) sort key getter.
    
    Parameters
    ----------
    item_entry : ``ItemEntry``
        Item entry to get sort key of.
    
    Returns
    -------
    sort_key : `int`
    """
    return item_entry.amount * item_entry.item.value


def sort_function_by_cumulative_weight(item_entry):
    """
    By cumulative weight (amount * value) sort key getter.
    
    Parameters
    ----------
    item_entry : ``ItemEntry``
        Item entry to get sort key of.
    
    Returns
    -------
    sort_key : `int`
    """
    return item_entry.amount * item_entry.item.weight


SORT_FUNCTION_DEFAULT = sort_function_by_name
SORT_FUNCTIONS = {
    SORT_BY_NAME : sort_function_by_name,
    SORT_BY_AMOUNT : sort_function_by_amount,
    SORT_BY_VALUE : sort_function_by_value,
    SORT_BY_WEIGHT : sort_function_by_weight,
    SORT_BY_TYPE : sort_function_by_type,
    SORT_BY_CUMULATIVE_VALUE : sort_function_by_cumulative_value,
    SORT_BY_CUMULATIVE_WEIGHT : sort_function_by_cumulative_weight,
}
