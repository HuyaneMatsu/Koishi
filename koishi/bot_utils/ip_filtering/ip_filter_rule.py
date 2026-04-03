__all__ = ('IPFilterRule',)

from scarletio import RichAttributeErrorBaseType

from .utils import produce_ip_as_bits


class IPFilterRule(RichAttributeErrorBaseType):
    """
    Good.
    
    Parameters
    ----------
    absorbed_bits : `bool`
        How much bits are absorbed from the end.
    
    ip : `int`
        The ip address.
    
    type : `int`
        The ip's type.
    """
    __slots__ = ('absorbed_bits', 'ip', 'type')
    
    def __new__(cls, ip_type, ip, absorbed_bits):
        """
        A rule for ip filtering.
        
        Parameters
        ----------
        ip_type : `int`
            The ip's type.
        
        ip : `int`
            The ip address.
        
        absorbed_bits : `bool`
            How much bits are absorbed from the end.
        """
        self = object.__new__(cls)
        self.type = ip_type
        self.ip = ip
        self.absorbed_bits = absorbed_bits
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # type
        ip_type = self.type
        repr_parts.append(' type = ')
        repr_parts.append(repr(ip_type))
        
        # ip
        repr_parts.append(', ip = ')
        repr_parts.extend(produce_ip_as_bits(ip_type, self.ip))
        
        # absorbed_bits
        repr_parts.append(', absorbed_bits = ')
        repr_parts.append(repr(self.absorbed_bits))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns self == other."""
        if type(self) is not type(other):
            return NotImplemented
        
        # absorbed_bits
        if self.absorbed_bits != other.absorbed_bits:
            return False
        
        # ip
        if self.ip != other.ip:
            return False
        
        # type
        if self.type != other.type:
            return False
        
        return True

    
    def __hash__(self):
        """Returns hash(self)."""
        hash_value = 0
        
        # absorbed_bits
        hash_value ^= self.absorbed_bits << 8
        
        # ip
        hash_value ^= hash(self.ip)
        
        # type
        hash_value ^= self.type
        
        return hash_value
