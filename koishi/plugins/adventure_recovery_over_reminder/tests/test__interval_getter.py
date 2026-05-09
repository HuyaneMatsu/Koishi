from datetime import datetime as DateTime, timedelta as TimeDelta, timezone as TimeZone

import vampytest

from ..looping import interval_getter


async def test__interval_getter__default():
    """
    Tests whether ``interval_getter`` works as intended.
    
    This function is a coroutine.
    
    Case: default.
    """
    interval_default = 60.0
    
    async def get_next_notification_date_time():
        return None
    
    mocked = vampytest.mock_globals(
        interval_getter,
        get_next_notification_date_time = get_next_notification_date_time,
    )
    
    output = await mocked(interval_default)
    
    vampytest.assert_instance(output, float)
    vampytest.assert_eq(output, interval_default)


async def test__interval_getter__custom_positive():
    """
    Tests whether ``interval_getter`` works as intended.
    
    This function is a coroutine.
    
    Case: custom, positive.
    """
    interval_default = 60.0
    now = DateTime.now(TimeZone.utc)
    interval_custom = 90.0
    
    async def get_next_notification_date_time():
        nonlocal interval_custom
        nonlocal now
        return now + TimeDelta(seconds = interval_custom)
    
    mocked = vampytest.mock_globals(
        interval_getter,
        get_next_notification_date_time = get_next_notification_date_time,
    )
    
    output = await mocked(interval_default)
    
    vampytest.assert_instance(output, float)
    vampytest.assert_true(output > interval_custom - 1.0 and output < interval_custom + 1.0)


async def test__interval_getter__custom_negative():
    """
    Tests whether ``interval_getter`` works as intended.
    
    This function is a coroutine.
    
    Case: custom, positive.
    """
    interval_default = 60.0
    now = DateTime.now(TimeZone.utc)
    interval_custom = 90.0
    
    async def get_next_notification_date_time():
        nonlocal interval_custom
        nonlocal now
        return now - TimeDelta(seconds = interval_custom)
    
    mocked = vampytest.mock_globals(
        interval_getter,
        get_next_notification_date_time = get_next_notification_date_time,
    )
    
    output = await mocked(interval_default)
    
    vampytest.assert_instance(output, float)
    vampytest.assert_eq(output, 0.0)
