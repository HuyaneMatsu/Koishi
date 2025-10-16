__all__ = ('get_guild_adventurer_rank_info', 'get_user_adventurer_rank_info')

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
    
    return AdventurerRankInfo(rank, 1 + (rank >> 1))


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
    
    return AdventurerRankInfo(rank, 2 + rank)
