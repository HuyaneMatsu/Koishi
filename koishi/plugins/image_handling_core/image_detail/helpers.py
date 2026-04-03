__all__ = ()


def _merge_values_with_value(old_values, value):
    """
    Merges a single value to the other ones.
    
    Parameters
    ----------
    old_values : `None | tuple<object>`
        Values to merge to.
    value : `object`
        Value to merge.
    
    Returns
    -------
    new_values : `tuple<object>`
    """
    if old_values is None:
        return (value,)
    
    if value in old_values:
        return old_values
    
    new_values = [*old_values, value]
    new_values.sort()
    return tuple(new_values)


def _merge_values_with_values(old_values, values):
    """
    Merges a single value to the other ones.
    
    Parameters
    ----------
    old_values : `None | tuple<object>`
        Values to merge to.
    values : `sequence<object>`
        Values to merge with.
    
    Returns
    -------
    new_values : `None | tuple<object>`
    """
    if not values:
        return old_values
    
    if old_values is None:
        new_values = [*{*values}]
        new_values.sort()
        return tuple(new_values)
    
    new_values = [*{*old_values, *values}]
    new_values.sort()
    return tuple(new_values)
