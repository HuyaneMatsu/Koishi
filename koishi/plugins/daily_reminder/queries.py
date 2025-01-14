__all__ = ()

from datetime import datetime as DateTime, timezone as TimeZone

from sqlalchemy import and_, not_
from sqlalchemy.sql import select

from ...bot_utils.daily import DAILY_REMINDER_AFTER
from ...bot_utils.models import USER_BALANCE_TABLE, user_balance_model, user_settings_model


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
            ]
        ).where(
            and_(
                user_balance_model.user_id == user_settings_model.user_id,
                user_balance_model.daily_can_claim_at <= DateTime.now(TimeZone.utc) - DAILY_REMINDER_AFTER,
                user_settings_model.notification_daily_reminder,
                not_(user_balance_model.daily_reminded),
            )
        )
    )
    
    return await response.fetchall()


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
