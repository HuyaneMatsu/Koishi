import vampytest

from ..cache import USER_SETTINGS_CACHE, put_none_to_cache, put_one_to_cache
from ..user_settings import UserSettings
from ..queries import save_one_user_settings


async def test__save_one_user_settings__save_and_move():
    """
    Tests whether ``save_one_user_settings`` works as intended.
    
    Case: saving and moving to end.
    
    This function is a coroutine.
    """
    query_called = False
    user_id_0 = 202309250000
    user_id_1 = 202309250001
    user_settings = UserSettings(user_id_0, notification_daily_by_waifu = False)
    called_with_user_settings = None
    
    async def query(user_settings):
        nonlocal query_called
        nonlocal called_with_user_settings
        
        query_called = True
        called_with_user_settings = user_settings
    
    
    mocked = vampytest.mock_globals(
        save_one_user_settings,
        _save_user_settings = query,
    )
    
    try:
        put_none_to_cache(user_id_0)
        put_none_to_cache(user_id_1)
        
        await mocked(user_settings)
        
        
        vampytest.assert_true(query_called)
        vampytest.assert_eq(called_with_user_settings, user_settings)
        
        vampytest.assert_eq(
            [*USER_SETTINGS_CACHE.items()],
            [(user_id_1, None), (user_id_0, user_settings)],
        )
        
    finally:
        USER_SETTINGS_CACHE.clear()


async def test__save_one_user_settings__delete_and_move():
    """
    Tests whether ``save_one_user_settings`` works as intended.
    
    Case: delete and moving to end.
    
    This function is a coroutine.
    """
    query_called = False
    user_id_0 = 202309250002
    user_id_1 = 202309250003
    user_settings = UserSettings(user_id_0, notification_daily_by_waifu = False)
    called_with_user_settings = None
    
    async def query(user_settings):
        nonlocal query_called
        nonlocal called_with_user_settings
        
        query_called = True
        called_with_user_settings = user_settings
    
    
    mocked = vampytest.mock_globals(
        save_one_user_settings,
        _remove_user_settings = query,
    )
    
    try:
        put_one_to_cache(user_settings)
        put_none_to_cache(user_id_1)
        
        user_settings = UserSettings(user_id_0)
        
        await mocked(user_settings)
        
        
        vampytest.assert_true(query_called)
        vampytest.assert_eq(called_with_user_settings, user_settings)
        
        vampytest.assert_eq(
            [*USER_SETTINGS_CACHE.items()],
            [(user_id_1, None), (user_id_0, None)],
        )
        
    finally:
        USER_SETTINGS_CACHE.clear()
