import vampytest


from ..cache import USER_SETTINGS_CACHE, put_more_to_cache
from ..user_settings import UserSettings


def test__put_more_to_cache__none():
    """
    Tests whether ``put_more_to_cache`` works as intended.
    
    Case: None.
    """
    user_id_0 = 202309240030
    user_id_1 = 202309240031
    
    user_settings = None
    
    try:
        put_more_to_cache(user_settings)
        
        vampytest.assert_eq([*USER_SETTINGS_CACHE.items()], [])
    
    finally:
        USER_SETTINGS_CACHE.clear()


def test__put_more_to_cache__value():
    """
    Tests whether ``put_more_to_cache`` works as intended.
    
    Case: actual value.
    """
    user_id_0 = 202309240032
    user_id_1 = 202309240033
    
    user_settings_0 = UserSettings(user_id_0, notification_daily_by_waifu = False)
    user_settings_1 = UserSettings(user_id_1, notification_proposal = False)
    
    try:
        put_more_to_cache([user_settings_0, user_settings_1])
        
        vampytest.assert_eq(
            [*USER_SETTINGS_CACHE.items()],
            [(user_id_0, user_settings_0), (user_id_1, user_settings_1)],
        )
    
    finally:
        USER_SETTINGS_CACHE.clear()


def test__put_more_to_cache__move():
    """
    Tests whether ``put_more_to_cache`` works as intended.
    
    Case: move to end.
    """
    user_id_0 = 202309240035
    user_id_1 = 202309240036
    
    user_settings_0 = UserSettings(user_id_0)
    
    try:
        USER_SETTINGS_CACHE[user_id_0] = None
        USER_SETTINGS_CACHE[user_id_1] = None
        
        put_more_to_cache([user_settings_0])
        
        vampytest.assert_eq(
            [*USER_SETTINGS_CACHE.items()],
            [(user_id_1, None), (user_id_0, user_settings_0)],
        )
    
    finally:
        USER_SETTINGS_CACHE.clear()


def test__put_more_to_cache__pop():
    """
    Tests whether ``put_more_to_cache`` works as intended.
    
    Case: Cache full.
    """
    user_id_0 = 202309240037
    user_id_1 = 202309240038
    
    user_settings_1 = UserSettings(user_id_1)
    
    try:
        USER_SETTINGS_CACHE[user_id_0] = None
        
        mocked = vampytest.mock_globals(put_more_to_cache, 2, USER_SETTINGS_CACHE_MAX_SIZE = 1)
        
        mocked([user_settings_1])
        
        vampytest.assert_eq([*USER_SETTINGS_CACHE.items()], [(user_id_1, user_settings_1)])
    
    finally:
        USER_SETTINGS_CACHE.clear()
