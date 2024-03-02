import vampytest

from ..cache import NOTIFICATION_SETTINGS_CACHE, put_none_to_cache
from ..notification_settings import NotificationSettings


def test__put_none_to_cache__value():
    """
    Tests whether ``put_none_to_cache`` works as intended.
    
    Case: actual value.
    """
    user_id = 202309240040
    
    notification_settings = NotificationSettings(user_id, daily_by_waifu = False)
    
    try:
        NOTIFICATION_SETTINGS_CACHE[user_id] = notification_settings
        
        put_none_to_cache(user_id)
        
        vampytest.assert_eq([*NOTIFICATION_SETTINGS_CACHE.items()], [(user_id, None)])
    
    finally:
        NOTIFICATION_SETTINGS_CACHE.clear()


def test__put_none_to_cache__move():
    """
    Tests whether ``put_none_to_cache`` works as intended.
    
    Case: move to end.
    """
    user_id_0 = 202309240041
    user_id_1 = 202309240042
    
    notification_settings_0 = NotificationSettings(user_id_0)
    notification_settings_1 = NotificationSettings(user_id_1)
    
    try:
        NOTIFICATION_SETTINGS_CACHE[user_id_0] = notification_settings_0
        NOTIFICATION_SETTINGS_CACHE[user_id_1] = notification_settings_1
        
        put_none_to_cache(user_id_0)
        
        vampytest.assert_eq(
            [*NOTIFICATION_SETTINGS_CACHE.items()],
            [(user_id_1, notification_settings_1), (user_id_0, None)],
        )
    
    finally:
        NOTIFICATION_SETTINGS_CACHE.clear()


def test__put_none_to_cache__pop():
    """
    Tests whether ``put_none_to_cache`` works as intended.
    
    Case: Cache full.
    """
    user_id_0 = 202309240043
    user_id_1 = 202309240044
    
    try:
        NOTIFICATION_SETTINGS_CACHE[user_id_0] = None
        
        mocked = vampytest.mock_globals(put_none_to_cache, NOTIFICATION_SETTINGS_CACHE_MAX_SIZE = 1)
        
        mocked(user_id_1)
        
        vampytest.assert_eq([*NOTIFICATION_SETTINGS_CACHE.items()], [(user_id_1, None)])
    
    finally:
        NOTIFICATION_SETTINGS_CACHE.clear()
