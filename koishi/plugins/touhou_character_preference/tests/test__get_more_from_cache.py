import vampytest

from ..cache import CHARACTER_PREFERENCE_CACHE, get_more_from_cache
from ..character_preference import CharacterPreference


def test__get_more_from_cache__miss():
    """
    Tests whether ``get_more_from_cache`` works as intended.
    
    Case: miss.
    """
    user_id_0 = 202309160006
    user_id_1 = 202309160007
    try:
        results, misses = get_more_from_cache([user_id_0, user_id_1])
        
        vampytest.assert_instance(results, list, nullable = True)
        vampytest.assert_instance(misses, list, nullable = True)
        
        vampytest.assert_is(results, None)
        vampytest.assert_eq(misses, [user_id_0, user_id_1])
    
    finally:
        CHARACTER_PREFERENCE_CACHE.clear()


def test__get_more_from_cache__hit_none():
    """
    Tests whether ``get_more_from_cache`` works as intended.
    
    Case: hit, but None.
    """
    user_id_0 = 202309160008
    user_id_1 = 202309160009
    
    character_preferences_0 = None
    character_preferences_1 = None
    
    try:
        CHARACTER_PREFERENCE_CACHE[user_id_0] = character_preferences_0
        CHARACTER_PREFERENCE_CACHE[user_id_1] = character_preferences_1
        
        results, misses = get_more_from_cache([user_id_0, user_id_1])
        
        vampytest.assert_instance(results, list, nullable = True)
        vampytest.assert_instance(misses, list, nullable = True)
        
        vampytest.assert_is(results, None)
        vampytest.assert_eq(misses, None)
    
    finally:
        CHARACTER_PREFERENCE_CACHE.clear()


def test__get_more_from_cache__hit_value():
    """
    Tests whether ``get_more_from_cache`` works as intended.
    
    Case: hit, actual values.
    """
    user_id_0 = 202309160010
    user_id_1 = 202309160011
    
    character_preferences_0 = [
        CharacterPreference(user_id_0, 'komeiji_koishi'),
        CharacterPreference(user_id_0, 'komeiji_satori'),
    ]
    
    character_preferences_1 = [
        CharacterPreference(user_id_1, 'kaenbyou_rin'),
        CharacterPreference(user_id_1, 'reiuji_utsuho'),
    ]
    
    try:
        CHARACTER_PREFERENCE_CACHE[user_id_0] = character_preferences_0
        CHARACTER_PREFERENCE_CACHE[user_id_1] = character_preferences_1
        
        results, misses = get_more_from_cache([user_id_0, user_id_1])
        
        vampytest.assert_instance(results, list, nullable = True)
        vampytest.assert_instance(misses, list, nullable = True)
        
        vampytest.assert_eq(results, [*character_preferences_0, *character_preferences_1])
        vampytest.assert_eq(misses, None)
    
    finally:
        CHARACTER_PREFERENCE_CACHE.clear()


def test__get_more_from_cache__hit_and_value():
    """
    Tests whether ``get_more_from_cache`` works as intended.
    
    Case: hit, actual values.
    """
    user_id_0 = 202309160014
    user_id_1 = 202309160015
    
    character_preferences_0 = [
        CharacterPreference(user_id_0, 'komeiji_koishi'),
        CharacterPreference(user_id_0, 'komeiji_satori'),
    ]
    
    try:
        CHARACTER_PREFERENCE_CACHE[user_id_0] = character_preferences_0
        
        results, misses = get_more_from_cache([user_id_0, user_id_1])
        
        vampytest.assert_instance(results, list, nullable = True)
        vampytest.assert_instance(misses, list, nullable = True)
        
        vampytest.assert_eq(results, [*character_preferences_0])
        vampytest.assert_eq(misses, [user_id_1])
    
    finally:
        CHARACTER_PREFERENCE_CACHE.clear()


def test__get_more_from_cache__hit_and_move():
    """
    Tests whether ``get_more_from_cache`` works as intended.
    
    Case: hit, move hit to end.
    """
    user_id_0 = 202309160012
    user_id_1 = 202309160013
    
    character_preferences_0 = None
    character_preferences_1 = None
    
    try:
        CHARACTER_PREFERENCE_CACHE[user_id_0] = character_preferences_0
        CHARACTER_PREFERENCE_CACHE[user_id_1] = character_preferences_1
        
        vampytest.assert_eq([*CHARACTER_PREFERENCE_CACHE.items()], [(user_id_0, None), (user_id_1, None)])
        
        get_more_from_cache([user_id_0])
        
        vampytest.assert_eq([*CHARACTER_PREFERENCE_CACHE.items()], [(user_id_1, None), (user_id_0, None)])
    
    finally:
        CHARACTER_PREFERENCE_CACHE.clear()
