__all__ = ('AutoCancellation', 'auto_cancellation_create')

from scarletio import RichType


class AutoCancellation(metaclass = RichType, rich_type_feature_flags = ~0):
    """
    Represents the condition to cancel an event.
    
    Attributes
    ----------
    energy_flat : ``None | AutoCancellationCondition``
        Condition for flat energy based cancellation.
    
    energy_percentage : ``None | AutoCancellationCondition``
        Condition for percentage energy based cancellation.
    
    health_flat : ``None | AutoCancellationCondition``
        Condition for flat health based cancellation.
    
    health_percentage : ``None | AutoCancellationCondition``
        Condition for percentage health based cancellation.
    
    id : `int`
        The identifier of the auto cancellation.
    
    inventory_flat : ``None | AutoCancellationCondition``
        Condition for flat inventory based cancellation.
    
    inventory_percentage : ``None | AutoCancellationCondition``
        Condition for percentage inventory based cancellation.
    
    looted_items : ``None | AutoCancellationConditionFunctional``
        Condition for looted items based cancellation.
    
    name : `int`
        The name of the auto cancellation.
    """
    __slots__ = (
        'energy_flat', 'energy_percentage', 'health_flat', 'health_percentage', 'id', 'inventory_flat',
        'inventory_percentage', 'looted_items', 'name',
    )


def auto_cancellation_create(
    auto_cancellation_id,
    name,
    inventory_flat,
    inventory_percentage,
    health_flat,
    health_percentage,
    energy_flat,
    energy_percentage,
    looted_items,
):
    """
    Creates a new auto cancellation.
    
    Parameters
    ----------
    auto_cancellation_id : `int`
        The identifier for the auto cancellation.
    
    name : `int`
        The name of the auto cancellation.

    inventory_flat : ``None | AutoCancellationCondition``
        Condition for flat inventory based cancellation.
    
    inventory_percentage : ``None | AutoCancellationCondition``
        Condition for percentage inventory based cancellation.
    
    health_flat : ``None | AutoCancellationCondition``
        Condition for flat health based cancellation.
    
    health_percentage : ``None | AutoCancellationCondition``
        Condition for percentage health based cancellation.
    
    energy_flat : ``None | AutoCancellationCondition``
        Condition for flat energy based cancellation.
    
    energy_percentage : ``None | AutoCancellationCondition``
        Condition for percentage energy based cancellation.
    
    looted_items : ``None | AutoCancellationConditionFunctional``
        Condition for looted items based cancellation.
    
    Returns
    -------
    auto_cancellation : ``AutoCancellation``
    """
    auto_cancellation = object.__new__(AutoCancellation)
    auto_cancellation.energy_flat = energy_flat
    auto_cancellation.energy_percentage = energy_percentage
    auto_cancellation.health_flat = health_flat
    auto_cancellation.health_percentage = health_percentage
    auto_cancellation.id = auto_cancellation_id
    auto_cancellation.inventory_flat = inventory_flat
    auto_cancellation.inventory_percentage = inventory_percentage
    auto_cancellation.looted_items = looted_items
    auto_cancellation.name = name
    return auto_cancellation
