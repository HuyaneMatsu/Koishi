__all__ = (
    'check_auto_cancellation_conditions', 'produce_auto_cancellation_conditions',
    'produce_auto_cancellation_conditions_listing'
)

from math import floor

from ...unit_core import produce_kilogram

from .auto_cancellation_condition_ids import (
    AUTO_CANCELLATION_CONDITION_ID_EQUAL, AUTO_CANCELLATION_CONDITION_ID_GREATER_OR_EQUAL,
    AUTO_CANCELLATION_CONDITION_ID_GREATER_THAN, AUTO_CANCELLATION_CONDITION_ID_LESS_OR_EQUAL,
    AUTO_CANCELLATION_CONDITION_ID_LESS_THAN, AUTO_CANCELLATION_CONDITION_ID_NOT_EQUAL
)


def _produce_single_condition(auto_cancellation_condition, value_name, percentage, value_producer):
    """
    Produces a single condition.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    auto_cancellation_condition : ``AutoCancellationCondition``
        The condition to produce.
    
    value_name : `str`
        The name of the value.
    
    percentage : `bool`
        Whether this field is a percentage.
    
    value_producer : `None | GeneratorFunctionType`
        Custom value producer.
    
    Yields
    ------
    part : `str`
    """
    yield value_name
    yield ' '
    
    condition = auto_cancellation_condition.condition
    if condition == AUTO_CANCELLATION_CONDITION_ID_LESS_THAN:
        sign = '<'
    elif condition == AUTO_CANCELLATION_CONDITION_ID_LESS_OR_EQUAL:
        sign = '<='
    elif condition == AUTO_CANCELLATION_CONDITION_ID_EQUAL:
        sign = '=='
    elif condition == AUTO_CANCELLATION_CONDITION_ID_NOT_EQUAL:
        sign = '!='
    elif condition == AUTO_CANCELLATION_CONDITION_ID_GREATER_OR_EQUAL:
        sign = '>='
    elif condition == AUTO_CANCELLATION_CONDITION_ID_GREATER_THAN:
        sign = '>'
    else:
        sign = '?'
    
    yield sign
    yield ' '
    
    threshold = auto_cancellation_condition.threshold
    if value_producer is None:
        yield str(threshold)
    else:
        yield from value_producer(threshold)
    
    if percentage:
        yield ' %'


def _produce_single_condition_functional(auto_cancellation_condition_functional, value_name):
    """
    Produces a single condition.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    auto_cancellation_condition_functional : ``None | AutoCancellationConditionFunctional``
        The condition to produce.
    
    value_name : `str`
        The name of the value.
    
    Yields
    ------
    part : `str`
    """
    yield value_name
    yield ': '
    yield auto_cancellation_condition_functional.name


def produce_auto_cancellation_conditions(auto_cancellation):
    """
    Produces auto cancellation conditions.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    auto_cancellation : ``AutoCancellation``
        Auto cancellation to produce its conditions.
    
    Yields
    ------
    part : `str`
    """
    field_added = False
    
    condition = auto_cancellation.inventory_flat
    if (condition is not None):
        field_added = True
        
        yield from _produce_single_condition(condition, 'inventory', False, produce_kilogram)
    
    condition = auto_cancellation.inventory_percentage
    if (condition is not None):
        if field_added:
            yield ' or '
        else:
            field_added = True
        
        yield from _produce_single_condition(condition, 'inventory', True, None)
    
    condition = auto_cancellation.health_flat
    if (condition is not None):
        if field_added:
            yield ' or '
        else:
            field_added = True
        
        yield from _produce_single_condition(condition, 'health', False, None)
    
    condition = auto_cancellation.health_percentage
    if (condition is not None):
        if field_added:
            yield ' or '
        else:
            field_added = True
        
        yield from _produce_single_condition(condition, 'health', True, None)
    
    condition = auto_cancellation.energy_flat
    if (condition is not None):
        if field_added:
            yield ' or '
        else:
            field_added = True
        
        yield from _produce_single_condition(condition, 'energy', False, None)
    
    condition = auto_cancellation.energy_percentage
    if (condition is not None):
        if field_added:
            yield ' or '
        else:
            field_added = True
        
        yield from _produce_single_condition(condition, 'energy', True, None)
    
    condition = auto_cancellation.looted_items
    if (condition is not None):
        if field_added:
            yield ' or '
        else:
            field_added = True
        
        yield from _produce_single_condition_functional(condition, 'looted items')
    
    if not field_added:
        yield 'none'


def produce_auto_cancellation_conditions_listing(auto_cancellation, indent_prefix):
    """
    Produces the auto cancellation's conditions in a listing form.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    auto_cancellation : ``AutoCancellation``
        Auto cancellation to produce its conditions.
    
    indent_prefix : `None | str`
        Prefix to add before every line.
    
    Yields
    ------
    part : `str`
    """
    if (indent_prefix is not None):
        yield indent_prefix
    yield '- name: '
    yield auto_cancellation.name
    
    condition = auto_cancellation.inventory_flat
    if (condition is not None):
        yield '\n'
        if (indent_prefix is not None):
            yield indent_prefix
        yield '- '
        yield from _produce_single_condition(condition, 'inventory', False, produce_kilogram)
    
    condition = auto_cancellation.inventory_percentage
    if (condition is not None):
        yield '\n'
        if (indent_prefix is not None):
            yield indent_prefix
        yield '- '
        yield from _produce_single_condition(condition, 'inventory', True, None)
    
    condition = auto_cancellation.health_flat
    if (condition is not None):
        yield '\n'
        if (indent_prefix is not None):
            yield indent_prefix
        yield '- '
        yield from _produce_single_condition(condition, 'health', False, None)
    
    condition = auto_cancellation.health_percentage
    if (condition is not None):
        yield '\n'
        if (indent_prefix is not None):
            yield indent_prefix
        yield '- '
        yield from _produce_single_condition(condition, 'health', True, None)
    
    condition = auto_cancellation.energy_flat
    if (condition is not None):
        yield '\n'
        if (indent_prefix is not None):
            yield indent_prefix
        yield '- '
        yield from _produce_single_condition(condition, 'energy', False, None)
    
    condition = auto_cancellation.energy_percentage
    if (condition is not None):
        yield '\n'
        if (indent_prefix is not None):
            yield indent_prefix
        yield '- '
        yield from _produce_single_condition(condition, 'energy', True, None)
    
    condition = auto_cancellation.looted_items
    if (condition is not None):
        yield '\n'
        if (indent_prefix is not None):
            yield indent_prefix
        yield '- '
        yield from _produce_single_condition_functional(condition, 'looted items')


