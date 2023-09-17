import vampytest

from ..cache import CHARACTER_PREFERENCE_CACHE, put_one_to_cache
from ..character_preference import CharacterPreference
from ..queries import get_one_touhou_character_preference_with_connector


async def test__get_one_touhou_character_preference_with_connector__cache_hit():
    """
    Tests whether ``get_one_touhou_character_preference_with_connector`` works as intended.
    
    Case: Cache hit.
    
    This function is a coroutine.
    """
    query_called = False
    connector = object()
    
    user_id = 2023090060
    character_preferences = [
        CharacterPreference(user_id, 'komeiji_koishi'),
        CharacterPreference(user_id, 'komeiji_satori'),
    ]
    
    async def query(user_id, connector):
        nonlocal query_called
        query_called = True
    
    
    mocked = vampytest.mock_globals(
        get_one_touhou_character_preference_with_connector,
        _query_one_touhou_character_preference_with_connector = query,
    )
    
    try:
        put_one_to_cache(user_id, character_preferences)
        
        output = await mocked(user_id, connector)
        
        vampytest.assert_eq(output, character_preferences)
        
        vampytest.assert_false(query_called)
    finally:
        CHARACTER_PREFERENCE_CACHE.clear()


async def test__get_one_touhou_character_preference_with_connector__database_hit_value():
    """
    Tests whether ``get_one_touhou_character_preference_with_connector`` works as intended.
    
    Case: Database hit with value.
    
    This function is a coroutine.
    """
    query_called = False
    called_with_user_id = 0
    connector = object()
    called_with_connector = None
    
    user_id = 2023090061
    character_preferences = [
        CharacterPreference(user_id, 'komeiji_koishi'),
        CharacterPreference(user_id, 'komeiji_satori'),
    ]
    
    async def query(user_id, connector):
        nonlocal query_called
        nonlocal called_with_user_id
        nonlocal character_preferences
        nonlocal called_with_connector
        
        query_called = True
        called_with_user_id = user_id
        called_with_connector = connector
        
        return character_preferences
    
    
    mocked = vampytest.mock_globals(
        get_one_touhou_character_preference_with_connector,
        _query_one_touhou_character_preference_with_connector = query,
    )
    
    try:
        output = await mocked(user_id, connector)
        
        vampytest.assert_eq(output, character_preferences)
        
        vampytest.assert_true(query_called)
        vampytest.assert_eq(called_with_user_id, user_id)
        vampytest.assert_is(called_with_connector, connector)
        
        vampytest.assert_eq([*CHARACTER_PREFERENCE_CACHE.items()], [(user_id, character_preferences)])
    finally:
        CHARACTER_PREFERENCE_CACHE.clear()


async def test__get_one_touhou_character_preference_with_connector__database_hit_none():
    """
    Tests whether ``get_one_touhou_character_preference_with_connector`` works as intended.
    
    Case: Database hit with none.
    
    This function is a coroutine.
    """
    query_called = False
    called_with_user_id = 0
    connector = object()
    called_with_connector = None
    
    user_id = 2023090062
    character_preferences = None
    
    async def query(user_id, connector):
        nonlocal query_called
        nonlocal called_with_user_id
        nonlocal character_preferences
        nonlocal called_with_connector
        
        query_called = True
        called_with_user_id = user_id
        called_with_connector = connector
        
        return character_preferences
    
    
    mocked = vampytest.mock_globals(
        get_one_touhou_character_preference_with_connector,
        _query_one_touhou_character_preference_with_connector = query,
    )
    
    try:
        output = await mocked(user_id, connector)
        
        vampytest.assert_eq(output, character_preferences)
        
        vampytest.assert_true(query_called)
        vampytest.assert_eq(called_with_user_id, user_id)
        vampytest.assert_is(called_with_connector, connector)
        
        vampytest.assert_eq([*CHARACTER_PREFERENCE_CACHE.items()], [(user_id, character_preferences)])
    finally:
        CHARACTER_PREFERENCE_CACHE.clear()
