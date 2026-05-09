from datetime import datetime as DateTime, timedelta as TimeDelta, timezone as TimeZone

import vampytest
from scarletio import skip_ready_cycle

from ...reminder_notification_delivery_core import ReminderLooper
from ...user_settings import UserSettings
from ...user_stats_core import UserStats

from .. import set_closest_adventure_recovery_over_reminder


async def test__set_closest_adventure_recovery_over_reminder__disabled():
    """
    Tests whether ``set_closest_adventure_recovery_over_reminder`` works as intended.
    
    This function is a coroutine.
    
    Case: Option disabled.
    """
    user_id = 202605080010
    date_time = DateTime.now(TimeZone.utc) + TimeDelta(seconds = 5)
    
    user_settings = UserSettings.create_with_specification(
        user_id,
        notification_adventure_recovery_over = 0,
    )
    user_stats = UserStats(user_id)
    
    async def get_one_user_settings(input_user_id):
        nonlocal user_id
        nonlocal user_settings
        vampytest.assert_eq(input_user_id, user_id)
        return user_settings
    
    
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
        set_closest_adventure_recovery_over_reminder,
        get_one_user_settings = get_one_user_settings,
        ADVENTURE_RECOVERY_OVER_REMINDER_LOOPER = ADVENTURE_RECOVERY_OVER_REMINDER_LOOPER,
    )
    
    ADVENTURE_RECOVERY_OVER_REMINDER_LOOPER.start()
    
    try:
        await skip_ready_cycle()
        
        when = ADVENTURE_RECOVERY_OVER_REMINDER_LOOPER.handle.when
        
        await mocked(user_stats, date_time)
        
        vampytest.assert_true(ADVENTURE_RECOVERY_OVER_REMINDER_LOOPER.handle.when == when)
        vampytest.assert_is(user_stats.recovering_until_notification_at, None)
        
    finally:
        ADVENTURE_RECOVERY_OVER_REMINDER_LOOPER.stop()


async def test__set_closest_adventure_recovery_over_reminder__enabled():
    """
    Tests whether ``set_closest_adventure_recovery_over_reminder`` works as intended.
    
    This function is a coroutine.
    
    Case: Option enabled.
    """
    user_id = 202605080011
    date_time = DateTime.now(TimeZone.utc) + TimeDelta(seconds = 5)
    
    user_settings = UserSettings.create_with_specification(
        user_id,
        notification_adventure_recovery_over = 1,
    )
    user_stats = UserStats(user_id)
    
    async def get_one_user_settings(input_user_id):
        nonlocal user_id
        nonlocal user_settings
        vampytest.assert_eq(input_user_id, user_id)
        return user_settings
    
    
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
    ADVENTURE_RECOVERY_OVER_REMINDER_LOOPER.start()
    
    mocked = vampytest.mock_globals(
        set_closest_adventure_recovery_over_reminder,
        get_one_user_settings = get_one_user_settings,
        ADVENTURE_RECOVERY_OVER_REMINDER_LOOPER = ADVENTURE_RECOVERY_OVER_REMINDER_LOOPER,
    )
    
    try:
        await skip_ready_cycle()
        
        when = ADVENTURE_RECOVERY_OVER_REMINDER_LOOPER.handle.when
        
        await mocked(user_stats, date_time)
        
        vampytest.assert_true(ADVENTURE_RECOVERY_OVER_REMINDER_LOOPER.handle.when < when)
        vampytest.assert_eq(user_stats.recovering_until_notification_at, date_time)
        
    finally:
        ADVENTURE_RECOVERY_OVER_REMINDER_LOOPER.stop()
