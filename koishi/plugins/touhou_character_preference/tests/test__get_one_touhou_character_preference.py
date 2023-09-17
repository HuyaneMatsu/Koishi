import vampytest

from ..cache import CHARACTER_PREFERENCE_CACHE, put_one_to_cache
from ..character_preference import CharacterPreference
from ..queries import get_one_touhou_character_preference


async def test__get_one_touhou_character_preference__cache_hit():
    """
    Tests whether ``get_one_touhou_character_preference`` works as intended.
    
    Case: Cache hit.
    
    This function is a coroutine.
    """
    query_called = False
    
    user_id = 2023090050
    character_preferences = [
        CharacterPreference(user_id, 'komeiji_koishi'),
        CharacterPreference(user_id, 'komeiji_satori'),
    ]
    
    async def query(user_id):
        nonlocal query_called
        query_called = True
    
    
    mocked = vampytest.mock_globals(
        get_one_touhou_character_preference,
        query_one_touhou_character_preference = query,
    )
    
    try:
        put_one_to_cache(user_id, character_preferences)
        
        output = await mocked(user_id)
        
        vampytest.assert_eq(output, character_preferences)
        
        vampytest.assert_false(query_called)
    finally:
        CHARACTER_PREFERENCE_CACHE.clear()


async def test__get_one_touhou_character_preference__database_hit_value():
    """
    Tests whether ``get_one_touhou_character_preference`` works as intended.
    
    Case: Database hit with value.
    
    This function is a coroutine.
    """
    query_called = False
    called_with_user_id = 0
    
    user_id = 2023090051
    character_preferences = [
        CharacterPreference(user_id, 'komeiji_koishi'),
        CharacterPreference(user_id, 'komeiji_satori'),
    ]
    
    async def query(user_id):
        nonlocal query_called
        nonlocal called_with_user_id
        nonlocal character_preferences
        
        query_called = True
        called_with_user_id = user_id
        
        return character_preferences
    
    
    mocked = vampytest.mock_globals(
        get_one_touhou_character_preference,
        _query_one_touhou_character_preference = query,
    )
    
    try:
        output = await mocked(user_id)
        
        vampytest.assert_eq(output, character_preferences)
        
        vampytest.assert_true(query_called)
        vampytest.assert_eq(called_with_user_id, user_id)
        
        vampytest.assert_eq([*CHARACTER_PREFERENCE_CACHE.items()], [(user_id, character_preferences)])
    finally:
        CHARACTER_PREFERENCE_CACHE.clear()


async def test__get_one_touhou_character_preference__database_hit_none():
    """
    Tests whether ``get_one_touhou_character_preference`` works as intended.
    
    Case: Database hit with none.
    
    This function is a coroutine.
    """
    query_called = False
    called_with_user_id = 0
    
    user_id = 2023090052
    character_preferences = None
    
    async def query(user_id):
        nonlocal query_called
        nonlocal called_with_user_id
        nonlocal character_preferences
        
        query_called = True
        called_with_user_id = user_id
        
        return character_preferences
    
    
    mocked = vampytest.mock_globals(
        get_one_touhou_character_preference,
        _query_one_touhou_character_preference = query,
    )
    
    try:
        output = await mocked(user_id)
        
        vampytest.assert_eq(output, character_preferences)
        
        vampytest.assert_true(query_called)
        vampytest.assert_eq(called_with_user_id, user_id)
        
        vampytest.assert_eq([*CHARACTER_PREFERENCE_CACHE.items()], [(user_id, character_preferences)])
    finally:
        CHARACTER_PREFERENCE_CACHE.clear()
