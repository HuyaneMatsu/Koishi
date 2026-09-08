from datetime import datetime as DateTime, timedelta as TimeDelta, timezone as TimeZone

import vampytest
from scarletio import skip_ready_cycle

from ...reminder_notification_delivery_core import ReminderLooper
from ...user_settings import user_settings_create_with_specification
from ...user_stats_core import user_stats_create, user_stats_set_recovering_until

from .. import adventure_recover_over_reminder_option_hook


async def test__adventure_recover_over_reminder_option_hook__not_on_recover():
    """
    Tests whether ``adventure_recover_over_reminder_option_hook`` works as intended.
    
    This function is a coroutine.
    
    Case: Not on recovery.
    """
    user_id = 202605080012
    date_time = None
    
    user_settings = user_settings_create_with_specification(
        user_id,
        notification_adventure_recovery_over = 1,
    )
    
    user_stats = user_stats_create(user_id)
    user_stats_set_recovering_until(user_stats, date_time)
    
    
    async def user_stats_get(input_user_id):
        nonlocal user_id
        nonlocal user_stats
        vampytest.assert_eq(input_user_id, user_id)
        return user_stats
    
    async def user_stats_save(input_user_stats):
        raise RuntimeError
    
    
    async def get_entries_to_notify_with_connector(connector):
        return []
    
    async def notify_user(entry, connector):
        return False
    
    
    ADVENTURE_RECOVERY_OVER_REMINDER_LOOPER = ReminderLooper(
        'test',
        get_entries_to_notify_with_connector,
        notify_user,
        interval_default = 10.0,
    )
    
    mocked = vampytest.mock_globals(
        adventure_recover_over_reminder_option_hook,
        2,
        user_stats_get = user_stats_get,
        user_stats_save = user_stats_save,
        ADVENTURE_RECOVERY_OVER_REMINDER_LOOPER = ADVENTURE_RECOVERY_OVER_REMINDER_LOOPER,
    )
    
    ADVENTURE_RECOVERY_OVER_REMINDER_LOOPER.start()
    
    try:
        await skip_ready_cycle()
        
        when = ADVENTURE_RECOVERY_OVER_REMINDER_LOOPER.handle.when
        
        mocked(user_settings, 1)
        await skip_ready_cycle()
        
        vampytest.assert_true(ADVENTURE_RECOVERY_OVER_REMINDER_LOOPER.handle.when == when)
        vampytest.assert_eq(user_stats.recovering_until_notification_at, date_time)
    finally:
        ADVENTURE_RECOVERY_OVER_REMINDER_LOOPER.stop()


async def test__adventure_recover_over_reminder_option_hook__on_recover():
    """
    Tests whether ``adventure_recover_over_reminder_option_hook`` works as intended.
    
    This function is a coroutine.
    
    Case: On recovery.
    """
    user_id = 202605080013
    date_time = DateTime.now(TimeZone.utc) + TimeDelta(seconds = 5)
    
    user_settings = user_settings_create_with_specification(
        user_id,
        notification_adventure_recovery_over = 1,
    )
    
    user_stats = user_stats_create(user_id)
    user_stats_set_recovering_until(user_stats, date_time)
    
    
    async def user_stats_get(input_user_id):
        nonlocal user_id
        nonlocal user_stats
        vampytest.assert_eq(input_user_id, user_id)
        return user_stats
    
    async def user_stats_save(input_user_stats):
        nonlocal user_stats
        vampytest.assert_eq(input_user_stats, user_stats)
    
    
    async def get_entries_to_notify_with_connector(connector):
        return []
    
    async def notify_user(entry, connector):
        return False
    
    
    ADVENTURE_RECOVERY_OVER_REMINDER_LOOPER = ReminderLooper(
        'test',
        get_entries_to_notify_with_connector,
        notify_user,
        interval_default = 10.0,
    )
    
    mocked = vampytest.mock_globals(
        adventure_recover_over_reminder_option_hook,
        2,
        user_stats_get = user_stats_get,
        ADVENTURE_RECOVERY_OVER_REMINDER_LOOPER = ADVENTURE_RECOVERY_OVER_REMINDER_LOOPER,
    )
    
    ADVENTURE_RECOVERY_OVER_REMINDER_LOOPER.start()
    
    try:
        await skip_ready_cycle()
        
        when = ADVENTURE_RECOVERY_OVER_REMINDER_LOOPER.handle.when
        
        mocked(user_settings, 1)
        await skip_ready_cycle()
        
        vampytest.assert_true(ADVENTURE_RECOVERY_OVER_REMINDER_LOOPER.handle.when <= when)
        vampytest.assert_eq(user_stats.recovering_until_notification_at, date_time)
        
    finally:
        ADVENTURE_RECOVERY_OVER_REMINDER_LOOPER.stop()
