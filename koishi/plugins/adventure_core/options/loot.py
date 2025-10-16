__all__ = ('OptionLoot',)

from scarletio import copy_docs

from .base import OptionBase


class OptionLoot(OptionBase):
    """
    Represents awarded items by completing an action.
    
    Attributes
    ----------
    amount_base : `int`
        The base amount that is always given.
    
    amount_interval : `int`
        The interval between the base amount and the maximal amount that can be given.
    
    chance_in : `int`
        The chance to be chosen in.
    
    chance_out : `int`
        The chance to be chosen out of.
    
    duration_cost_flat : `int`
        The required  duration to execute this action.
    
    duration_cost_scaling : `int`
        The required duration by item given to complete this action.
    
    energy_cost_flat : `int`
        The required energy to successfully execute this action.
    
    energy_cost_scaling : `int`
        The required energy for each item given.
    
    item_id : `int`
        The given item's identifier.
    """
    __slots__ = (
        'duration_cost_flat', 'duration_cost_scaling', 'energy_cost_flat', 'energy_cost_scaling', 'item_id',
    )
    
    def __new__(
        cls,
        chance_in,
        chance_out,
        amount_min,
        amount_max,
        item_id,
        duration_cost_flat,
        duration_cost_scaling,
        energy_cost_flat,
        energy_cost_scaling,
    ):
        """
        Creates a new loot option.
        
        Parameters
        ----------
        chance_in : `int`
            The chance to be chosen in.
        
        chance_out : `int`
            The chance to be chosen out of.
        
        amount_min : `int`
            The minimal amount.
        
        amount_max : `int`
            The maximal amount.
        
        item_id : `int`
            The given item's identifier.
        
        duration_cost_flat : `int`
            The required  duration to execute this action.
        
        duration_cost_scaling : `int`
            The required duration by item given to complete this action.
        
        energy_cost_flat : `int`
            The required energy to successfully execute this action.
        
        energy_cost_scaling : `int`
            The required energy for each item given.
        """
        self = OptionBase.__new__(cls, chance_in, chance_out, amount_min, amount_max)
        self.duration_cost_flat = duration_cost_flat
        self.duration_cost_scaling = duration_cost_scaling
        self.energy_cost_flat = energy_cost_flat
        self.energy_cost_scaling = energy_cost_scaling
        self.item_id = item_id
        return self
    
    
    @copy_docs(OptionBase._produce_nested_repr_parts)
    def _produce_nested_repr_parts(self):
        yield from OptionBase._produce_nested_repr_parts(self)
        
        # item_id
        yield ', item_id = '
        yield repr(self.item_id)
        
        # duration_cost_flat
        yield ', duration_cost_flat = '
        yield repr(self.duration_cost_flat)
        
        # duration_cost_scaling
        yield ', duration_cost_scaling = '
        yield repr(self.duration_cost_scaling)
        
        # energy_cost_flat
        yield ', energy_cost_flat = '
        yield repr(self.energy_cost_flat)
        
        # energy_cost_scaling
        yield ', energy_cost_scaling = '
        yield repr(self.energy_cost_scaling)
    
    
    @copy_docs(OptionBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        if not OptionBase._is_equal_same_type(self, other):
            return False
        
        # duration_cost_flat
        if self.duration_cost_flat != other.duration_cost_flat:
            return False
        
        # duration_cost_scaling
        if self.duration_cost_scaling != other.duration_cost_scaling:
            return False
        
        # energy_cost_flat
        if self.energy_cost_flat != other.energy_cost_flat:
            return False
        
        # energy_cost_scaling
        if self.energy_cost_scaling != other.energy_cost_scaling:
            return False
        
        # item_id
        if self.item_id != other.item_id:
            return False
        
        return True
    
    
    @copy_docs(OptionBase.__hash__)
    def __hash__(self):
        hash_value = OptionBase.__hash__(self)
        
        # duration_cost_flat
        hash_value ^= self.duration_cost_flat << 5
        
        # duration_cost_scaling
        hash_value ^= self.duration_cost_scaling << 13
        
        # energy_cost_flat
        hash_value ^= self.energy_cost_flat << 7
        
        # energy_cost_scaling
        hash_value ^= self.energy_cost_scaling << 15
        
        # item_id
        hash_value ^= self.item_id
        
        return hash_value
