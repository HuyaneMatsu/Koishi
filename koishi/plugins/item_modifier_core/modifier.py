__all__ = ('Modifier',)

from scarletio import RichAttributeErrorBaseType

from .helpers import get_modifier_name_and_value_producer_and_amount_postfix


class Modifier(RichAttributeErrorBaseType):
    """
    Represents a modifier.
    
    Attributes
    ----------
    amount : `int`
        The modifier amount.
    
    type : `int`
        The modifier's type.
    """
    __slots__ = ('amount', 'type')
    
    def __new__(cls, modifier_type, amount):
        """
        Creates a new modifier.
        
        Parameters
        ----------
        modifier_type : `int`
            The modifier's type.
        
        amount : `int`
            The modifier amount.
        """
        self = object.__new__(cls)
        self.amount = amount
        self.type = modifier_type
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__, ' ']
        
        (
            modifier_name,
            value_producer,
            modifier_amount_postfix,
        ) = get_modifier_name_and_value_producer_and_amount_postfix(self.type)
        
        amount = self.amount
        repr_parts.append('+' if amount >= 0 else '-')
        amount = abs(amount)
        if value_producer is None:
            repr_parts.append(str(amount))
        else:
            repr_parts.extend(value_producer(amount))
        
        if (modifier_amount_postfix is not None):
            repr_parts.append(modifier_amount_postfix)
        
        repr_parts.append(' ')
        repr_parts.append(modifier_name)
        
        repr_parts.append('>')
        return ''.join(repr_parts)
