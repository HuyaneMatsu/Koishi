__all__ = ()

from datetime import datetime as DateTime, timedelta as TimeDelta, timezone as TimeZone

from scarletio import copy_docs
from sqlalchemy import and_
from sqlalchemy.sql import asc, select

from ...bot_utils.models import DB_ENGINE, USER_BALANCE_TABLE, user_stats_model, user_settings_model

from ..user_settings import USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_ADVENTURE_RECOVERY_OVER


NOTIFICATION_FLAG_MASK = 1 << USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_ADVENTURE_RECOVERY_OVER

RETRY_DELAY = TimeDelta(minutes = 30)


if DB_ENGINE is None:
    from ..user_stats_core import USER_STATS_CACHE
    from ..user_settings import USER_SETTINGS_CACHE, USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT


async def get_next_notification_date_time():
    """
    Gets when the next notification should be executed.
    
    This function is a coroutine.
    
    Returns
    -------
    next_notification_date_time : `None | DateTine`
    """
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select(
                [
                    user_stats_model.recovering_until_notification_at,
                ],
            ).where(
                and_(
                    user_stats_model.user_id == user_settings_model.user_id,
                    user_stats_model.recovering_until_notification_at != None,
                    user_stats_model.recovering_until_notification_at <= DateTime.now(TimeZone.utc),
                    user_settings_model.notification_flags.op('&')(NOTIFICATION_FLAG_MASK) != 0,
                )
            ).order_by(
                asc(user_stats_model.recovering_until_notification_at),
            ).limit(
                1,
            ),
        )
        
        result = await response.fetchone()
    
    if (result is not None):
        return result[0].replace(tzinfo = TimeZone.utc)


if DB_ENGINE is None:
    @copy_docs(get_next_notification_date_time)
    async def get_next_notification_date_time():
        remind_before = DateTime.now(TimeZone.utc)
        best = None
        
        for user_stats in USER_STATS_CACHE.values():
            recovering_until_notification_at = user_stats.recovering_until_notification_at
            if not (recovering_until_notification_at is not None):
                continue
            
            if not (recovering_until_notification_at <= remind_before):
                continue
            
            user_settings = USER_SETTINGS_CACHE.get(user_stats.user_id, None)
            if (user_settings is None):
                notification_flags = USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT
            else:
                notification_flags = user_settings.notification_flags
            
            if not (notification_flags & NOTIFICATION_FLAG_MASK != 0):
                continue
            
            if (best is None) or (recovering_until_notification_at < best):
                best = recovering_until_notification_at
        
        return best


async def get_entries_to_notify_with_connector(connector):
    """
    Gets entries which should be notified.
    
    This function is a coroutine.
    
    Parameters
    ----------
    connector : ``AsyncConnection``
        Database connector.
    
    Returns
    -------
    results : `list<sqlalchemy.engine.result.RowProxy<id: int, user_id: int, preferred_client_id: int>>`
    """
    response = await connector.execute(
        select(
            [
                user_stats_model.id,
                user_stats_model.user_id,
                user_settings_model.preferred_client_id,
            ],
        ).where(
            and_(
                user_stats_model.user_id == user_settings_model.user_id,
                user_stats_model.recovering_until_notification_at != None,
                user_stats_model.recovering_until_notification_at <= DateTime.now(TimeZone.utc),
                user_settings_model.notification_flags.op('&')(NOTIFICATION_FLAG_MASK) != 0,
            ),
        ),
    )
    
    return await response.fetchall()


if DB_ENGINE is None:
    @copy_docs(get_entries_to_notify_with_connector)
    async def get_entries_to_notify_with_connector(connector):
        remind_before = DateTime.now(TimeZone.utc)
        results = []
        
        for user_stats in USER_STATS_CACHE.values():
            recovering_until_notification_at = user_stats.recovering_until_notification_at
            if not (recovering_until_notification_at is not None):
                continue
            
            if not (recovering_until_notification_at <= remind_before):
                continue
            
            user_settings = USER_SETTINGS_CACHE.get(user_stats.user_id, None)
            if (user_settings is None):
                notification_flags = USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT
                preferred_client_id = 0
            else:
                notification_flags = user_settings.notification_flags
                preferred_client_id = user_settings.preferred_client_id
            
            if not (notification_flags & NOTIFICATION_FLAG_MASK != 0):
                continue
            
            results.append((
                user_stats.entry_id,
                user_stats.user_id,
                preferred_client_id,
            ))
        
        return results


async def set_entry_as_notified_with_connector(connector, entry_id):
    """
    Sets the entry as notified.
    
    This function is a coroutine.
    
    Parameters
    ----------
    connector : ``AsyncConnection``
        Database connector.
    
    entry_id : `int`
        The entry's id to interact with.
    """
    await connector.execute(
        USER_BALANCE_TABLE.update(
            user_stats_model.id == entry_id,
        ).values(
            recovering_until_notification_at = None,
        )
    )


if DB_ENGINE is None:
    @copy_docs(set_entry_as_notified_with_connector)
    async def set_entry_as_notified_with_connector(connector, entry_id):
        for user_stats in USER_STATS_CACHE.values():
            if user_stats.entry_id == entry_id:
                user_stats.recovering_until_notification_at = None
                break


async def set_entry_as_delayed_with_connector(connector, entry_id):
    """
    Sets the entry as delayed.
    
    This function is a coroutine.
    
    Parameters
    ----------
    connector : ``AsyncConnection``
        Database connector.
    
    entry_id : `int`
        The entry's id to interact with.
    """
    await connector.execute(
        USER_BALANCE_TABLE.update(
            user_stats_model.id == entry_id,
        ).values(
            recovering_until_notification_at = DateTime.now(TimeZone.utc) + RETRY_DELAY,
        )
    )


if DB_ENGINE is None:
    @copy_docs(set_entry_as_delayed_with_connector)
    async def set_entry_as_delayed_with_connector(connector, entry_id):
        for user_stats in USER_STATS_CACHE.values():
            if user_stats.entry_id == entry_id:
                user_stats.recovering_until_notification_at = DateTime.now(TimeZone.utc) + RETRY_DELAY
                break
