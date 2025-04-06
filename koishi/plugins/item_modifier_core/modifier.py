__all__ = ('Modifier',)

from scarletio import RichAttributeErrorBaseType

from .helpers import get_modifier_name_and_amount_postfix


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
        
        amount = self.amount
        repr_parts.append('+' if amount >= 0 else '-')
        repr_parts.append(str(abs(amount)))
        
        modifier_name, modifier_amount_postfix = get_modifier_name_and_amount_postfix(self.type)
        
        if (modifier_amount_postfix is not None):
            repr_parts.append(modifier_amount_postfix)
        
        repr_parts.append(' ')
        repr_parts.append(modifier_name)
        
        repr_parts.append('>')
        return ''.join(repr_parts)
