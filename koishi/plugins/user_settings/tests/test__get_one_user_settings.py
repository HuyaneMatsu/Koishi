import vampytest

from ..cache import USER_SETTINGS_CACHE, put_one_to_cache
from ..user_settings import UserSettings
from ..queries import get_one_user_settings


async def test__get_one_user_settings__cache_hit():
    """
    Tests whether ``get_one_user_settings`` works as intended.
    
    Case: Cache hit.
    
    This function is a coroutine.
    """
    query_called = False
    
    user_id = 202309240050
    user_settings = UserSettings(user_id, notification_daily_by_waifu = False)
    
    async def query(user_id):
        nonlocal query_called
        query_called = True
    
    
    mocked = vampytest.mock_globals(
        get_one_user_settings,
        query_one_touhou_user_settings = query,
    )
    
    try:
        put_one_to_cache(user_settings)
        
        output = await mocked(user_id)
        
        vampytest.assert_eq(output, user_settings)
        
        vampytest.assert_false(query_called)
    finally:
        USER_SETTINGS_CACHE.clear()


async def test__get_one_user_settings__database_hit_value():
    """
    Tests whether ``get_one_user_settings`` works as intended.
    
    Case: Database hit with value.
    
    This function is a coroutine.
    """
    query_called = False
    called_with_user_id = 0
    
    user_id = 202309240051
    user_settings = UserSettings(user_id, notification_daily_by_waifu = False)
    
    async def query(user_id):
        nonlocal query_called
        nonlocal called_with_user_id
        nonlocal user_settings
        
        query_called = True
        called_with_user_id = user_id
        
        return user_settings
    
    
    mocked = vampytest.mock_globals(
        get_one_user_settings,
        _query_one_user_settings = query,
    )
    
    try:
        output = await mocked(user_id)
        
        vampytest.assert_eq(output, user_settings)
        
        vampytest.assert_true(query_called)
        vampytest.assert_eq(called_with_user_id, user_id)
        
        vampytest.assert_eq([*USER_SETTINGS_CACHE.items()], [(user_id, user_settings)])
    finally:
        USER_SETTINGS_CACHE.clear()


async def test__get_one_user_settings__database_hit_none():
    """
    Tests whether ``get_one_user_settings`` works as intended.
    
    Case: Database hit with none.
    
    This function is a coroutine.
    """
    query_called = False
    called_with_user_id = 0
    
    user_id = 202309240052
    user_settings = None
    
    async def query(user_id):
        nonlocal query_called
        nonlocal called_with_user_id
        nonlocal user_settings
        
        query_called = True
        called_with_user_id = user_id
        
        return user_settings
    
    
    mocked = vampytest.mock_globals(
        get_one_user_settings,
        _query_one_user_settings = query,
    )
    
    try:
        output = await mocked(user_id)
        
        vampytest.assert_eq(output, UserSettings(user_id))
        
        vampytest.assert_true(query_called)
        vampytest.assert_eq(called_with_user_id, user_id)
        
        vampytest.assert_eq([*USER_SETTINGS_CACHE.items()], [(user_id, user_settings)])
    finally:
        USER_SETTINGS_CACHE.clear()
