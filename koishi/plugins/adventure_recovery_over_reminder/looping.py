__all__ = ('REMINDER_LOOPER',)

from datetime import datetime as DateTime, timezone as TimeZone

from ..reminder_notification_delivery_core import ReminderLooper

from .notifier import notify_user
from .queries import get_entries_to_notify_with_connector, get_next_notification_date_time


async def interval_getter(interval_default):
    """
    Gets when the next notification should be delivered at.
    
    This function is a coroutine.
    
    Parameters
    ----------
    interval_default : `float`
        Default interval to return.
    
    Returns
    -------
    interval : `float`
    """
    next_notification_date_time = await get_next_notification_date_time()
    if next_notification_date_time is None:
        return interval_default
    
    now = DateTime.now(TimeZone.utc)
    if next_notification_date_time > now:
        return (next_notification_date_time - now).total_seconds()
    
    return 0.0


REMINDER_LOOPER = ReminderLooper(
    'adventure_recovery_over_reminder',
    get_entries_to_notify_with_connector,
    notify_user,
    interval_getter = interval_getter,
)
