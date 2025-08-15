__all__ = ()

from scarletio import RichAttributeErrorBaseType


class LootAccumulation(RichAttributeErrorBaseType):
    """
    Represents the accumulated loot value for an item.
    
    Parameters
    ----------
    amount : `int`
        Accumulated amount.
    
    duration_cost : `int`
        Accumulated duration cost.
    
    energy_cost : `int`
        Accumulated energy cost.
    """
    __slots__ = ('amount', 'duration_cost', 'energy_cost')
    
    def __new__(cls, amount, duration_cost, energy_cost):
        """
        Creates a new loot accumulator.
        
        Parameters
        ----------
        amount : `int`
            Accumulated amount.
        
        duration_cost : `int`
            Accumulated duration cost.
        
        energy_cost : `int`
            Accumulated energy cost.
        """
        self = object.__new__(cls)
        self.amount = amount
        self.duration_cost = duration_cost
        self.energy_cost = energy_cost
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # amount
        repr_parts.append(' amount = ')
        repr_parts.append(repr(self.amount))
        
        # duration_cost
        repr_parts.append(' duration_cost = ')
        repr_parts.append(repr(self.duration_cost))
        
        # energy_cost
        repr_parts.append(' energy_cost = ')
        repr_parts.append(repr(self.energy_cost))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns self == other."""
        if type(self) is not type(other):
            return NotImplemented
        
        # amount
        if self.amount != other.amount:
            return False
        
        # duration_cost
        if self.duration_cost != other.duration_cost:
            return False
        
        # energy_cost
        if self.energy_cost != other.energy_cost:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns hash(self)."""
        hash_value = 0
        
        # amount
        hash_value ^= self.amount
        
        # duration_cost
        hash_value ^= self.duration_cost << 8
        
        # energy_cost
        hash_value ^= self.energy_cost << 16
        
        return hash_value   
    
    
    def copy(self):
        """
        Copies the loot accumulation.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.amount = self.amount
        new.duration_cost = self.duration_cost
        new.energy_cost = self.energy_cost
        return new
