__all__ = ('OptionBase',)

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
    
    chance_in : `int`
        The chance to be chosen in.
    
    chance_out : `int`
        The chance to be chosen out of.
    """
    __slots__ = ('amount_base', 'amount_interval', 'chance_in', 'chance_out')
    
    def __new__(cls, chance_in, chance_out, amount_min, amount_max):
        """
        Creates a new enemy option.
        
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
        """
        self = object.__new__(cls)
        self.amount_base = amount_min
        self.amount_interval = amount_max - amount_min
        self.chance_in = chance_in
        self.chance_out = chance_out
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
        
        # chance_in
        yield ', chance_in = '
        yield repr(self.chance_in)
        
        # chance_out
        yield ', chance_out = '
        yield repr(self.chance_out)
    
    
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
        
        # chance_in
        if self.chance_in != other.chance_in:
            return False
        
        # chance_out
        if self.chance_out != other.chance_out:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns hash(self)."""
        hash_value = 0
        
        # amount_base
        hash_value ^= self.amount_base << 16
        
        # amount_interval
        hash_value ^= self.amount_interval << 8
        
        # chance_in
        hash_value ^= self.chance_in << 24
        
        # chance_out
        hash_value ^= self.chance_out << 0
        
        return hash_value
