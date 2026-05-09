__all__ = ('set_closest_adventure_recovery_over_reminder',)

from datetime import datetime as DateTime, timezone as TimeZone

from scarletio import Task, copy_docs, get_event_loop

from config import MARISA_MODE

try:
    from ..adventure_recovery_over_reminder import REMINDER_LOOPER as ADVENTURE_RECOVERY_OVER_REMINDER_LOOPER
except ImportError:
    if not MARISA_MODE:
        raise
    
    ADVENTURE_RECOVERY_OVER_REMINDER_LOOPER = None

try:
    from ..user_settings import (
        OPTION_NOTIFICATION_ADVENTURE_RECOVERY_OVER, USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT_ADVENTURE_RECOVERY_OVER,
        get_one_user_settings
    )
except ImportError:
    if not MARISA_MODE:
        raise
    
    OPTION_NOTIFICATION_ADVENTURE_RECOVERY_OVER = None
    USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT_ADVENTURE_RECOVERY_OVER = 0
    get_one_user_settings = None


try:
    from ..user_stats_core import get_user_stats, save_user_stats
except ImportError:
    if not MARISA_MODE:
        raise
    
    get_user_stats = None
    save_user_stats = None


LOOP = get_event_loop()    


async def set_closest_adventure_recovery_over_reminder(user_stats, date_time):
    """
    Sets the closest adventure recovery over reminder's date time.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_stats : ``UserStats``
        The user's stats.
    
    date_time : `DateTime`
        Date time to set.
    """
    user_settings = await get_one_user_settings(user_stats.user_id)
    if (user_settings.notification_flags >> USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT_ADVENTURE_RECOVERY_OVER) & 1:
        ADVENTURE_RECOVERY_OVER_REMINDER_LOOPER.ensure_step_at_date_time(date_time)
        user_stats.set_recovering_until_notification_at(date_time)


if (get_one_user_settings is None) or (ADVENTURE_RECOVERY_OVER_REMINDER_LOOPER is None):
    @copy_docs(set_closest_adventure_recovery_over_reminder)
    async def set_closest_adventure_recovery_over_reminder(user_stats, date_time):
        return None


async def _adventure_recover_over_reminder_option_hook(user_id):
    """
    Sets the closest adventure recovery over reminder's date time; ensured by the reminder hook.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        The user's identifier who enabled the hook.
    """
    user_stats = await get_user_stats(user_id)
    recovering_until = user_stats.recovering_until
    if (recovering_until is not None) and (recovering_until > DateTime.now(TimeZone.utc)):
        user_stats.set_recovering_until_notification_at(recovering_until)
        await save_user_stats(user_stats)
        ADVENTURE_RECOVERY_OVER_REMINDER_LOOPER.ensure_step_at_date_time(recovering_until)


def adventure_recover_over_reminder_option_hook(user_settings, value):
    """
    Hook added to adventure recovery notification option. Called when the notification changes.
    
    Parameters
    ---------
    user_settings : ``UserSettings`
        The changed user settings.
    
    value : `int`
        The new value of the option.
    """
    if value:
        Task(LOOP, _adventure_recover_over_reminder_option_hook(user_settings.user_id))


if (get_user_stats is None) or (save_user_stats is None) or (ADVENTURE_RECOVERY_OVER_REMINDER_LOOPER is None):
    @copy_docs(_adventure_recover_over_reminder_option_hook)
    async def _adventure_recover_over_reminder_option_hook(user_id):
        return
    
    @copy_docs(adventure_recover_over_reminder_option_hook)
    def adventure_recover_over_reminder_option_hook(user_settings, value):
        return


if (OPTION_NOTIFICATION_ADVENTURE_RECOVERY_OVER is not None):
    OPTION_NOTIFICATION_ADVENTURE_RECOVERY_OVER.hook = adventure_recover_over_reminder_option_hook
