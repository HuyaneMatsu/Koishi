import vampytest

from ..cache import NOTIFICATION_SETTINGS_CACHE, put_one_to_cache
from ..notification_settings import NotificationSettings
from ..queries import get_one_notification_settings


async def test__get_one_notification_settings__cache_hit():
    """
    Tests whether ``get_one_notification_settings`` works as intended.
    
    Case: Cache hit.
    
    This function is a coroutine.
    """
    query_called = False
    
    user_id = 202309240050
    notification_settings = NotificationSettings(user_id, daily = False)
    
    async def query(user_id):
        nonlocal query_called
        query_called = True
    
    
    mocked = vampytest.mock_globals(
        get_one_notification_settings,
        query_one_touhou_notification_settings = query,
    )
    
    try:
        put_one_to_cache(notification_settings)
        
        output = await mocked(user_id)
        
        vampytest.assert_eq(output, notification_settings)
        
        vampytest.assert_false(query_called)
    finally:
        NOTIFICATION_SETTINGS_CACHE.clear()


async def test__get_one_notification_settings__database_hit_value():
    """
    Tests whether ``get_one_notification_settings`` works as intended.
    
    Case: Database hit with value.
    
    This function is a coroutine.
    """
    query_called = False
    called_with_user_id = 0
    
    user_id = 202309240051
    notification_settings = NotificationSettings(user_id, daily = False)
    
    async def query(user_id):
        nonlocal query_called
        nonlocal called_with_user_id
        nonlocal notification_settings
        
        query_called = True
        called_with_user_id = user_id
        
        return notification_settings
    
    
    mocked = vampytest.mock_globals(
        get_one_notification_settings,
        _query_one_notification_settings = query,
    )
    
    try:
        output = await mocked(user_id)
        
        vampytest.assert_eq(output, notification_settings)
        
        vampytest.assert_true(query_called)
        vampytest.assert_eq(called_with_user_id, user_id)
        
        vampytest.assert_eq([*NOTIFICATION_SETTINGS_CACHE.items()], [(user_id, notification_settings)])
    finally:
        NOTIFICATION_SETTINGS_CACHE.clear()


async def test__get_one_notification_settings__database_hit_none():
    """
    Tests whether ``get_one_notification_settings`` works as intended.
    
    Case: Database hit with none.
    
    This function is a coroutine.
    """
    query_called = False
    called_with_user_id = 0
    
    user_id = 202309240052
    notification_settings = None
    
    async def query(user_id):
        nonlocal query_called
        nonlocal called_with_user_id
        nonlocal notification_settings
        
        query_called = True
        called_with_user_id = user_id
        
        return notification_settings
    
    
    mocked = vampytest.mock_globals(
        get_one_notification_settings,
        _query_one_notification_settings = query,
    )
    
    try:
        output = await mocked(user_id)
        
        vampytest.assert_eq(output, NotificationSettings(user_id))
        
        vampytest.assert_true(query_called)
        vampytest.assert_eq(called_with_user_id, user_id)
        
        vampytest.assert_eq([*NOTIFICATION_SETTINGS_CACHE.items()], [(user_id, notification_settings)])
    finally:
        NOTIFICATION_SETTINGS_CACHE.clear()
