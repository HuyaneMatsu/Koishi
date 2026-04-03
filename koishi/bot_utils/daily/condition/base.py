__all__ = ('ConditionBase',)

from scarletio import RichAttributeErrorBaseType


class ConditionBase(RichAttributeErrorBaseType):
    """
    Represents the condition of a daily reward.
    """
    __slots__ = ()
    
    def __new__(cls):
        """
        Creates a new condition.
        """
        return object.__new__(cls)
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        repr_parts = self._build_repr_parts_into(repr_parts)
        repr_parts.append('>')
        return ''.join(repr_parts)

    
    def _build_repr_parts_into(self, into):
        """
        Representation builder helper.
        
        Parameters
        ----------
        into : `list<str>`
            List of strings to build the representation into.
        
        Returns
        -------
        into : `list<str>`
        """
        return into
    
    
    def __hash__(self):
        """Returns hash(self)."""
        return 0
    
    
    def __eq__(self, other):
        """Returns self == other."""
        if type(self) is not type(other):
            return NotImplemented
        
        return self._eq_same_type(other)
    
    
    def _eq_same_type(self, other):
        """
        Helper method for ``.__eq__``. Returns whether the two instances are equal.
        
        Parameters
        ----------
        other : `instance<type<self>>`
            The other instance.
        
        Returns
        -------
        equal : `bool`
        """
        return True
    
    
    def __call__(self, user):
        """
        Returns whether the condition passes for the given user.
        
        Parameters
        ----------
        user : ``ClientUserBase``
            The user to check.
        
        Returns
        -------
        passing : `bool`
        """
        return True
