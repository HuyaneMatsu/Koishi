__all__ = ()

from datetime import datetime as DateTime, timezone as TimeZone

from scarletio import copy_docs
from sqlalchemy import and_, not_
from sqlalchemy.sql import select

from ...bot_utils.daily import DAILY_REMINDER_AFTER
from ...bot_utils.models import DB_ENGINE, USER_BALANCE_TABLE, user_balance_model, user_settings_model

from ..user_settings import USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_DAILY_REMINDER


NOTIFICATION_FLAG_MASK = 1 << USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_DAILY_REMINDER


if DB_ENGINE is None:
    from ..user_balance import USER_BALANCE_CACHE
    from ..user_settings import USER_SETTINGS_CACHE, USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT


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
                user_balance_model.id,
                user_balance_model.user_id,
                user_settings_model.preferred_client_id,
            ],
        ).where(
            and_(
                user_balance_model.user_id == user_settings_model.user_id,
                user_balance_model.daily_can_claim_at <= DateTime.now(TimeZone.utc) - DAILY_REMINDER_AFTER,
                not_(user_balance_model.daily_reminded),
                user_settings_model.notification_flags.op('&')(NOTIFICATION_FLAG_MASK) != 0,
            )
        )
    )
    
    return await response.fetchall()


if DB_ENGINE is None:
    @copy_docs(get_entries_to_notify_with_connector)
    async def get_entries_to_notify_with_connector(connector):
        remind_before = DateTime.now(TimeZone.utc) - DAILY_REMINDER_AFTER
        results = []
        
        for user_balance in USER_BALANCE_CACHE.values():
            if not (user_balance.daily_can_claim_at <= remind_before):
                continue
            
            if user_balance.daily_reminded:
                continue
            
            user_settings = USER_SETTINGS_CACHE.get(user_balance.user_id, None)
            if (user_settings is None):
                notification_flags = USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT
                preferred_client_id = 0
            else:
                notification_flags = user_settings.notification_flags
                preferred_client_id = user_settings.preferred_client_id
            
            if not (notification_flags & NOTIFICATION_FLAG_MASK != 0):
                continue
            
            results.append((
                user_balance.entry_id,
                user_balance.user_id,
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
            user_balance_model.id == entry_id,
        ).values(
            daily_reminded = True,
        )
    )


if DB_ENGINE is None:
    @copy_docs(set_entry_as_notified_with_connector)
    async def set_entry_as_notified_with_connector(connector, entry_id):
        for user_balance in USER_BALANCE_CACHE.values():
            if user_balance.entry_id == entry_id:
                user_balance.daily_reminded = True
                break
