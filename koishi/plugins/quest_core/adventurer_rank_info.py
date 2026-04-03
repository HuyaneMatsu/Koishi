__all__ = ('AdventurerRankInfo',)

from scarletio import RichAttributeErrorBaseType


class AdventurerRankInfo(RichAttributeErrorBaseType):
    """
    Information about a user's or guild's adventurer rank.
    
    Attributes
    ----------
    level : `int`
        The adventurer level (or rank).
    
    quest_limit : `int`
        How much quests the user can accept / the guild can offer.
    """
    __slots__ = ('level', 'quest_limit')
    
    def __new__(cls, level, quest_limit):
        """
        Creates a new adventurer rank info.
        
        Parameters
        ----------
        level : `int`
            The adventurer level (or rank).
        
        quest_limit : `int`
            How much quests the user can accept / the guild can offer.
        """
        self = object.__new__(cls)
        self.level = level
        self.quest_limit = quest_limit
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # level
        repr_parts.append(' level = ')
        repr_parts.append(repr(self.level))
        
        # quest_limit
        repr_parts.append(', quest_limit = ')
        repr_parts.append(repr(self.quest_limit))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
