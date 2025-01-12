__all__ = ()

from ...bot_utils.daily import TOP_GG_VOTE_DELAY_MAX, TOP_GG_VOTE_DELAY_MIN


def should_top_gg_notify(count_top_gg_vote, top_gg_voted_at, now):
    """
    Returns whether the user should get reminder to vote on top.gg.
    
    Parameters
    ----------
    count_top_gg_vote : `int`
        The amount of times the user voted on top.gg.
    
    top_gg_voted_at : `DateTime`
        When the user voted last time.
    
    now : `DateTime`
        Current time.
    
    Returns
    -------
    should_notify : `bool`
    """
    if count_top_gg_vote <= 0:
        return False
        
    vote_difference = now - top_gg_voted_at
    
    if vote_difference < TOP_GG_VOTE_DELAY_MIN:
        return False
    
    if vote_difference > TOP_GG_VOTE_DELAY_MAX:
        return False
    
    return True
