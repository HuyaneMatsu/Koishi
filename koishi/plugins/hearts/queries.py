__all__ = ()

from datetime import datetime as DateTime, timezone as TimeZone

from scarletio import copy_docs
from sqlalchemy.sql import select

from ...bot_utils.constants import IN_GAME_IDS
from ...bot_utils.daily import TOP_GG_VOTE_INTERVAL, refresh_daily_streak
from ...bot_utils.models import DB_ENGINE, USER_COMMON_TABLE, user_common_model


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
    total : `int`
    streak : `int`
    ready_to_claim : `bool`
    """
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select(
                [
                    user_common_model.id,
                    user_common_model.total_love,
                    user_common_model.daily_streak,
                    user_common_model.daily_next,
                    user_common_model.total_allocated,
                ]
            ).where(
                user_common_model.user_id == target_user_id,
            )
        )
        
        result = await response.fetchone()
        
        if result is None:
            total = 0
            streak = 0
            ready_to_claim = True
        
        else:
            entry_id, total, streak, daily_next, total_allocated = result
            daily_next = daily_next.replace(tzinfo = TimeZone.utc)
            
            now = DateTime.now(TimeZone.utc)
            if daily_next < now:
                ready_to_claim = True
                streak = refresh_daily_streak(streak, daily_next, now)
            
            else:
                ready_to_claim = False
        
            if total_allocated and (target_user_id not in IN_GAME_IDS):
                await connector.execute(
                    USER_COMMON_TABLE.update(
                        user_common_model.id == entry_id,
                    ).values(
                        total_allocated = 0,
                    )
                )
    
    return total, streak, ready_to_claim
    

if DB_ENGINE is None:
    @copy_docs(get_generic_heart_fields)
    async def get_generic_heart_fields(target_user_id):
        return 0, 0, False


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
    total : `int`
    streak : `int`
    ready_to_vote : `bool`
    """
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select(
                [
                    user_common_model.id,
                    user_common_model.total_love,
                    user_common_model.daily_streak,
                    user_common_model.daily_next,
                    user_common_model.total_allocated,
                    user_common_model.top_gg_last_vote,
                ]
            ).where(
                user_common_model.user_id == target_user_id,
            )
        )
        
        result = await response.fetchone()
        
        if result is None:
            streak = 0
            total = 0
            ready_to_vote = False
        
        else:
            entry_id, total, streak, daily_next, total_allocated, top_gg_last_vote = result
            daily_next = daily_next.replace(tzinfo = TimeZone.utc)
            top_gg_last_vote = top_gg_last_vote.replace(tzinfo = TimeZone.utc)
            
            now = DateTime.now(TimeZone.utc)
            if daily_next < now:
                streak = refresh_daily_streak(streak, daily_next, now)
            
            ready_to_vote = top_gg_last_vote + TOP_GG_VOTE_INTERVAL >= now
            
            if total_allocated and (target_user_id not in IN_GAME_IDS):
                await connector.execute(
                    USER_COMMON_TABLE.update(
                        user_common_model.id == entry_id,
                    ).values(
                        total_allocated = 0,
                    )
                )
        
        return total, streak, ready_to_vote


if DB_ENGINE is None:
    @copy_docs(get_generic_vote_fields)
    async def get_generic_vote_fields(target_user_id):
        return 0, 0, False



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
    total : `int`
    streak : `int`
    count_daily_self : `int`
    count_daily_by_waifu : `int`
    count_daily_for_waifu : `int`
    count_top_gg_vote : `int`
    """
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select(
                [
                    user_common_model.id,
                    user_common_model.total_love,
                    user_common_model.daily_streak,
                    user_common_model.daily_next,
                    user_common_model.total_allocated,
                    
                    # Counts
                    user_common_model.count_daily_self,
                    user_common_model.count_daily_by_waifu,
                    user_common_model.count_daily_for_waifu,
                    user_common_model.count_top_gg_vote,
                ]
            ).where(
                user_common_model.user_id == target_user_id,
            )
        )
        
        result = await response.fetchone()
        
        if (result is None):
            total = 0
            streak = 0
            
            count_daily_self = 0
            count_daily_by_waifu = 0
            count_daily_for_waifu = 0
            count_top_gg_vote = 0
        
        else:
            (
                entry_id,
                total,
                streak,
                daily_next,
                total_allocated,
                count_daily_self,
                count_daily_by_waifu,
                count_daily_for_waifu,
                count_top_gg_vote
            ) = result
            
            daily_next = daily_next.replace(tzinfo = TimeZone.utc)
            
            now = DateTime.now(TimeZone.utc)
            if daily_next > now:
                streak = refresh_daily_streak(streak, daily_next, now)
            
            if total_allocated and (target_user_id not in IN_GAME_IDS):
                await connector.execute(
                    USER_COMMON_TABLE.update(
                        user_common_model.id == entry_id,
                    ).values(
                        total_allocated = 0,
                    )
                )
    
    return total, streak, count_daily_self, count_daily_by_waifu, count_daily_for_waifu, count_top_gg_vote 


if DB_ENGINE is None:
    @copy_docs(get_stat_fields)
    async def get_stat_fields(target_user_id):
        return 0, 0, 0, 0, 0, 0
