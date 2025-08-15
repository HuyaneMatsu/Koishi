__all__ = ('AutoCancellation',)

from scarletio import RichAttributeErrorBaseType


class AutoCancellation(RichAttributeErrorBaseType):
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
    
    name : `int`
        The name of the auto cancellation.
    """
    __slots__ = (
        'energy_flat', 'energy_percentage', 'health_flat', 'health_percentage', 'id', 'inventory_flat',
        'inventory_percentage', 'name',
    )
    
    def __new__(
        cls,
        auto_cancellation_id,
        name,
        inventory_flat,
        inventory_percentage,
        health_flat,
        health_percentage,
        energy_flat,
        energy_percentage,
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
        """
        self = object.__new__(cls)
        self.energy_flat = energy_flat
        self.energy_percentage = energy_percentage
        self.health_flat = health_flat
        self.health_percentage = health_percentage
        self.id = auto_cancellation_id
        self.inventory_flat = inventory_flat
        self.inventory_percentage = inventory_percentage
        self.name = name
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # id
        repr_parts.append(' id = ')
        repr_parts.append(repr(self.id))
        
        # name
        repr_parts.append(', name = ')
        repr_parts.append(repr(self.name))
        
        # inventory_flat
        inventory_flat = self.inventory_flat
        if (inventory_flat is not None):
            repr_parts.append(', inventory_flat = ')
            repr_parts.append(repr(inventory_flat))
        
        # inventory_percentage
        inventory_percentage = self.inventory_percentage
        if (inventory_percentage is not None):
            repr_parts.append(', inventory_percentage = ')
            repr_parts.append(repr(inventory_percentage))
        
        # health_flat
        health_flat = self.health_flat
        if (health_flat is not None):
            repr_parts.append(', health_flat = ')
            repr_parts.append(repr(health_flat))
        
        # health_percentage
        health_percentage = self.health_percentage
        if (health_percentage is not None):
            repr_parts.append(', health_percentage = ')
            repr_parts.append(repr(health_percentage))
        
        # inventory_flat
        inventory_flat = self.inventory_flat
        if (inventory_flat is not None):
            repr_parts.append(', inventory_flat = ')
            repr_parts.append(repr(inventory_flat))
        
        # inventory_percentage
        inventory_percentage = self.inventory_percentage
        if (inventory_percentage is not None):
            repr_parts.append(', inventory_percentage = ')
            repr_parts.append(repr(inventory_percentage))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
