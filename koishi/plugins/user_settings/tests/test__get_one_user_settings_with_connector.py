import vampytest

from ..cache import USER_SETTINGS_CACHE, put_one_to_cache
from ..user_settings import UserSettings
from ..queries import get_one_user_settings_with_connector


async def test__get_one_user_settings_with_connector__cache_hit():
    """
    Tests whether ``get_one_user_settings_with_connector`` works as intended.
    
    Case: Cache hit.
    
    This function is a coroutine.
    """
    query_called = False
    connector = object()
    
    user_id = 202309240060
    user_settings = UserSettings(user_id, notification_daily_by_waifu = False)
    
    async def query(user_id, connector):
        nonlocal query_called
        query_called = True
        
        return None
    
    
    mocked = vampytest.mock_globals(
        get_one_user_settings_with_connector,
        query_one_touhou_user_settings_with_connector = query,
    )
    
    try:
        put_one_to_cache(user_settings)
        
        output = await mocked(user_id, connector)
        
        vampytest.assert_eq(output, user_settings)
        
        vampytest.assert_false(query_called)
    finally:
        USER_SETTINGS_CACHE.clear()


async def test__get_one_user_settings_with_connector__database_hit_value():
    """
    Tests whether ``get_one_user_settings_with_connector`` works as intended.
    
    Case: Database hit with value.
    
    This function is a coroutine.
    """
    query_called = False
    connector = object()
    called_with_user_id = 0
    called_connector_with = None
    
    user_id = 202309240061
    user_settings = UserSettings(user_id, notification_daily_by_waifu = False)
    
    async def query(user_id, connector):
        nonlocal query_called
        nonlocal called_with_user_id
        nonlocal user_settings
        nonlocal called_connector_with
        
        query_called = True
        called_with_user_id = user_id
        called_connector_with = connector
        
        return user_settings
    
    
    mocked = vampytest.mock_globals(
        get_one_user_settings_with_connector,
        _query_one_user_settings_with_connector = query,
    )
    
    try:
        output = await mocked(user_id, connector)
        
        vampytest.assert_eq(output, user_settings)
        
        vampytest.assert_true(query_called)
        vampytest.assert_eq(called_with_user_id, user_id)
        vampytest.assert_is(called_connector_with, connector)
        
        vampytest.assert_eq([*USER_SETTINGS_CACHE.items()], [(user_id, user_settings)])
    finally:
        USER_SETTINGS_CACHE.clear()


async def test__get_one_user_settings_with_connector__database_hit_none():
    """
    Tests whether ``get_one_user_settings_with_connector`` works as intended.
    
    Case: Database hit with none.
    
    This function is a coroutine.
    """
    query_called = False
    connector = object()
    called_with_user_id = 0
    called_connector_with = None
    
    user_id = 202309240062
    user_settings = None
    
    async def query(user_id, connector):
        nonlocal query_called
        nonlocal called_with_user_id
        nonlocal user_settings
        nonlocal called_connector_with
        
        query_called = True
        called_with_user_id = user_id
        called_connector_with = connector
        
        return user_settings
    
    
    mocked = vampytest.mock_globals(
        get_one_user_settings_with_connector,
        _query_one_user_settings_with_connector = query,
    )
    
    try:
        output = await mocked(user_id, connector)
        
        vampytest.assert_eq(output, UserSettings(user_id))
        
        vampytest.assert_true(query_called)
        vampytest.assert_eq(called_with_user_id, user_id)
        vampytest.assert_is(called_connector_with, connector)
        
        vampytest.assert_eq([*USER_SETTINGS_CACHE.items()], [(user_id, user_settings)])
    finally:
        USER_SETTINGS_CACHE.clear()
