import vampytest

from ..cache import NOTIFICATION_SETTINGS_CACHE, put_one_to_cache
from ..notification_settings import NotificationSettings
from ..queries import get_one_notification_settings_with_connector


async def test__get_one_notification_settings_with_connector__cache_hit():
    """
    Tests whether ``get_one_notification_settings_with_connector`` works as intended.
    
    Case: Cache hit.
    
    This function is a coroutine.
    """
    query_called = False
    connector = object()
    
    user_id = 202309240060
    notification_settings = NotificationSettings(user_id, daily = False)
    
    async def query(user_id, connector):
        nonlocal query_called
        query_called = True
        
        return None
    
    
    mocked = vampytest.mock_globals(
        get_one_notification_settings_with_connector,
        query_one_touhou_notification_settings_with_connector = query,
    )
    
    try:
        put_one_to_cache(notification_settings)
        
        output = await mocked(user_id, connector)
        
        vampytest.assert_eq(output, notification_settings)
        
        vampytest.assert_false(query_called)
    finally:
        NOTIFICATION_SETTINGS_CACHE.clear()


async def test__get_one_notification_settings_with_connector__database_hit_value():
    """
    Tests whether ``get_one_notification_settings_with_connector`` works as intended.
    
    Case: Database hit with value.
    
    This function is a coroutine.
    """
    query_called = False
    connector = object()
    called_with_user_id = 0
    called_connector_with = None
    
    user_id = 202309240061
    notification_settings = NotificationSettings(user_id, daily = False)
    
    async def query(user_id, connector):
        nonlocal query_called
        nonlocal called_with_user_id
        nonlocal notification_settings
        nonlocal called_connector_with
        
        query_called = True
        called_with_user_id = user_id
        called_connector_with = connector
        
        return notification_settings
    
    
    mocked = vampytest.mock_globals(
        get_one_notification_settings_with_connector,
        _query_one_notification_settings_with_connector = query,
    )
    
    try:
        output = await mocked(user_id, connector)
        
        vampytest.assert_eq(output, notification_settings)
        
        vampytest.assert_true(query_called)
        vampytest.assert_eq(called_with_user_id, user_id)
        vampytest.assert_is(called_connector_with, connector)
        
        vampytest.assert_eq([*NOTIFICATION_SETTINGS_CACHE.items()], [(user_id, notification_settings)])
    finally:
        NOTIFICATION_SETTINGS_CACHE.clear()


async def test__get_one_notification_settings_with_connector__database_hit_none():
    """
    Tests whether ``get_one_notification_settings_with_connector`` works as intended.
    
    Case: Database hit with none.
    
    This function is a coroutine.
    """
    query_called = False
    connector = object()
    called_with_user_id = 0
    called_connector_with = None
    
    user_id = 202309240062
    notification_settings = None
    
    async def query(user_id, connector):
        nonlocal query_called
        nonlocal called_with_user_id
        nonlocal notification_settings
        nonlocal called_connector_with
        
        query_called = True
        called_with_user_id = user_id
        called_connector_with = connector
        
        return notification_settings
    
    
    mocked = vampytest.mock_globals(
        get_one_notification_settings_with_connector,
        _query_one_notification_settings_with_connector = query,
    )
    
    try:
        output = await mocked(user_id, connector)
        
        vampytest.assert_eq(output, NotificationSettings(user_id))
        
        vampytest.assert_true(query_called)
        vampytest.assert_eq(called_with_user_id, user_id)
        vampytest.assert_is(called_connector_with, connector)
        
        vampytest.assert_eq([*NOTIFICATION_SETTINGS_CACHE.items()], [(user_id, notification_settings)])
    finally:
        NOTIFICATION_SETTINGS_CACHE.clear()
