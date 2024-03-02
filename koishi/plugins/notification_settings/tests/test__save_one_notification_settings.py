import vampytest

from ..cache import NOTIFICATION_SETTINGS_CACHE, put_none_to_cache, put_one_to_cache
from ..notification_settings import NotificationSettings
from ..queries import save_one_notification_settings


async def test__save_one_notification_settings__save_and_move():
    """
    Tests whether ``save_one_notification_settings`` works as intended.
    
    Case: saving and moving to end.
    
    This function is a coroutine.
    """
    query_called = False
    user_id_0 = 202309250000
    user_id_1 = 202309250001
    notification_settings = NotificationSettings(user_id_0, daily_by_waifu = False)
    called_with_notification_settings = None
    
    async def query(notification_settings):
        nonlocal query_called
        nonlocal called_with_notification_settings
        
        query_called = True
        called_with_notification_settings = notification_settings
    
    
    mocked = vampytest.mock_globals(
        save_one_notification_settings,
        _save_notification_settings = query,
    )
    
    try:
        put_none_to_cache(user_id_0)
        put_none_to_cache(user_id_1)
        
        await mocked(notification_settings)
        
        
        vampytest.assert_true(query_called)
        vampytest.assert_eq(called_with_notification_settings, notification_settings)
        
        vampytest.assert_eq(
            [*NOTIFICATION_SETTINGS_CACHE.items()],
            [(user_id_1, None), (user_id_0, notification_settings)],
        )
        
    finally:
        NOTIFICATION_SETTINGS_CACHE.clear()


async def test__save_one_notification_settings__delete_and_move():
    """
    Tests whether ``save_one_notification_settings`` works as intended.
    
    Case: delete and moving to end.
    
    This function is a coroutine.
    """
    query_called = False
    user_id_0 = 202309250002
    user_id_1 = 202309250003
    notification_settings = NotificationSettings(user_id_0, daily_by_waifu = False)
    called_with_notification_settings = None
    
    async def query(notification_settings):
        nonlocal query_called
        nonlocal called_with_notification_settings
        
        query_called = True
        called_with_notification_settings = notification_settings
    
    
    mocked = vampytest.mock_globals(
        save_one_notification_settings,
        _remove_notification_settings = query,
    )
    
    try:
        put_one_to_cache(notification_settings)
        put_none_to_cache(user_id_1)
        
        notification_settings = NotificationSettings(user_id_0)
        
        await mocked(notification_settings)
        
        
        vampytest.assert_true(query_called)
        vampytest.assert_eq(called_with_notification_settings, notification_settings)
        
        vampytest.assert_eq(
            [*NOTIFICATION_SETTINGS_CACHE.items()],
            [(user_id_1, None), (user_id_0, None)],
        )
        
    finally:
        NOTIFICATION_SETTINGS_CACHE.clear()
