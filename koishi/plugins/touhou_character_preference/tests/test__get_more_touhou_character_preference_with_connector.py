import vampytest

from ..cache import CHARACTER_PREFERENCE_CACHE, put_one_to_cache
from ..character_preference import CharacterPreference
from ..queries import get_more_touhou_character_preference_with_connector


async def test__get_more_touhou_character_preference_with_connector__cache_hit():
    """
    Tests whether ``get_more_touhou_character_preference_with_connector`` works as intended.
    
    Case: Cache hit.
    
    This function is a coroutine.
    """
    query_called = False
    connector = object()
    
    user_id_0 = 2023090080
    user_id_1 = 2023090081
    
    character_preferences_0 = [
        CharacterPreference(user_id_0, 'komeiji_koishi'),
        CharacterPreference(user_id_0, 'komeiji_satori'),
    ]
    
    character_preferences_1 = [
        CharacterPreference(user_id_1, 'kaenbyou_rin'),
        CharacterPreference(user_id_1, 'reiuji_utsuho'),
    ]
    
    async def query(user_ids, connector):
        nonlocal query_called
        query_called = True
    
    
    mocked = vampytest.mock_globals(
        get_more_touhou_character_preference_with_connector,
        _query_more_touhou_character_preference_with_connector = query,
    )
    
    try:
        put_one_to_cache(user_id_0, character_preferences_0)
        put_one_to_cache(user_id_1, character_preferences_1)
        
        output = await mocked([user_id_0, user_id_1], connector)
        
        vampytest.assert_eq(output, [*character_preferences_0, *character_preferences_1])
        
        vampytest.assert_false(query_called)
    finally:
        CHARACTER_PREFERENCE_CACHE.clear()


async def test__get_more_touhou_character_preference_with_connector__database_hit_value():
    """
    Tests whether ``get_more_touhou_character_preference_with_connector`` works as intended.
    
    Case: Database hit with value.
    
    This function is a coroutine.
    """
    query_called = False
    called_with_user_ids = None
    connector = object()
    called_with_connector = None
    
    user_id_0 = 2023090082
    user_id_1 = 2023090083
    
    character_preferences_0 = [
        CharacterPreference(user_id_0, 'komeiji_koishi'),
        CharacterPreference(user_id_0, 'komeiji_satori'),
    ]
    
    character_preferences_1 = [
        CharacterPreference(user_id_1, 'kaenbyou_rin'),
        CharacterPreference(user_id_1, 'reiuji_utsuho'),
    ]
    
    async def query(user_ids, connector):
        nonlocal query_called
        nonlocal called_with_user_ids
        nonlocal character_preferences_0
        nonlocal character_preferences_1
        nonlocal called_with_connector
        
        query_called = True
        called_with_user_ids = user_ids
        called_with_connector = connector
        
        return [*character_preferences_0, *character_preferences_1]
    
    
    mocked = vampytest.mock_globals(
        get_more_touhou_character_preference_with_connector,
        _query_more_touhou_character_preference_with_connector = query,
    )
    
    try:
        output = await mocked([user_id_0, user_id_1], connector)
        
        vampytest.assert_eq(output, [*character_preferences_0, *character_preferences_1])
        
        vampytest.assert_true(query_called)
        vampytest.assert_eq(called_with_user_ids, [user_id_0, user_id_1])
        vampytest.assert_is(called_with_connector, connector)
        
        vampytest.assert_eq(
            [*CHARACTER_PREFERENCE_CACHE.items()],
            [(user_id_0, character_preferences_0), (user_id_1, character_preferences_1)],
        )
    finally:
        CHARACTER_PREFERENCE_CACHE.clear()


async def test__get_more_touhou_character_preference_with_connector__database_hit_none():
    """
    Tests whether ``get_more_touhou_character_preference_with_connector`` works as intended.
    
    Case: Database hit with none.
    
    This function is a coroutine.
    """
    query_called = False
    called_with_user_ids = 0
    connector = object()
    called_with_connector = None
    
    user_id_0 = 2023090084
    user_id_1 = 2023090085
    
    character_preferences_0 = None
    character_preferences_1 = None
    
    async def query(user_ids, connector):
        nonlocal query_called
        nonlocal called_with_user_ids
        nonlocal called_with_connector
        
        query_called = True
        called_with_user_ids = user_ids
        called_with_connector = connector
        
        return None
    
    
    mocked = vampytest.mock_globals(
        get_more_touhou_character_preference_with_connector,
        _query_more_touhou_character_preference_with_connector = query,
    )
    
    try:
        output = await mocked([user_id_0, user_id_1], connector)
        
        vampytest.assert_is(output, None)
        
        vampytest.assert_true(query_called)
        vampytest.assert_eq(called_with_user_ids, [user_id_0, user_id_1])
        vampytest.assert_is(called_with_connector, connector)
        
        vampytest.assert_eq(
            [*CHARACTER_PREFERENCE_CACHE.items()],
            [(user_id_0, character_preferences_0), (user_id_1, character_preferences_1)],
        )
    finally:
        CHARACTER_PREFERENCE_CACHE.clear()


async def test__get_more_touhou_character_preference_with_connector__mixed_hit_value():
    """
    Tests whether ``get_more_touhou_character_preference_with_connector`` works as intended.
    
    Case: Cache and database hit with value.
    
    This function is a coroutine.
    """
    query_called = False
    called_with_user_ids = None
    connector = object()
    called_with_connector = None
    
    user_id_0 = 2023090086
    user_id_1 = 2023090088
    
    character_preferences_0 = [
        CharacterPreference(user_id_0, 'komeiji_koishi'),
        CharacterPreference(user_id_0, 'komeiji_satori'),
    ]
    
    character_preferences_1 = [
        CharacterPreference(user_id_1, 'kaenbyou_rin'),
        CharacterPreference(user_id_1, 'reiuji_utsuho'),
    ]
    
    async def query(user_ids, connector):
        nonlocal query_called
        nonlocal called_with_user_ids
        nonlocal character_preferences_1
        nonlocal called_with_connector
        
        query_called = True
        called_with_user_ids = user_ids
        called_with_connector = connector
        
        return [*character_preferences_1]
    
    
    mocked = vampytest.mock_globals(
        get_more_touhou_character_preference_with_connector,
        _query_more_touhou_character_preference_with_connector = query,
    )
    
    try:
        put_one_to_cache(user_id_0, character_preferences_0)
        
        output = await mocked([user_id_0, user_id_1], connector)
        
        vampytest.assert_eq(output, [*character_preferences_0, *character_preferences_1])
        
        vampytest.assert_true(query_called)
        vampytest.assert_eq(called_with_user_ids, [user_id_1])
        vampytest.assert_is(called_with_connector, connector)
        
        vampytest.assert_eq(
            [*CHARACTER_PREFERENCE_CACHE.items()],
            [(user_id_0, character_preferences_0), (user_id_1, character_preferences_1)],
        )
    finally:
        CHARACTER_PREFERENCE_CACHE.clear()
