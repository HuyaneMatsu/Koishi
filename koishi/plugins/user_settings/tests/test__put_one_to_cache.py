import vampytest

from ..cache import USER_SETTINGS_CACHE, put_one_to_cache
from ..user_settings import UserSettings


def test__put_one_to_cache__value():
    """
    Tests whether ``put_one_to_cache`` works as intended.
    
    Case: actual value.
    """
    user_id = 202309240021
    
    user_settings = UserSettings(user_id, notification_daily_by_waifu = False)
    
    try:
        put_one_to_cache(user_settings)
        
        vampytest.assert_eq([*USER_SETTINGS_CACHE.items()], [(user_id, user_settings)])
    
    finally:
        USER_SETTINGS_CACHE.clear()


def test__put_one_to_cache__move():
    """
    Tests whether ``put_one_to_cache`` works as intended.
    
    Case: move to end.
    """
    user_id_0 = 202309240022
    user_id_1 = 202309240023
    
    user_settings_0 = UserSettings(user_id_0)
    
    try:
        USER_SETTINGS_CACHE[user_id_0] = None
        USER_SETTINGS_CACHE[user_id_1] = None
        
        put_one_to_cache(user_settings_0)
        
        vampytest.assert_eq(
            [*USER_SETTINGS_CACHE.items()],
            [(user_id_1, None), (user_id_0, user_settings_0)],
        )
    
    finally:
        USER_SETTINGS_CACHE.clear()


def test__put_one_to_cache__pop():
    """
    Tests whether ``put_one_to_cache`` works as intended.
    
    Case: Cache full.
    """
    user_id_0 = 202309240024
    user_id_1 = 202309240025
    
    user_settings_1 = UserSettings(user_id_1)
    
    try:
        USER_SETTINGS_CACHE[user_id_0] = None
        
        mocked = vampytest.mock_globals(put_one_to_cache, USER_SETTINGS_CACHE_MAX_SIZE = 1)
        
        mocked(user_settings_1)
        
        vampytest.assert_eq([*USER_SETTINGS_CACHE.items()], [(user_id_1, user_settings_1)])
    
    finally:
        USER_SETTINGS_CACHE.clear()
