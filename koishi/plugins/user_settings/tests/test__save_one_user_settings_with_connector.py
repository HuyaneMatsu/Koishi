import vampytest

from ..cache import USER_SETTINGS_CACHE, put_none_to_cache, put_one_to_cache
from ..user_settings import UserSettings
from ..queries import save_one_user_settings_with_connector


async def test__save_one_user_settings_with_connector__save_and_move():
    """
    Tests whether ``save_one_user_settings_with_connector`` works as intended.
    
    Case: saving and moving to end.
    
    This function is a coroutine.
    """
    query_called = False
    user_id_0 = 202309250010
    user_id_1 = 202309250011
    user_settings = UserSettings(user_id_0, notification_daily_by_waifu = False)
    called_with_user_settings = None
    connector = object()
    called_with_connector = None
    
    
    async def query(user_settings, connector):
        nonlocal query_called
        nonlocal called_with_user_settings
        nonlocal called_with_connector
        
        query_called = True
        called_with_user_settings = user_settings
        called_with_connector = connector
    
    
    mocked = vampytest.mock_globals(
        save_one_user_settings_with_connector,
        _save_user_settings_with_connector = query,
    )
    
    try:
        put_none_to_cache(user_id_0)
        put_none_to_cache(user_id_1)
        
        await mocked(user_settings, connector)
        
        
        vampytest.assert_true(query_called)
        vampytest.assert_eq(called_with_user_settings, user_settings)
        vampytest.assert_is(called_with_connector, connector)
        
        vampytest.assert_eq(
            [*USER_SETTINGS_CACHE.items()],
            [(user_id_1, None), (user_id_0, user_settings)],
        )
        
    finally:
        USER_SETTINGS_CACHE.clear()


async def test__save_one_user_settings_with_connector__delete_and_move():
    """
    Tests whether ``save_one_user_settings_with_connector`` works as intended.
    
    Case: delete and moving to end.
    
    This function is a coroutine.
    """
    query_called = False
    user_id_0 = 202309250012
    user_id_1 = 202309250013
    user_settings = UserSettings(user_id_0, notification_daily_by_waifu = False)
    called_with_user_settings = None
    connector = object()
    called_with_connector = None
    
    async def query(user_settings, connector):
        nonlocal query_called
        nonlocal called_with_user_settings
        nonlocal called_with_connector
        
        query_called = True
        called_with_user_settings = user_settings
        called_with_connector = connector
    
    
    mocked = vampytest.mock_globals(
        save_one_user_settings_with_connector,
        _remove_user_settings_with_connector = query,
    )
    
    try:
        put_one_to_cache(user_settings)
        put_none_to_cache(user_id_1)
        
        user_settings = UserSettings(user_id_0)
        
        await mocked(user_settings, connector)
        
        
        vampytest.assert_true(query_called)
        vampytest.assert_eq(called_with_user_settings, user_settings)
        vampytest.assert_is(called_with_connector, connector)
        
        vampytest.assert_eq(
            [*USER_SETTINGS_CACHE.items()],
            [(user_id_1, None), (user_id_0, None)],
        )
        
    finally:
        USER_SETTINGS_CACHE.clear()
