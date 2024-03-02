import vampytest

from ..cache import NOTIFICATION_SETTINGS_CACHE, get_more_from_cache
from ..notification_settings import NotificationSettings


def test__get_more_from_cache__miss():
    """
    Tests whether ``get_more_from_cache`` works as intended.
    
    Case: miss.
    """
    user_id_0 = 202309240006
    user_id_1 = 202309240007
    try:
        results, misses = get_more_from_cache([user_id_0, user_id_1])
        
        vampytest.assert_instance(results, list, nullable = True)
        vampytest.assert_instance(misses, list, nullable = True)
        
        vampytest.assert_is(results, None)
        vampytest.assert_eq(misses, [user_id_0, user_id_1])
    
    finally:
        NOTIFICATION_SETTINGS_CACHE.clear()


def test__get_more_from_cache__hit_none():
    """
    Tests whether ``get_more_from_cache`` works as intended.
    
    Case: hit, but None.
    """
    user_id_0 = 202309240008
    user_id_1 = 202309240009
    
    notification_settings_0 = None
    notification_settings_1 = None
    
    try:
        NOTIFICATION_SETTINGS_CACHE[user_id_0] = notification_settings_0
        NOTIFICATION_SETTINGS_CACHE[user_id_1] = notification_settings_1
        
        results, misses = get_more_from_cache([user_id_0, user_id_1])
        
        vampytest.assert_instance(results, list, nullable = True)
        vampytest.assert_instance(misses, list, nullable = True)
        
        vampytest.assert_eq(results, [NotificationSettings(user_id_0), NotificationSettings(user_id_1)])
        vampytest.assert_eq(misses, None)
    
    finally:
        NOTIFICATION_SETTINGS_CACHE.clear()


def test__get_more_from_cache__hit_value():
    """
    Tests whether ``get_more_from_cache`` works as intended.
    
    Case: hit, actual values.
    """
    user_id_0 = 202309240010
    user_id_1 = 202309240011
    
    notification_settings_0 = NotificationSettings(user_id_0, daily_by_waifu = False)
    notification_settings_1 = NotificationSettings(user_id_0, proposal = False)
    
    try:
        NOTIFICATION_SETTINGS_CACHE[user_id_0] = notification_settings_0
        NOTIFICATION_SETTINGS_CACHE[user_id_1] = notification_settings_1
        
        results, misses = get_more_from_cache([user_id_0, user_id_1])
        
        vampytest.assert_instance(results, list, nullable = True)
        vampytest.assert_instance(misses, list, nullable = True)
        
        vampytest.assert_eq(results, [notification_settings_0, notification_settings_1])
        vampytest.assert_eq(misses, None)
    
    finally:
        NOTIFICATION_SETTINGS_CACHE.clear()


def test__get_more_from_cache__hit_and_value():
    """
    Tests whether ``get_more_from_cache`` works as intended.
    
    Case: hit, actual values.
    """
    user_id_0 = 202309240014
    user_id_1 = 202309240015
    
    notification_settings_0 = NotificationSettings(user_id_0, daily_by_waifu = False)
    
    try:
        NOTIFICATION_SETTINGS_CACHE[user_id_0] = notification_settings_0
        
        results, misses = get_more_from_cache([user_id_0, user_id_1])
        
        vampytest.assert_instance(results, list, nullable = True)
        vampytest.assert_instance(misses, list, nullable = True)
        
        vampytest.assert_eq(results, [notification_settings_0])
        vampytest.assert_eq(misses, [user_id_1])
    
    finally:
        NOTIFICATION_SETTINGS_CACHE.clear()


def test__get_more_from_cache__hit_and_move():
    """
    Tests whether ``get_more_from_cache`` works as intended.
    
    Case: hit, move hit to end.
    """
    user_id_0 = 202309240012
    user_id_1 = 202309240013
    
    notification_settings_0 = None
    notification_settings_1 = None
    
    try:
        NOTIFICATION_SETTINGS_CACHE[user_id_0] = notification_settings_0
        NOTIFICATION_SETTINGS_CACHE[user_id_1] = notification_settings_1
        
        vampytest.assert_eq([*NOTIFICATION_SETTINGS_CACHE.items()], [(user_id_0, None), (user_id_1, None)])
        
        get_more_from_cache([user_id_0])
        
        vampytest.assert_eq([*NOTIFICATION_SETTINGS_CACHE.items()], [(user_id_1, None), (user_id_0, None)])
    
    finally:
        NOTIFICATION_SETTINGS_CACHE.clear()
