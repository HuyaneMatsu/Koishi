import vampytest

from ..cache import USER_SETTINGS_CACHE, get_more_from_cache
from ..user_settings import UserSettings


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
        USER_SETTINGS_CACHE.clear()


def test__get_more_from_cache__hit_none():
    """
    Tests whether ``get_more_from_cache`` works as intended.
    
    Case: hit, but None.
    """
    user_id_0 = 202309240008
    user_id_1 = 202309240009
    
    user_settings_0 = None
    user_settings_1 = None
    
    try:
        USER_SETTINGS_CACHE[user_id_0] = user_settings_0
        USER_SETTINGS_CACHE[user_id_1] = user_settings_1
        
        results, misses = get_more_from_cache([user_id_0, user_id_1])
        
        vampytest.assert_instance(results, list, nullable = True)
        vampytest.assert_instance(misses, list, nullable = True)
        
        vampytest.assert_eq(results, [UserSettings(user_id_0), UserSettings(user_id_1)])
        vampytest.assert_eq(misses, None)
    
    finally:
        USER_SETTINGS_CACHE.clear()


def test__get_more_from_cache__hit_value():
    """
    Tests whether ``get_more_from_cache`` works as intended.
    
    Case: hit, actual values.
    """
    user_id_0 = 202309240010
    user_id_1 = 202309240011
    
    user_settings_0 = UserSettings(user_id_0, notification_daily_by_waifu = False)
    user_settings_1 = UserSettings(user_id_0, notification_proposal = False)
    
    try:
        USER_SETTINGS_CACHE[user_id_0] = user_settings_0
        USER_SETTINGS_CACHE[user_id_1] = user_settings_1
        
        results, misses = get_more_from_cache([user_id_0, user_id_1])
        
        vampytest.assert_instance(results, list, nullable = True)
        vampytest.assert_instance(misses, list, nullable = True)
        
        vampytest.assert_eq(results, [user_settings_0, user_settings_1])
        vampytest.assert_eq(misses, None)
    
    finally:
        USER_SETTINGS_CACHE.clear()


def test__get_more_from_cache__hit_and_value():
    """
    Tests whether ``get_more_from_cache`` works as intended.
    
    Case: hit, actual values.
    """
    user_id_0 = 202309240014
    user_id_1 = 202309240015
    
    user_settings_0 = UserSettings(user_id_0, notification_daily_by_waifu = False)
    
    try:
        USER_SETTINGS_CACHE[user_id_0] = user_settings_0
        
        results, misses = get_more_from_cache([user_id_0, user_id_1])
        
        vampytest.assert_instance(results, list, nullable = True)
        vampytest.assert_instance(misses, list, nullable = True)
        
        vampytest.assert_eq(results, [user_settings_0])
        vampytest.assert_eq(misses, [user_id_1])
    
    finally:
        USER_SETTINGS_CACHE.clear()


def test__get_more_from_cache__hit_and_move():
    """
    Tests whether ``get_more_from_cache`` works as intended.
    
    Case: hit, move hit to end.
    """
    user_id_0 = 202309240012
    user_id_1 = 202309240013
    
    user_settings_0 = None
    user_settings_1 = None
    
    try:
        USER_SETTINGS_CACHE[user_id_0] = user_settings_0
        USER_SETTINGS_CACHE[user_id_1] = user_settings_1
        
        vampytest.assert_eq([*USER_SETTINGS_CACHE.items()], [(user_id_0, None), (user_id_1, None)])
        
        get_more_from_cache([user_id_0])
        
        vampytest.assert_eq([*USER_SETTINGS_CACHE.items()], [(user_id_1, None), (user_id_0, None)])
    
    finally:
        USER_SETTINGS_CACHE.clear()
