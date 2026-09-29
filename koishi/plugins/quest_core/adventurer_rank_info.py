__all__ = ('adventure_rank_info_create',)

from scarletio import RichType


class AdventurerRankInfo(metaclass = RichType, rich_type_feature_flags = ~0):
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


def adventure_rank_info_create(level, quest_limit):
    """
    Creates a new adventurer rank info.
    
    Parameters
    ----------
    level : `int`
        The adventurer level (or rank).
    
    quest_limit : `int`
        How much quests the user can accept / the guild can offer.
    
    Returns
    -------
    adventure_tank_info : ``AdventurerRankInfo``
    """
    adventure_tank_info = object.__new__(AdventurerRankInfo)
    adventure_tank_info.level = level
    adventure_tank_info.quest_limit = quest_limit
    return adventure_tank_info
