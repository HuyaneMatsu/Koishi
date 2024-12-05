__all__ = ('ConditionRole',)

from scarletio import copy_docs

from .base import ConditionBase


class ConditionRole(ConditionBase):
    """
    Condition whether the user has the given role.
    
    Attributes
    ----------
    role : ``Role``
        Role to check for.
    """
    __slots__ = ('role',)
    
    
    def __new__(cls, role):
        """
        Creates a new role condition.
        
        Parameters
        ----------
        role : ``Role``
            The role to check for.
        """
        self = object.__new__(cls)
        self.role = role
        return self
    
    
    @copy_docs(ConditionBase._build_repr_parts_into)
    def _build_repr_parts_into(self, into):
        into.append(' role = ')
        into.append(repr(self.role))
        return into
    
    
    @copy_docs(ConditionBase.__hash__)
    def __hash__(self):
        return self.role.id

    
    @copy_docs(ConditionBase._eq_same_type)
    def _eq_same_type(self, other):
        return self.role is other.role
    
    
    @copy_docs(ConditionBase.__call__)
    def __call__(self, user):
        return user.has_role(self.role)
