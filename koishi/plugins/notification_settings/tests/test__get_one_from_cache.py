import vampytest

from ..cache import NOTIFICATION_SETTINGS_CACHE, get_one_from_cache
from ..notification_settings import NotificationSettings


def test__get_one_from_cache__miss():
    """
    Tests whether ``get_one_from_cache`` works as intended.
    
    Case: miss.
    """
    user_id = 202309240000
    try:
        result, miss = get_one_from_cache(user_id)
        
        vampytest.assert_instance(result, NotificationSettings, nullable = True)
        vampytest.assert_instance(miss, bool)
        
        vampytest.assert_is(result, None)
        vampytest.assert_eq(miss, True)
    
    finally:
        NOTIFICATION_SETTINGS_CACHE.clear()


def test__get_one_from_cache__hit_none():
    """
    Tests whether ``get_one_from_cache`` works as intended.
    
    Case: git, but None.
    """
    user_id = 202309240001
    notification_settings = None
    
    try:
        NOTIFICATION_SETTINGS_CACHE[user_id] = notification_settings
        
        result, miss = get_one_from_cache(user_id)
        
        vampytest.assert_instance(result, NotificationSettings, nullable = True)
        vampytest.assert_instance(miss, bool)
        
        vampytest.assert_eq(result, NotificationSettings(user_id))
        vampytest.assert_eq(miss, False)
    
    finally:
        NOTIFICATION_SETTINGS_CACHE.clear()


def test__get_one_from_cache__hit_value():
    """
    Tests whether ``get_one_from_cache`` works as intended.
    
    Case: hiz, actual values.
    """
    user_id = 202309240002
    notification_settings = NotificationSettings(user_id, daily_by_waifu = False)
    
    try:
        NOTIFICATION_SETTINGS_CACHE[user_id] = notification_settings
        
        result, miss = get_one_from_cache(user_id)
        
        vampytest.assert_instance(result, NotificationSettings, nullable = True)
        vampytest.assert_instance(miss, bool)
        
        vampytest.assert_eq(result, notification_settings)
        vampytest.assert_eq(miss, False)
    
    finally:
        NOTIFICATION_SETTINGS_CACHE.clear()


def test__get_one_from_cache__hit_and_move():
    """
    Tests whether ``get_one_from_cache`` works as intended.
    
    Case: hiz, move to end.
    """
    user_id_0 = 202309240003
    user_id_1 = 202309240004
    
    try:
        NOTIFICATION_SETTINGS_CACHE[user_id_0] = None
        NOTIFICATION_SETTINGS_CACHE[user_id_1] = None
        
        vampytest.assert_eq([*NOTIFICATION_SETTINGS_CACHE.items()], [(user_id_0, None), (user_id_1, None)])
        
        get_one_from_cache(user_id_0)
        
        vampytest.assert_eq([*NOTIFICATION_SETTINGS_CACHE.items()], [(user_id_1, None), (user_id_0, None)])
    
    finally:
        NOTIFICATION_SETTINGS_CACHE.clear()
