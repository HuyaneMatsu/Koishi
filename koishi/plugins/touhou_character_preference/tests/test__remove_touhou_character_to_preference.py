import vampytest

from ...touhou_core.characters import KOMEIJI_KOISHI, KOMEIJI_SATORI

from ..cache import CHARACTER_PREFERENCE_CACHE, put_one_to_cache
from ..character_preference import CharacterPreference
from ..queries import remove_touhou_character_from_preference


async def test__remove_touhou_character_from_preference__missing():
    """
    Tests whether ``remove_touhou_character_from_preference`` works as intended.
    
    This function is a coroutine.
    
    Case: no entry in db.
    """
    user_id = 202309170038
    
    query_called = False
    
    async def query(character_preference):
        nonlocal query_called
        
        query_called = True
    
    
    mocked = vampytest.mock_globals(
        remove_touhou_character_from_preference,
        _remove_touhou_character_preference = query,
    )
    
    try:
        put_one_to_cache(user_id, None)
        
        await mocked(user_id, KOMEIJI_KOISHI)
        
        vampytest.assert_false(query_called)
        
        vampytest.assert_eq(
            [*CHARACTER_PREFERENCE_CACHE.items()],
            [(user_id, None)],
        )
    finally:
        CHARACTER_PREFERENCE_CACHE.clear()


async def test__remove_touhou_character_from_preference__shortening():
    """
    Tests whether ``remove_touhou_character_from_preference`` works as intended.
    
    This function is a coroutine.
    
    Case: shortening from multiple entries.
    """
    user_id = 202309170039
    character_preference_0 = CharacterPreference(user_id, KOMEIJI_KOISHI.system_name)
    character_preference_1 = CharacterPreference(user_id, KOMEIJI_SATORI.system_name)
    
    query_called = False
    called_with_character_preference = None
    
    async def query(character_preference):
        nonlocal query_called
        nonlocal called_with_character_preference
        
        query_called = True
        called_with_character_preference = character_preference
    
    
    mocked = vampytest.mock_globals(
        remove_touhou_character_from_preference,
        _remove_touhou_character_preference = query,
    )
    
    try:
        put_one_to_cache(user_id, [character_preference_1, character_preference_0])
        
        await mocked(user_id, KOMEIJI_KOISHI)
        
        vampytest.assert_true(query_called)
        vampytest.assert_eq(called_with_character_preference, character_preference_0)
        
        vampytest.assert_eq(
            [*CHARACTER_PREFERENCE_CACHE.items()],
            [(user_id, [character_preference_1])],
        )
    finally:
        CHARACTER_PREFERENCE_CACHE.clear()


async def test__remove_touhou_character_from_preference__clearing():
    """
    Tests whether ``remove_touhou_character_from_preference`` works as intended.
    
    This function is a coroutine.
    
    Case: only one entry -> clearing.
    """
    user_id = 202309170040
    character_preference_0 = CharacterPreference(user_id, KOMEIJI_KOISHI.system_name)
    
    query_called = False
    called_with_character_preference = None
    
    
    async def query(character_preference):
        nonlocal query_called
        nonlocal called_with_character_preference
        
        query_called = True
        called_with_character_preference = character_preference
    
    mocked = vampytest.mock_globals(
        remove_touhou_character_from_preference,
        _remove_touhou_character_preference = query,
    )
    
    try:
        put_one_to_cache(user_id, [character_preference_0])
        
        await mocked(user_id, character_preference_0)
        
        vampytest.assert_true(query_called)
        vampytest.assert_eq(called_with_character_preference, character_preference_0)
        
        vampytest.assert_eq(
            [*CHARACTER_PREFERENCE_CACHE.items()],
            [(user_id, None)],
        )
    finally:
        CHARACTER_PREFERENCE_CACHE.clear()
