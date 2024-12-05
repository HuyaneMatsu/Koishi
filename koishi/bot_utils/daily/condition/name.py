__all__ = ('ConditionName',)

from scarletio import copy_docs

from .base import ConditionBase


class ConditionName(ConditionBase):
    """
    Condition whether the user's name matches.
    
    Attributes
    ----------
    name : ``str``
        Name to check for.
    """
    __slots__ = ('name',)
    
    
    def __new__(cls, name):
        """
        Creates a new name condition.
        
        Parameters
        ----------
        name : ``str``
            The name to check for.
        """
        self = object.__new__(cls)
        self.name = name
        return self
    
    
    @copy_docs(ConditionBase._build_repr_parts_into)
    def _build_repr_parts_into(self, into):
        into.append(' name = ')
        into.append(repr(self.name))
        return into
    
    
    @copy_docs(ConditionBase.__hash__)
    def __hash__(self):
        return hash(self.name)

    
    @copy_docs(ConditionBase._eq_same_type)
    def _eq_same_type(self, other):
        return self.name == other.name
    
    
    @copy_docs(ConditionBase.__call__)
    def __call__(self, user):
        return user.name == self.name
