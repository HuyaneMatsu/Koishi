__all__ = ('OptionBase',)

from math import floor

from scarletio import RichAttributeErrorBaseType


class OptionBase(RichAttributeErrorBaseType):
    """
    Base type for randomization based options.
    
    Attributes
    ----------
    amount_base : `int`
        The base amount that is always given.
    
    amount_interval : `int`
        The interval between the base amount and the maximal amount that can be given.
    
    chance_byte_size : `int`
        The chance of this loot option to be selected.
        Is between `0` and `255`
    """
    __slots__ = ('amount_base', 'amount_interval', 'chance_byte_size')
    
    def __new__(cls, chance, amount_min, amount_max):
        """
        Creates a new enemy option.
        
        Parameters
        ----------
        chance : `float`
            The chance of this loot option to be selected.
            Value from `0.0` to `1.0`.
        
        amount_min : `int`
            The minimal amount.
        
        amount_max : `int`
            The maximal amount.
        """
        self = object.__new__(cls)
        self.amount_base = amount_min
        self.amount_interval = amount_max - amount_min
        self.chance_byte_size = floor(255.0 * chance)
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        return ''.join(['<', type(self).__name__, *self._produce_nested_repr_parts(), '>'])
    
    
    def _produce_nested_repr_parts(self):
        """
        Helper function for creating the representation of the option.
        
        This function is an iterable generator.
        
        Yields
        ------
        part : `str`
        """
        # amount_base
        yield ' amount_base = '
        yield repr(self.amount_base)
        
        # amount_interval
        yield ', amount_interval = '
        yield repr(self.amount_interval)
        
        # chance_byte_size
        yield ', chance_byte_size = '
        yield repr(self.chance_byte_size)
    
    
    def __eq__(self, other):
        """Returns self == other."""
        if type(self) is not type(other):
            return NotImplemented
        
        return self._is_equal_same_type(other)
    
    
    def _is_equal_same_type(self, other):
        """
        Returns whether self is equal to other. Other must be same type as self.
        
        Parameters
        ----------
        other : `instance<type<self>>`
            The other instance.
        
        Returns
        -------
        is_equal : `bool`
        """
        # amount_base
        if self.amount_base != other.amount_base:
            return False
        
        # amount_interval
        if self.amount_interval != other.amount_interval:
            return False
        
        # chance_byte_size
        if self.chance_byte_size != other.chance_byte_size:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns hash(self)."""
        hash_value = 0
        
        # amount_base
        hash_value ^= self.amount_base << 16
        
        # amount_interval
        hash_value ^= self.amount_interval << 8
        
        # chance_byte_size
        hash_value ^= self.chance_byte_size << 24
        
        return hash_value
