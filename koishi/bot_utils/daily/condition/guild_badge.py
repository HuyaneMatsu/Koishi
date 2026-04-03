__all__ = ('ConditionGuildBadge',)

from scarletio import copy_docs

from .base import ConditionBase


class ConditionGuildBadge(ConditionBase):
    """
    Condition whether the user has the given guild badge.
    
    Attributes
    ----------
    guild : ``Guild``
        Guild to check for.
    """
    __slots__ = ('guild',)
    
    
    def __new__(cls, guild):
        """
        Creates a new guild badge condition.
        
        Parameters
        ----------
        guild : ``Guild``
            The guild to check for.
        """
        self = object.__new__(cls)
        self.guild = guild
        return self
    
    
    @copy_docs(ConditionBase._build_repr_parts_into)
    def _build_repr_parts_into(self, into):
        into.append(' guild = ')
        into.append(repr(self.guild))
        return into
    
    
    @copy_docs(ConditionBase.__hash__)
    def __hash__(self):
        return self.guild.id

    
    @copy_docs(ConditionBase._eq_same_type)
    def _eq_same_type(self, other):
        return self.guild is other.guild
    
    
    @copy_docs(ConditionBase.__call__)
    def __call__(self, user):
        guild_badge = user.primary_guild_badge
        if (guild_badge is None):
            return False
        
        return guild_badge.guild_id == self.guild.id
