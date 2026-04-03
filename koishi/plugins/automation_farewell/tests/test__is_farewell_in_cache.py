import vampytest

from ..constants import FAREWELL_CACHE, FAREWELL_CACHE_MAX_SIZE
from ..farewell_spam_protection import is_farewell_in_cache


def test__is_farewell_in_cache__nope():
    """
    Tests whether ``is_farewell_in_cache`` works as intended.
    
    Case: Not in cache.
    """
    farewell_cache = type(FAREWELL_CACHE)()
    
    mocked = vampytest.mock_globals(
        is_farewell_in_cache,
        FAREWELL_CACHE = farewell_cache,
        FAREWELL_CACHE_MAX_SIZE = FAREWELL_CACHE_MAX_SIZE,
    )
    
    guild_id = 202502220030
    farewelled_id = 202502220031
    
    output = mocked(guild_id, farewelled_id)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)
    vampytest.assert_eq(len(farewell_cache), 0)


def test__is_farewell_in_cache__yes():
    """
    Tests whether ``is_farewell_in_cache`` works as intended.
    
    Case: Not in cache.
    """
    farewell_cache = type(FAREWELL_CACHE)()
    
    mocked = vampytest.mock_globals(
        is_farewell_in_cache,
        FAREWELL_CACHE = farewell_cache,
        FAREWELL_CACHE_MAX_SIZE = FAREWELL_CACHE_MAX_SIZE,
    )
    
    guild_id = 202502220032
    farewelled_id = 202502220033
    
    farewell_cache[guild_id, farewelled_id] = None
    
    output = mocked(guild_id, farewelled_id)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)
    vampytest.assert_eq(len(farewell_cache), 1)
