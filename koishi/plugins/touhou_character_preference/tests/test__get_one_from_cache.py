import vampytest

from ..cache import CHARACTER_PREFERENCE_CACHE, get_one_from_cache
from ..character_preference import CharacterPreference


def test__get_one_from_cache__miss():
    """
    Tests whether ``get_one_from_cache`` works as intended.
    
    Case: miss.
    """
    user_id = 202309160000
    try:
        result, miss = get_one_from_cache(user_id)
        
        vampytest.assert_instance(result, list, nullable = True)
        vampytest.assert_instance(miss, bool)
        
        vampytest.assert_is(result, None)
        vampytest.assert_eq(miss, True)
    
    finally:
        CHARACTER_PREFERENCE_CACHE.clear()


def test__get_one_from_cache__hit_none():
    """
    Tests whether ``get_one_from_cache`` works as intended.
    
    Case: git, but None.
    """
    user_id = 202309160001
    character_preferences = None
    
    try:
        CHARACTER_PREFERENCE_CACHE[user_id] = character_preferences
        
        result, miss = get_one_from_cache(user_id)
        
        vampytest.assert_instance(result, list, nullable = True)
        vampytest.assert_instance(miss, bool)
        
        vampytest.assert_eq(result, character_preferences)
        vampytest.assert_eq(miss, False)
    
    finally:
        CHARACTER_PREFERENCE_CACHE.clear()


def test__get_one_from_cache__hit_value():
    """
    Tests whether ``get_one_from_cache`` works as intended.
    
    Case: hiz, actual values.
    """
    user_id = 202309160002
    character_preferences = [
        CharacterPreference(user_id, 'komeiji_koishi'),
        CharacterPreference(user_id, 'komeiji_satori'),
    ]
    
    try:
        CHARACTER_PREFERENCE_CACHE[user_id] = character_preferences
        
        result, miss = get_one_from_cache(user_id)
        
        vampytest.assert_instance(result, list, nullable = True)
        vampytest.assert_instance(miss, bool)
        
        vampytest.assert_eq(result, character_preferences)
        vampytest.assert_eq(miss, False)
    
    finally:
        CHARACTER_PREFERENCE_CACHE.clear()


def test__get_one_from_cache__hit_and_move():
    """
    Tests whether ``get_one_from_cache`` works as intended.
    
    Case: hiz, move to end.
    """
    user_id_0 = 202309160003
    user_id_1 = 202309160004
    
    try:
        CHARACTER_PREFERENCE_CACHE[user_id_0] = None
        CHARACTER_PREFERENCE_CACHE[user_id_1] = None
        
        vampytest.assert_eq([*CHARACTER_PREFERENCE_CACHE.items()], [(user_id_0, None), (user_id_1, None)])
        
        get_one_from_cache(user_id_0)
        
        vampytest.assert_eq([*CHARACTER_PREFERENCE_CACHE.items()], [(user_id_1, None), (user_id_0, None)])
    
    finally:
        CHARACTER_PREFERENCE_CACHE.clear()