def _check_condition_flat_succeeds(auto_cancellation_condition, total, exhausted):
    """
    Checks whether a flat condition succeeds
    
    Parameters
    ----------
    auto_cancellation_condition : ``None | AutoCancellationCondition``
        The condition to produce.
    
    total : `int`
        The total amount
    
    exhausted : `int`
        The exhausted amount.
    
    Returns
    -------
    succeeds : `bool`
    """
    if auto_cancellation_condition is None:
        return False
    
    return _check_condition_condition(
        auto_cancellation_condition.condition,
        total - exhausted,
        auto_cancellation_condition.threshold,
    )


def _check_condition_percentage_succeeds(auto_cancellation_condition, total, exhausted):
    """
    Checks whether a flat condition succeeds
    
    Parameters
    ----------
    auto_cancellation_condition : ``None | AutoCancellationCondition``
        The condition to check.
    
    total : `int`
        The total amount
    
    exhausted : `int`
        The exhausted amount.
    
    Returns
    -------
    succeeds : `bool`
    """
    if auto_cancellation_condition is None:
        return False
    
    return _check_condition_condition(
        auto_cancellation_condition.condition,
        floor((total - exhausted) * 100 / total),
        auto_cancellation_condition.threshold,
    )


def _check_condition_condition(condition, value, threshold):
    """
    Checks whether a condition's condition succeeds for the given value.
    
    Parameters
    ----------
    condition : `int`
        Condition identifier.
    
    value : `int`
        Value to compare.
    
    threshold : `int`
        Threshold value to fail at.
    
    Returns
    -------
    succeeds : `bool`
    """
    if condition == AUTO_CANCELLATION_CONDITION_ID_LESS_THAN:
        succeeds = value < threshold
    elif condition == AUTO_CANCELLATION_CONDITION_ID_LESS_OR_EQUAL:
        succeeds = value <= threshold
    elif condition == AUTO_CANCELLATION_CONDITION_ID_EQUAL:
        succeeds = value == threshold
    elif condition == AUTO_CANCELLATION_CONDITION_ID_NOT_EQUAL:
        succeeds = value != threshold
    elif condition == AUTO_CANCELLATION_CONDITION_ID_GREATER_OR_EQUAL:
        succeeds = value >= threshold
    elif condition == AUTO_CANCELLATION_CONDITION_ID_GREATER_THAN:
        succeeds = value > threshold
    else:
        succeeds = False
    
    return succeeds


def _check_condition_functional(auto_cancellation_condition_functional, data):
    """
    Checks custom condition.
    
    Parameters
    ----------
    auto_cancellation_condition_functional : ``None | AutoCancellationConditionFunctional``
        Condition to check.
    
    data : `object`
        Data to test with.
    
    Returns
    -------
    succeeds : `bool`
    """
    if auto_cancellation_condition_functional is None:
        return False
    
    return auto_cancellation_condition_functional.function(data)


def check_auto_cancellation_conditions(
    auto_cancellation,
    inventory_total,
    inventory_exhausted,
    health_total,
    health_exhausted,
    energy_total,
    energy_exhausted,
    looted_items,
):
    """
    Checks whether any condition succeeds.
    
    Parameters
    ----------
    auto_cancellation : ``AutoCancellation``
        Auto cancellation.
    
    inventory_total : `int`
        The total inventory of the user.
    
    inventory_exhausted : `int`
        The exhausted inventory of the user.
    
    health_total : `int`
        The total health of the user.
    
    health_exhausted : `int`
        The exhausted health of the user.
    
    energy_total : `int`
        The total energy of the user.
    
    energy_exhausted : `int`
        The exhausted energy of the user.
    
    looted_items : `list<(int, int, int)>`
        A list of tuple of 3 elements: loot state, item id and given amount.
    
    Returns
    -------
    succeeds : `bool`
    """
    return (
        _check_condition_flat_succeeds(
            auto_cancellation.inventory_flat, inventory_total, inventory_exhausted
        ) or
        _check_condition_percentage_succeeds(
            auto_cancellation.inventory_percentage, inventory_total, inventory_exhausted
        ) or
        _check_condition_flat_succeeds(
            auto_cancellation.health_flat, health_total, health_exhausted
        ) or
        _check_condition_percentage_succeeds(
            auto_cancellation.health_percentage, health_total, health_exhausted
        ) or
        _check_condition_flat_succeeds(
            auto_cancellation.energy_flat, energy_total, energy_exhausted
        ) or
        _check_condition_percentage_succeeds(
            auto_cancellation.energy_percentage, energy_total, energy_exhausted
        ) or
        _check_condition_functional(
            auto_cancellation.looted_items, looted_items,
        )
    )
