__all__ = (
    'get_guild_adventurer_rank_info', 'get_guild_adventurer_rank_up_credibility', 'get_user_adventurer_rank_info',
    'get_user_adventurer_rank_up_credibility'
)

from .adventurer_rank_info import AdventurerRankInfo


def get_user_adventurer_rank_info(credibility):
    """
    Gets the user's adventurer rank info.
    
    Parameters
    ----------
    credibility : `int`
        The user's credibility.
    
    Returns
    -------
    adventurer_rank_info : ``AdventurerRankInfo``
    """
    rank = 0
    credibility >>= 8
    
    while True:
        if not credibility:
            break
        
        rank += 1
        credibility >>= 1
        continue
    
    return AdventurerRankInfo(rank, ((rank + 3) >> 1))


def get_guild_adventurer_rank_info(credibility):
    """
    Gets the guild's adventurer rank info.
    
    Parameters
    ----------
    credibility : `int`
        The user's credibility.
    
    Returns
    -------
    adventurer_rank_info : ``AdventurerRankInfo``
    """
    rank = 0
    credibility >>= 10
    
    while True:
        if not credibility:
            break
        
        rank += 1
        credibility >>= 1
        continue
    
    return AdventurerRankInfo(rank, rank + ((rank + 6) >> 1))


def get_user_adventurer_rank_up_credibility(level):
    """
    Returns how much credibility is required for the user for the next adventurer rank.
    
    Parameters
    ----------
    level : `int`
        The user's current level.
    
    Returns
    -------
    credibility : `int`
    """
    return 1 << (8 + level)


def get_guild_adventurer_rank_up_credibility(level):
    """
    Returns how much credibility is required for the guild for the next adventurer rank.
    
    Parameters
    ----------
    level : `int`
        The guild's current level.
    
    Returns
    -------
    credibility : `int`
    """
    return 1 << (10 + level)
