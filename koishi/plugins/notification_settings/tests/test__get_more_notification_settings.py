import vampytest

from ..cache import NOTIFICATION_SETTINGS_CACHE, put_one_to_cache
from ..notification_settings import NotificationSettings
from ..queries import get_more_notification_settings


async def test__get_more_notification_settings__cache_hit():
    """
    Tests whether ``get_more_notification_settings`` works as intended.
    
    Case: Cache hit.
    
    This function is a coroutine.
    """
    query_called = False
    
    user_id_0 = 202309240070
    user_id_1 = 202309240071
    
    notification_settings_0 = NotificationSettings(user_id_0, daily_by_waifu = False)
    notification_settings_1 = NotificationSettings(user_id_1, proposal = False)
    
    async def query(user_ids):
        nonlocal query_called
        query_called = True
        
        return None, None
    
    
    mocked = vampytest.mock_globals(
        get_more_notification_settings,
        _query_more_notification_settings = query,
    )
    
    try:
        put_one_to_cache(notification_settings_0)
        put_one_to_cache(notification_settings_1)
        
        output = await mocked([user_id_0, user_id_1])
        
        vampytest.assert_eq(output, [notification_settings_0, notification_settings_1])
        
        vampytest.assert_false(query_called)
    finally:
        NOTIFICATION_SETTINGS_CACHE.clear()


async def test__get_more_notification_settings__database_hit_value():
    """
    Tests whether ``get_more_notification_settings`` works as intended.
    
    Case: Database hit with value.
    
    This function is a coroutine.
    """
    query_called = False
    called_with_user_ids = None
    
    user_id_0 = 202309240072
    user_id_1 = 202309240073
    
    notification_settings_0 = NotificationSettings(user_id_0, daily_by_waifu = False)
    notification_settings_1 = NotificationSettings(user_id_1, proposal = False)
    
    async def query(user_ids):
        nonlocal query_called
        nonlocal called_with_user_ids
        nonlocal notification_settings_0
        nonlocal notification_settings_1
        
        query_called = True
        called_with_user_ids = user_ids
        
        return [notification_settings_0, notification_settings_1], None
    
    
    mocked = vampytest.mock_globals(
        get_more_notification_settings,
        _query_more_notification_settings = query,
    )
    
    try:
        output = await mocked([user_id_0, user_id_1])
        
        vampytest.assert_eq(output, [notification_settings_0, notification_settings_1])
        
        vampytest.assert_true(query_called)
        vampytest.assert_eq(called_with_user_ids, [user_id_0, user_id_1])
        
        vampytest.assert_eq(
            [*NOTIFICATION_SETTINGS_CACHE.items()],
            [(user_id_0, notification_settings_0), (user_id_1, notification_settings_1)],
        )
    finally:
        NOTIFICATION_SETTINGS_CACHE.clear()


async def test__get_more_notification_settings__database_hit_none():
    """
    Tests whether ``get_more_notification_settings`` works as intended.
    
    Case: Database hit with none.
    
    This function is a coroutine.
    """
    query_called = False
    called_with_user_ids = 0
    
    user_id_0 = 202309240074
    user_id_1 = 202309240075
    
    async def query(user_ids):
        nonlocal query_called
        nonlocal called_with_user_ids
        nonlocal user_id_0
        nonlocal user_id_1
        
        query_called = True
        called_with_user_ids = user_ids
        
        return None, [user_id_0, user_id_1]
    
    
    mocked = vampytest.mock_globals(
        get_more_notification_settings,
        _query_more_notification_settings = query,
    )
    
    try:
        output = await mocked([user_id_0, user_id_1])
        
        vampytest.assert_eq(output, [NotificationSettings(user_id_0), NotificationSettings(user_id_1)])
        
        vampytest.assert_true(query_called)
        vampytest.assert_eq(called_with_user_ids, [user_id_0, user_id_1])
        
        vampytest.assert_eq(
            [*NOTIFICATION_SETTINGS_CACHE.items()],
            [(user_id_0, None), (user_id_1, None)],
        )
    finally:
        NOTIFICATION_SETTINGS_CACHE.clear()


async def test__get_more_notification_settings__mixed_hit_value():
    """
    Tests whether ``get_more_notification_settings`` works as intended.
    
    Case: Cache and database hit with value.
    
    This function is a coroutine.
    """
    query_called = False
    called_with_user_ids = None
    
    user_id_0 = 202309240076
    user_id_1 = 202309240077
    
    notification_settings_0 = NotificationSettings(user_id_0, daily_by_waifu = False)
    notification_settings_1 = NotificationSettings(user_id_1, proposal = False)
    
    async def query(user_ids):
        nonlocal query_called
        nonlocal called_with_user_ids
        nonlocal notification_settings_1
        
        query_called = True
        called_with_user_ids = user_ids
        
        return [notification_settings_1], None
    
    
    mocked = vampytest.mock_globals(
        get_more_notification_settings,
        _query_more_notification_settings = query,
    )
    
    try:
        put_one_to_cache(notification_settings_0)
        
        output = await mocked([user_id_0, user_id_1])
        
        vampytest.assert_eq(output, [notification_settings_0, notification_settings_1])
        
        vampytest.assert_true(query_called)
        vampytest.assert_eq(called_with_user_ids, [user_id_1])
        
        vampytest.assert_eq(
            [*NOTIFICATION_SETTINGS_CACHE.items()],
            [(user_id_0, notification_settings_0), (user_id_1, notification_settings_1)],
        )
    finally:
        NOTIFICATION_SETTINGS_CACHE.clear()
