__all__ = ('check_auto_cancellation_conditions', 'produce_auto_cancellation_conditions',)

from math import floor

from ...item_core import produce_weight

from .auto_cancellation_condition_ids import (
    AUTO_CANCELLATION_CONDITION_ID_EQUAL, AUTO_CANCELLATION_CONDITION_ID_GREATER_OR_EQUAL,
    AUTO_CANCELLATION_CONDITION_ID_GREATER_THAN, AUTO_CANCELLATION_CONDITION_ID_LESS_OR_EQUAL,
    AUTO_CANCELLATION_CONDITION_ID_LESS_THAN, AUTO_CANCELLATION_CONDITION_ID_NOT_EQUAL
)


def _produce_kilogram(value):
    """
    Produces a kilogram value.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    value : `int`
        Weight to produce as kilogram in grams.
    
    Yields
    ------
    part : `str`
    """
    yield from produce_weight(value)
    yield ' kg'


def _produce_single_condition(auto_cancellation_condition, field_added, value_name, percentage, value_producer):
    """
    Produces a single condition.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    auto_cancellation_condition : ``None | AutoCancellationCondition``
        The condition to produce.
    
    field_added : `bool`
        Whether a field was already added.
    
    value_name : `str`
        The name of the value.
    
    percentage : `bool`
        Whether this field is a percentage.
    
    value_producer : `None | GeneratorFunctionType`
        Custom value producer.
    
    Yields
    ------
    part : `str`
    
    Returns
    -------
    field_added : `bool`
    """
    if auto_cancellation_condition is None:
        return field_added
    
    if field_added:
        yield ' or '
    
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
    
    return True


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
    
    field_added = yield from _produce_single_condition(
        auto_cancellation.inventory_flat, field_added, 'inventory', False, _produce_kilogram
    )
    field_added = yield from _produce_single_condition(
        auto_cancellation.inventory_percentage, field_added, 'inventory', True, None
    )
    field_added = yield from _produce_single_condition(
        auto_cancellation.health_flat, field_added, 'health', False, None
    )
    field_added = yield from _produce_single_condition(
        auto_cancellation.health_percentage, field_added, 'health', True, None
    )
    field_added = yield from _produce_single_condition(
        auto_cancellation.energy_flat, field_added, 'energy', False, None
    )
    field_added = yield from _produce_single_condition(
        auto_cancellation.energy_percentage, field_added, 'energy', True, None
    )
    
    if not field_added:
        yield 'none'


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


def check_auto_cancellation_conditions(
    auto_cancellation,
    inventory_total,
    inventory_exhausted,
    health_total,
    health_exhausted,
    energy_total,
    energy_exhausted,
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
        )
    )
