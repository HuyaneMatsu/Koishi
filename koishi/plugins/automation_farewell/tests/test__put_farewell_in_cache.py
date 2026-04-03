import vampytest

from ..constants import FAREWELL_CACHE, FAREWELL_CACHE_MAX_SIZE
from ..farewell_spam_protection import put_farewell_in_cache


def test__put_farewell_in_cache__nope():
    """
    Tests whether ``put_farewell_in_cache`` works as intended.
    
    Case: Not in cache.
    """
    farewell_cache = type(FAREWELL_CACHE)()
    
    mocked = vampytest.mock_globals(
        put_farewell_in_cache,
        FAREWELL_CACHE = farewell_cache,
        FAREWELL_CACHE_MAX_SIZE = FAREWELL_CACHE_MAX_SIZE,
    )
    
    guild_id = 202502220020
    farewelled_id = 202502220021
    
    output = mocked(guild_id, farewelled_id)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)
    vampytest.assert_eq(len(farewell_cache), 1)


def test__put_farewell_in_cache__yes():
    """
    Tests whether ``put_farewell_in_cache`` works as intended.
    
    Case: Not in cache.
    """
    farewell_cache = type(FAREWELL_CACHE)()
    
    mocked = vampytest.mock_globals(
        put_farewell_in_cache,
        FAREWELL_CACHE = farewell_cache,
        FAREWELL_CACHE_MAX_SIZE = FAREWELL_CACHE_MAX_SIZE,
    )
    
    guild_id = 202502220023
    farewelled_id = 202502220024
    
    farewell_cache[guild_id, farewelled_id] = None
    
    output = mocked(guild_id, farewelled_id)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)
    vampytest.assert_eq(len(farewell_cache), 1)


def test__put_farewell_in_cache__cache_max_size():
    """
    Tests whether ``put_farewell_in_cache`` works as intended.
    
    Case: Not in cache.
    """
    farewell_cache = type(FAREWELL_CACHE)()
    
    mocked = vampytest.mock_globals(
        put_farewell_in_cache,
        FAREWELL_CACHE = farewell_cache,
        FAREWELL_CACHE_MAX_SIZE = 1,
    )
    
    guild_id = 202502220025
    farewelled_id = 202502220026
    
    farewell_cache[guild_id, farewelled_id] = None
    
    guild_id = 202502220027
    farewelled_id = 202502220028
    
    mocked(guild_id, farewelled_id)
    
    vampytest.assert_eq(len(farewell_cache), 1)
