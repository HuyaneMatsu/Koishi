import vampytest


from ..cache import CHARACTER_PREFERENCE_CACHE, put_more_to_cache
from ..character_preference import CharacterPreference


def test__put_more_to_cache__none():
    """
    Tests whether ``put_more_to_cache`` works as intended.
    
    Case: None.
    """
    user_id_0 = 202309160030
    user_id_1 = 202309160031
    
    character_preferences = None
    
    try:
        put_more_to_cache([user_id_0, user_id_1], character_preferences)
        
        vampytest.assert_eq([*CHARACTER_PREFERENCE_CACHE.items()], [(user_id_0, None), (user_id_1, None)])
    
    finally:
        CHARACTER_PREFERENCE_CACHE.clear()


def test__put_more_to_cache__value():
    """
    Tests whether ``put_more_to_cache`` works as intended.
    
    Case: actual value.
    """
    user_id_0 = 202309160032
    user_id_1 = 202309160033
    
    character_preferences_0 = [
        CharacterPreference(user_id_0, 'komeiji_koishi'),
        CharacterPreference(user_id_0, 'komeiji_satori'),
    ]
    character_preferences_1 = [
        CharacterPreference(user_id_1, 'kaenbyou_rin'),
        CharacterPreference(user_id_1, 'reiuji_utsuho'),
    ]
    
    try:
        put_more_to_cache([user_id_0, user_id_1], [*character_preferences_0, *character_preferences_1])
        
        vampytest.assert_eq(
            [*CHARACTER_PREFERENCE_CACHE.items()],
            [(user_id_0, character_preferences_0), (user_id_1, character_preferences_1)],
        )
    
    finally:
        CHARACTER_PREFERENCE_CACHE.clear()


def test__put_more_to_cache__mixed():
    """
    Tests whether ``put_more_to_cache`` works as intended.
    
    Case: Mixed, none and value.
    """
    user_id_0 = 202309160034
    user_id_1 = 202309160035
    
    character_preferences_0 = [
        CharacterPreference(user_id_0, 'komeiji_koishi'),
        CharacterPreference(user_id_0, 'komeiji_satori'),
    ]
    character_preferences_1 = None
    
    try:
        put_more_to_cache([user_id_0, user_id_1], [*character_preferences_0])
        
        vampytest.assert_eq(
            [*CHARACTER_PREFERENCE_CACHE.items()],
            [(user_id_0, character_preferences_0), (user_id_1, character_preferences_1)],
        )
    
    finally:
        CHARACTER_PREFERENCE_CACHE.clear()


def test__put_more_to_cache__move():
    """
    Tests whether ``put_more_to_cache`` works as intended.
    
    Case: move to end.
    """
    user_id_0 = 202309160035
    user_id_1 = 202309160036
    
    try:
        CHARACTER_PREFERENCE_CACHE[user_id_0] = None
        CHARACTER_PREFERENCE_CACHE[user_id_1] = None
        
        put_more_to_cache([user_id_0], None)
        
        vampytest.assert_eq([*CHARACTER_PREFERENCE_CACHE.items()], [(user_id_1, None), (user_id_0, None)])
    
    finally:
        CHARACTER_PREFERENCE_CACHE.clear()


def test__put_more_to_cache__pop():
    """
    Tests whether ``put_more_to_cache`` works as intended.
    
    Case: Cache full.
    """
    user_id_0 = 202309160037
    user_id_1 = 202309160038
    
    try:
        CHARACTER_PREFERENCE_CACHE[user_id_0] = None
        
        mocked = vampytest.mock_globals(put_more_to_cache, 2, CHARACTER_PREFERENCE_MAX_SIZE = 1)
        
        mocked([user_id_1], None)
        
        vampytest.assert_eq([*CHARACTER_PREFERENCE_CACHE.items()], [(user_id_1, None)])
    
    finally:
        CHARACTER_PREFERENCE_CACHE.clear()
