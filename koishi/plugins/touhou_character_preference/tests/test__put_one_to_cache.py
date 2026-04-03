import vampytest


from ..cache import CHARACTER_PREFERENCE_CACHE, put_one_to_cache
from ..character_preference import CharacterPreference


def test__put_one_to_cache__none():
    """
    Tests whether ``put_one_to_cache`` works as intended.
    
    Case: None.
    """
    user_id = 202309160020
    
    character_preferences = None
    
    try:
        put_one_to_cache(user_id, character_preferences)
        
        vampytest.assert_eq([*CHARACTER_PREFERENCE_CACHE.items()], [(user_id, character_preferences)])
    
    finally:
        CHARACTER_PREFERENCE_CACHE.clear()


def test__put_one_to_cache__value():
    """
    Tests whether ``put_one_to_cache`` works as intended.
    
    Case: actual value.
    """
    user_id = 202309160021
    
    character_preferences = [
        CharacterPreference(user_id, 'komeiji_koishi'),
        CharacterPreference(user_id, 'komeiji_satori'),
    ]
    
    try:
        put_one_to_cache(user_id, character_preferences)
        
        vampytest.assert_eq([*CHARACTER_PREFERENCE_CACHE.items()], [(user_id, character_preferences)])
    
    finally:
        CHARACTER_PREFERENCE_CACHE.clear()


def test__put_one_to_cache__move():
    """
    Tests whether ``put_one_to_cache`` works as intended.
    
    Case: move to end.
    """
    user_id_0 = 202309160022
    user_id_1 = 202309160023
    
    try:
        CHARACTER_PREFERENCE_CACHE[user_id_0] = None
        CHARACTER_PREFERENCE_CACHE[user_id_1] = None
        
        put_one_to_cache(user_id_0, None)
        
        vampytest.assert_eq([*CHARACTER_PREFERENCE_CACHE.items()], [(user_id_1, None), (user_id_0, None)])
    
    finally:
        CHARACTER_PREFERENCE_CACHE.clear()


def test__put_one_to_cache__pop():
    """
    Tests whether ``put_one_to_cache`` works as intended.
    
    Case: Cache full.
    """
    user_id_0 = 202309160024
    user_id_1 = 202309160025
    
    try:
        CHARACTER_PREFERENCE_CACHE[user_id_0] = None
        
        mocked = vampytest.mock_globals(put_one_to_cache, CHARACTER_PREFERENCE_CACHE_MAX_SIZE = 1)
        
        mocked(user_id_1, None)
        
        vampytest.assert_eq([*CHARACTER_PREFERENCE_CACHE.items()], [(user_id_1, None)])
    
    finally:
        CHARACTER_PREFERENCE_CACHE.clear()
