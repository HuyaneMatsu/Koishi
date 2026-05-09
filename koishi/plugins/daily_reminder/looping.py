__all__ = ('REMINDER_LOOPER',)


from ..reminder_notification_delivery_core import ReminderLooper

from .notifier import notify_user
from .queries import get_entries_to_notify_with_connector


REMINDER_LOOPER = ReminderLooper(
    'daily_reminder',
    get_entries_to_notify_with_connector,
    notify_user,
)
