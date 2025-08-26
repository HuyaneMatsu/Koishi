__all__ = ()

from scarletio import RichAttributeErrorBaseType


class Node(RichAttributeErrorBaseType):
    """
    Rerepresents a node of a built ip structure .
    
    Attributes
    ----------
    absorb : `bool`
        Whether to absorb everything after this node.
    
    one : ``None | instance<cls>``
        Branching out if the bit is one.
    
    zero : ``None | instance<cls>``
        Branching out if the bit is zero.
    """
    __slots__ = ('absorb', 'one', 'zero')
    
    
    def __new__(cls, zero, one, absorb):
        """
        Creates a new node.
        
        Parameters
        ----------
        zero : ``None | instance<cls>``
            Branching out if the bit is zero.
        
        one : ``None | instance<cls>``
            Branching out if the bit is one.
        
        absorb : `bool`
            Whether to absorb everything after this node.
        """
        self = object.__new__(cls)
        self.absorb = absorb
        self.one = one
        self.zero = zero
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        return ''.join([*self._build_repr_parts()])
    
    
    def _build_repr_parts(self):
        """
        Helper function for ``.__repr__`` to build the representation by part.
        
        This function is an iterable generator.
        
        Yields
        """
        yield '<'
        yield type(self).__name__
        
        # zero
        yield ' zero = '
        zero = self.zero
        if (zero is None):
            yield repr(None)
        else:
            yield from zero._build_repr_parts()
        
        # one
        yield ', one = '
        one = self.one
        if (one is None):
            yield repr(None)
        else:
            yield from one._build_repr_parts()
        
        # absorb
        yield ', absorb = '
        yield repr(self.absorb)
        
        yield '>'
    
    
    def __eq__(self, other):
        """Returns self == other."""
        if type(self) is not type(other):
            return NotImplemented
        
        # absorb
        if self.absorb != other.absorb:
            return False
        
        # one
        if self.one != other.one:
            return False
        
        # zero
        if self.zero != other.zero:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns hash(self)."""
        hash_value = 0
        
        # absorb
        hash_value ^= self.absorb
        
        # one
        one = self.one
        if (one is not None):
            one_hash = hash(one)
            hash_value ^= (one_hash >> 22) | ((one_hash & ((1 << 22) - 1)) << 42)
        
        # zero
        zero = self.zero
        if (zero is not None):
            zero_hash = hash(zero)
            hash_value ^= (zero_hash >> 42) | ((zero_hash & ((1 << 42) - 1)) << 22)
        
        return hash_value
