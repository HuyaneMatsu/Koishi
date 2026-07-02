__all__ = ('OptionButcher',)

from scarletio import RichAttributeErrorBaseType


class OptionButcher(RichAttributeErrorBaseType):
    """
    Represents an option of butchering.
    
    Attributes
    ----------
    amount : `int`
        Amount given.
    
    chance_in : `int`
        The chance to be chosen in.
    
    chance_out : `int`
        The chance to be chosen out of.
    
    chance_scaling_enabled : `bool`
        Whether the chance should be scaled by the multiplier.
    
    energy_cost_flat : `int`
        The required energy to successfully execute this action.
    
    energy_cost_scaling_failure : `int`
        The required energy for each item given for failure.
    
    energy_cost_scaling_success : `int`
        The required energy for each item given for success.
    
    item_id : `int`
        The given item's identifier.
    """
    __slots__ = (
        'amount', 'chance_in', 'chance_out', 'chance_scaling_enabled', 'energy_cost_flat',
        'energy_cost_scaling_failure', 'energy_cost_scaling_success', 'item_id'
    )
    
    def __new__(
        cls,
        chance_scaling_enabled,
        chance_in,
        chance_out,
        amount,
        item_id,
        energy_cost_flat,
        energy_cost_scaling_success,
        energy_cost_scaling_failure,
    ):
        """
        Creates a new option for butchering.
        
        Parameters
        ----------
        chance_scaling_enabled : `bool`
            Whether the chance should be scaled by the multiplier.
        
        chance_in : `int`
            The chance to be chosen in.
        
        chance_out : `int`
            The chance to be chosen out of.
        
        amount : `int`
            Amount given.
        
        item_id : `int`
            The given item's identifier.
            
        energy_cost_flat : `int`
            The required energy to successfully execute this action.
        
        energy_cost_scaling_success : `int`
            The required energy for each item given.
        
        energy_cost_scaling_failure : `int`
            The required energy for each item given for failure.
        """
        self = object.__new__(cls)
        self.amount = amount
        self.chance_scaling_enabled = chance_scaling_enabled
        self.chance_in = chance_in
        self.chance_out = chance_out
        self.energy_cost_flat = energy_cost_flat
        self.energy_cost_scaling_success = energy_cost_scaling_success
        self.energy_cost_scaling_failure = energy_cost_scaling_failure
        self.item_id = item_id
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # amount
        repr_parts.append(', amount = ')
        repr_parts.append(repr(self.amount))
        
        # chance_in
        repr_parts.append(', chance_in = ')
        repr_parts.append(repr(self.chance_in))
        
        # chance_out
        repr_parts.append(', chance_out = ')
        repr_parts.append(repr(self.chance_out))
        
        # chance_scaling_enabled
        repr_parts.append(', chance_scaling_enabled = ')
        repr_parts.append(repr(self.chance_scaling_enabled))
        
        # energy_cost_flat
        repr_parts.append(', energy_cost_flat = ')
        repr_parts.append(repr(self.energy_cost_flat))
        
        # energy_cost_scaling_failure
        repr_parts.append(', energy_cost_scaling_failure = ')
        repr_parts.append(repr(self.energy_cost_scaling_failure))
        
        # energy_cost_scaling_success
        repr_parts.append(', energy_cost_scaling_success = ')
        repr_parts.append(repr(self.energy_cost_scaling_success))
        
        # item_id
        repr_parts.append(', item_id = ')
        repr_parts.append(repr(self.item_id))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns self == other."""
        if type(self) is not type(other):
            return NotImplemented
        
        # amount
        if self.amount != other.amount:
            return False
        
        # chance_in
        if self.chance_in != other.chance_in:
            return False
        
        # chance_out
        if self.chance_out != other.chance_out:
            return False
        
        # chance_scaling_enabled
        if self.chance_scaling_enabled != other.chance_scaling_enabled:
            return False
        
        # energy_cost_flat
        if self.energy_cost_flat != other.energy_cost_flat:
            return False
        
        # energy_cost_scaling_failure
        if self.energy_cost_scaling_failure != other.energy_cost_scaling_failure:
            return False
        
        # energy_cost_scaling_success
        if self.energy_cost_scaling_success != other.energy_cost_scaling_success:
            return False
        
        # item_id
        if self.item_id != other.item_id:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns hash(self)."""
        hash_value = 0
        
        # amount
        hash_value ^= self.amount << 16
        
        # chance_in
        hash_value ^= self.chance_in << 24
        
        # chance_out
        hash_value ^= self.chance_out << 0
        
        # chance_scaling_enabled
        hash_value ^= self.chance_scaling_enabled << 33
        
        # energy_cost_flat
        hash_value ^= self.energy_cost_flat << 7
        
        # energy_cost_scaling_failure
        hash_value ^= self.energy_cost_scaling_failure << 15
        
        # energy_cost_scaling_success
        hash_value ^= self.energy_cost_scaling_success << 17
        
        # item_id
        hash_value ^= self.item_id
        
        return hash_value
