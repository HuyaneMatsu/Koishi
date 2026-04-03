import vampytest

from ..cache import CHARACTER_PREFERENCE_CACHE, add_to_cache
from ..character_preference import CharacterPreference


def test__add_to_cache__miss():
    """
    Tests whether ``add_to_cache`` works as intended.
    
    Case: Miss.
    """
    user_id = 202309170010
    
    character_preference = CharacterPreference(user_id, 'Komeiji_koishi')
    
    try:
        add_to_cache(character_preference)
        
        vampytest.assert_eq(
            [*CHARACTER_PREFERENCE_CACHE.items()],
            [],
        )
    finally:
        CHARACTER_PREFERENCE_CACHE.clear()


def test__add_to_cache__hit_empty():
    """
    Tests whether ``add_to_cache`` works as intended.
    
    Case: Hitting, empty preference.
    """
    user_id = 202309170011
    
    character_preference = CharacterPreference(user_id, 'Komeiji_koishi')
    
    try:
        CHARACTER_PREFERENCE_CACHE[user_id] = None
        
        add_to_cache(character_preference)
        
        vampytest.assert_eq(
            [*CHARACTER_PREFERENCE_CACHE.items()],
            [(user_id, [character_preference])],
        )
    finally:
        CHARACTER_PREFERENCE_CACHE.clear()


def test__add_to_cache__hit_populated():
    """
    Tests whether ``add_to_cache`` works as intended.
    
    Case: Hitting, populated preference(s).
    """
    user_id = 202309170012
    
    character_preference_0 = CharacterPreference(user_id, 'Komeiji_koishi')
    character_preference_1 = CharacterPreference(user_id, 'Komeiji_satori')
    
    try:
        CHARACTER_PREFERENCE_CACHE[user_id] = [character_preference_0]
        
        add_to_cache(character_preference_1)
        
        vampytest.assert_eq(
            [*CHARACTER_PREFERENCE_CACHE.items()],
            [(user_id, [character_preference_0, character_preference_1])],
        )
    finally:
        CHARACTER_PREFERENCE_CACHE.clear()
