import vampytest

from ..cache import CHARACTER_PREFERENCE_CACHE, remove_from_cache
from ..character_preference import CharacterPreference


def test__remove_from_cache__miss():
    """
    Tests whether ``remove_from_cache`` works as intended.
    
    Case: Miss.
    """
    user_id = 202309170013
    
    character_preference = CharacterPreference(user_id, 'Komeiji_koishi')
    
    try:
        remove_from_cache(character_preference)
        
        vampytest.assert_eq(
            [*CHARACTER_PREFERENCE_CACHE.items()],
            [],
        )
    finally:
        CHARACTER_PREFERENCE_CACHE.clear()


def test__remove_from_cache__hit_empty():
    """
    Tests whether ``remove_from_cache`` works as intended.
    
    Case: Hitting, empty preference.
    """
    user_id = 202309170014
    
    character_preference = CharacterPreference(user_id, 'Komeiji_koishi')
    
    try:
        CHARACTER_PREFERENCE_CACHE[user_id] = None
        
        remove_from_cache(character_preference)
        
        vampytest.assert_eq(
            [*CHARACTER_PREFERENCE_CACHE.items()],
            [(user_id, None)],
        )
    finally:
        CHARACTER_PREFERENCE_CACHE.clear()


def test__remove_from_cache__hit_populated_missing():
    """
    Tests whether ``remove_from_cache`` works as intended.
    
    Case: Hitting, populated preference(s), but missing the preference.
    """
    user_id = 202309170015
    
    character_preference_0 = CharacterPreference(user_id, 'Komeiji_koishi')
    character_preference_1 = CharacterPreference(user_id, 'Komeiji_satori')
    
    try:
        CHARACTER_PREFERENCE_CACHE[user_id] = [character_preference_0]
        
        remove_from_cache(character_preference_1)
        
        vampytest.assert_eq(
            [*CHARACTER_PREFERENCE_CACHE.items()],
            [(user_id, [character_preference_0])],
        )
    finally:
        CHARACTER_PREFERENCE_CACHE.clear()


def test__remove_from_cache__hit_populated_existing():
    """
    Tests whether ``remove_from_cache`` works as intended.
    
    Case: Hitting, populated preference(s), the preference exists.
    """
    user_id = 202309170016
    
    character_preference_0 = CharacterPreference(user_id, 'Komeiji_koishi')
    character_preference_1 = CharacterPreference(user_id, 'Komeiji_satori')
    
    try:
        CHARACTER_PREFERENCE_CACHE[user_id] = [character_preference_0, character_preference_1]
        
        remove_from_cache(character_preference_1)
        
        vampytest.assert_eq(
            [*CHARACTER_PREFERENCE_CACHE.items()],
            [(user_id, [character_preference_0])],
        )
    finally:
        CHARACTER_PREFERENCE_CACHE.clear()


def test__remove_from_cache__hit_populated_clear():
    """
    Tests whether ``remove_from_cache`` works as intended.
    
    Case: Hitting, populated preference(s), 1 out of 1 removed -> clearing.
    """
    user_id = 202309170017
    
    character_preference = CharacterPreference(user_id, 'Komeiji_koishi')
    
    try:
        CHARACTER_PREFERENCE_CACHE[user_id] = [character_preference]
        
        remove_from_cache(character_preference)
        
        vampytest.assert_eq(
            [*CHARACTER_PREFERENCE_CACHE.items()],
            [(user_id, None)],
        )
    finally:
        CHARACTER_PREFERENCE_CACHE.clear()
