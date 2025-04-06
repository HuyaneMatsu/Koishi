__all__ = ()

from datetime import datetime as DateTime, timezone as TimeZone

from ...bot_utils.constants import IN_GAME_IDS
from ...bot_utils.daily import TOP_GG_VOTE_INTERVAL, refresh_streak, calculate_daily_new

from ..user_balance import get_user_balance


async def get_generic_heart_fields(target_user_id):
    """
    Gets the generic heart fields.
    
    This function is a coroutine.
    
    Parameters
    ----------
    target_user_id : `int`
        The user to request the fields for.
    
    Returns
    -------
    balance : `int`
    streak : `int`
    ready_to_claim : `bool`
    """
    user_balance = await get_user_balance(target_user_id)
    
    if user_balance.allocated and (target_user_id not in IN_GAME_IDS):
        user_balance.set('allocated', 0)
        await user_balance.save()
    
    now = DateTime.now(TimeZone.utc)
    streak, daily_can_claim_at = calculate_daily_new(user_balance.streak, user_balance.daily_can_claim_at, now)
    ready_to_claim = daily_can_claim_at <= DateTime.now(TimeZone.utc)
    
    return user_balance.balance, streak, ready_to_claim


async def get_generic_vote_fields(target_user_id):
    """
    Gets the generic vote fields.
    
    This function is a coroutine.
    
    Parameters
    ----------
    target_user_id : `int`
        The user to request the fields for.
    
    Returns
    -------
    balance : `int`
    streak : `int`
    ready_to_vote : `bool`
    """
    user_balance = await get_user_balance(target_user_id)
    
    if user_balance.allocated and (target_user_id not in IN_GAME_IDS):
        user_balance.set('allocated', 0)
        await user_balance.save()
    
    now = DateTime.now(TimeZone.utc)
    streak = refresh_streak(user_balance.streak, user_balance.daily_can_claim_at, now)
    ready_to_vote = user_balance.top_gg_voted_at + TOP_GG_VOTE_INTERVAL <= now
    return user_balance.balance, streak, ready_to_vote


async def get_stat_fields(target_user_id):
    """
    Gets the stat fields.
    
    This function is a coroutine.
    
    Parameters
    ----------
    target_user_id : `int`
        The user to request the fields for.
    
    Returns
    -------
    balance : `int`
    streak : `int`
    count_daily_self : `int`
    count_daily_by_related : `int`
    count_daily_for_related : `int`
    count_top_gg_vote : `int`
    """
    user_balance = await get_user_balance(target_user_id)
    
    if user_balance.allocated and (target_user_id not in IN_GAME_IDS):
        user_balance.set('allocated', 0)
        await user_balance.save()
    
    now = DateTime.now(TimeZone.utc)
    streak = refresh_streak(user_balance.streak, user_balance.daily_can_claim_at, now)
    
    return (
        user_balance.balance,
        streak,
        user_balance.count_daily_self,
        user_balance.count_daily_by_related,
        user_balance.count_daily_for_related,
        user_balance.count_top_gg_vote,
    )
