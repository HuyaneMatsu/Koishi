import vampytest


from ..cache import NOTIFICATION_SETTINGS_CACHE, put_more_to_cache
from ..notification_settings import NotificationSettings


def test__put_more_to_cache__none():
    """
    Tests whether ``put_more_to_cache`` works as intended.
    
    Case: None.
    """
    user_id_0 = 202309240030
    user_id_1 = 202309240031
    
    notification_settings = None
    
    try:
        put_more_to_cache(notification_settings)
        
        vampytest.assert_eq([*NOTIFICATION_SETTINGS_CACHE.items()], [])
    
    finally:
        NOTIFICATION_SETTINGS_CACHE.clear()


def test__put_more_to_cache__value():
    """
    Tests whether ``put_more_to_cache`` works as intended.
    
    Case: actual value.
    """
    user_id_0 = 202309240032
    user_id_1 = 202309240033
    
    notification_settings_0 = NotificationSettings(user_id_0, daily = False)
    notification_settings_1 = NotificationSettings(user_id_1, proposal = False)
    
    try:
        put_more_to_cache([notification_settings_0, notification_settings_1])
        
        vampytest.assert_eq(
            [*NOTIFICATION_SETTINGS_CACHE.items()],
            [(user_id_0, notification_settings_0), (user_id_1, notification_settings_1)],
        )
    
    finally:
        NOTIFICATION_SETTINGS_CACHE.clear()


def test__put_more_to_cache__move():
    """
    Tests whether ``put_more_to_cache`` works as intended.
    
    Case: move to end.
    """
    user_id_0 = 202309240035
    user_id_1 = 202309240036
    
    notification_settings_0 = NotificationSettings(user_id_0)
    
    try:
        NOTIFICATION_SETTINGS_CACHE[user_id_0] = None
        NOTIFICATION_SETTINGS_CACHE[user_id_1] = None
        
        put_more_to_cache([notification_settings_0])
        
        vampytest.assert_eq(
            [*NOTIFICATION_SETTINGS_CACHE.items()],
            [(user_id_1, None), (user_id_0, notification_settings_0)],
        )
    
    finally:
        NOTIFICATION_SETTINGS_CACHE.clear()


def test__put_more_to_cache__pop():
    """
    Tests whether ``put_more_to_cache`` works as intended.
    
    Case: Cache full.
    """
    user_id_0 = 202309240037
    user_id_1 = 202309240038
    
    notification_settings_1 = NotificationSettings(user_id_1)
    
    try:
        NOTIFICATION_SETTINGS_CACHE[user_id_0] = None
        
        mocked = vampytest.mock_globals(put_more_to_cache, 2, NOTIFICATION_SETTINGS_CACHE_MAX_SIZE = 1)
        
        mocked([notification_settings_1])
        
        vampytest.assert_eq([*NOTIFICATION_SETTINGS_CACHE.items()], [(user_id_1, notification_settings_1)])
    
    finally:
        NOTIFICATION_SETTINGS_CACHE.clear()
